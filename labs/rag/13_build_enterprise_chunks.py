"""
13_build_enterprise_chunks.py

추출된 텍스트 JSONL 파일을 읽어서 RAG 검색용 Chunk를 생성한다.

입력:
- extracted_text/*.jsonl

출력:
- enterprise_chunks/enterprise_chunks.jsonl

실행:
python 13_build_enterprise_chunks.py
"""

from __future__ import annotations

from step2_5_config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    CHUNKS_DIR,
    ENTERPRISE_DOCS_DIR,
    EXTRACTED_TEXT_DIR,
    ensure_directories,
)
from step2_5_utils import (
    clean_text,
    find_files,
    read_jsonl,
    split_text,
    stable_id,
    write_jsonl,
    print_record_summary,
)


def extract_plain_text_files() -> list[dict]:
    """
    MD/TXT 파일은 별도 추출 스크립트 없이 여기서 직접 읽는다.
    """
    records: list[dict] = []

    targets = [
        (ENTERPRISE_DOCS_DIR / "md", ".md", "md"),
        (ENTERPRISE_DOCS_DIR / "txt", ".txt", "txt"),
    ]

    for directory, extension, doc_type in targets:
        for path in find_files(directory, (extension,)):
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                text = path.read_text(encoding="cp949")
            except Exception as exc:
                print(f"[텍스트 파일 읽기 실패] {path.name}: {exc}")
                continue

            text = clean_text(text)

            if not text:
                continue

            records.append(
                {
                    "id": stable_id(path.name, doc_type),
                    "text": text,
                    "metadata": {
                        "file_name": path.name,
                        "document_type": doc_type,
                        "source_path": str(path),
                        "extractor": "plain-text",
                    },
                }
            )

    return records


def load_extracted_records() -> list[dict]:
    """extracted_text 디렉터리의 모든 JSONL 추출 결과를 읽는다."""
    records: list[dict] = []

    for jsonl_path in sorted(EXTRACTED_TEXT_DIR.glob("*_extracted.jsonl")):
        records.extend(read_jsonl(jsonl_path))

    records.extend(extract_plain_text_files())

    return records


def build_chunks() -> list[dict]:
    ensure_directories()

    extracted_records = load_extracted_records()
    chunk_records: list[dict] = []

    for record in extracted_records:
        source_id = record.get("id", "")
        text = record.get("text", "")
        metadata = record.get("metadata", {})

        chunks = split_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)

        for chunk_index, chunk_text in enumerate(chunks, start=1):
            chunk_metadata = dict(metadata)
            chunk_metadata["source_record_id"] = source_id
            chunk_metadata["chunk_index"] = chunk_index
            chunk_metadata["chunk_size"] = len(chunk_text)

            chunk_records.append(
                {
                    "id": stable_id(source_id, "chunk", chunk_index),
                    "text": chunk_text,
                    "metadata": chunk_metadata,
                }
            )

    return chunk_records


def main() -> None:
    output_path = CHUNKS_DIR / "enterprise_chunks.jsonl"
    records = build_chunks()
    count = write_jsonl(output_path, records)
    print_record_summary("Enterprise Chunk 생성 완료", count, output_path)


if __name__ == "__main__":
    main()
