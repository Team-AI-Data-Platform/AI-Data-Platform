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
    MD/TXT 문서를 직접 읽어 RAG 문서 데이터로 변환한다.

    PDF, PPTX, DOCX 등은 별도 Extract 스크립트를 통해
    JSONL로 변환되지만, MD/TXT는 구조가 단순하므로
    별도 추출 단계 없이 여기서 직접 처리한다.

    처리 내용:
        - md 디렉터리의 .md 파일 수집
        - txt 디렉터리의 .txt 파일 수집
        - 텍스트 정제(clean_text)
        - 문서 메타데이터 생성
        - List[dict] 형태로 반환

    반환 결과는 JSONL 추출 결과와 함께 Chunk 생성 단계의
    입력 데이터로 사용된다.
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
    """
    extracted_text 디렉터리의 JSONL 추출 결과를 읽어 하나의 문서 목록으로 통합한다.
     - PDF, PPTX, DOCX 등은 사전 추출된 JSONL 파일을 읽고,
     - MD/TXT 파일은 별도 추출 단계가 없으므로 직접 읽어 동일한 문서 목록(records)에 포함한다.
    반환된 데이터는 Chunk 생성 단계의 입력으로 사용된다.
    """
    records: list[dict] = []

    for jsonl_path in sorted(EXTRACTED_TEXT_DIR.glob("*_extracted.jsonl")):

        records.extend(read_jsonl(jsonl_path))
        ##############################
        # extend()
        ##############################
        # 기능:
        #   리스트(또는 반복 가능한 객체)의 모든 요소를
        #   현재 리스트 끝에 추가한다.
        # 역할:
        #   여러 개의 데이터를 하나의 리스트로 합칠 때 사용한다.
        # 파라미터:
        #   iterable
        #     - list
        #     - tuple
        #     - set
        #     - generator
        #     - 기타 반복 가능한 객체
        # 리턴값:  없음 (None)
        # 예시:
        #   a = [1, 2]
        #   a.extend([3, 4])
        # 결과:   [1, 2, 3, 4]
        # 참고:
        #   append() 는 객체 자체를 추가하고,
        #   extend() 는 내부 요소들을 개별적으로 추가한다.
        ##############################

        ##############################
        # read_jsonl()
        ##############################
        # 기능:
        #   JSONL(JSON Lines) 파일을 읽어
        #   Python 객체(List[dict])로 변환한다.
        # 역할:
        #   JSONL 파일에 저장된 문서 데이터를
        #   메모리로 로드하는 역할을 수행한다.
        # 파라미터:
        #   jsonl_path : Path     -> 읽을 JSONL 파일 경로
        # 리턴값:
        #   list[dict]     -> JSONL 파일에 저장된 데이터 목록
        # 예시:   입력 파일
        #   {"text":"문서1"}
        #   {"text":"문서2"}
        #   {"text":"문서3"}
        #   반환 결과
        #   [
        #       {"text":"문서1"},
        #       {"text":"문서2"},
        #       {"text":"문서3"}
        #   ]
        #
        # 참고:
        #   JSONL은 한 줄에 하나의 JSON 객체를 저장하는 형식이다.
        #   일반 JSON 배열([ ])과 달리 대용량 데이터 처리에 적합하다.
        ##############################
        #def read_jsonl(jsonl_path: Path) -> list[dict]:




    # TXT, MD 등 일반 텍스트 파일을 스캔하여 문서 데이터를 추출한다.
    # 반환값:
    # [
    #   {"source":"guide.md", "text":"..."},
    #   {"source":"api.txt", "text":"..."}
    # ]
    #
    # 추출된 모든 문서를 records 리스트에 추가한다.
    records.extend(extract_plain_text_files())

    return records





def build_chunks() -> list[dict]:
    ensure_directories()

    # Extract 단계에서 수집된 전체 문서 목록(List[dict])
    # JSONL 추출 결과 + MD/TXT 문서를 통합하여 반환
    extracted_records = load_extracted_records()



    chunk_records: list[dict] = []



    ##############################
    # read_jsonl() 에서 JSONL → list[dict[str, Any]] 로 변환했으므로
    # 문서(dict) 1건씩 record 에 담아 처리한다.
    ##############################
    for record in extracted_records:
        source_id = record.get("id", "")
        text = record.get("text", "")
        metadata = record.get("metadata", {})



        # split_text() 는 프로젝트에서 직접 구현한 함수이며,
        # 문서를 Chunk 목록(list[str])으로 분할한다.
        # 예) ["Chunk1", "Chunk2", "Chunk3"]
        chunks = split_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)

        for chunk_index, chunk_text in enumerate(chunks, start=1):

            # 원본 metadata 복사 후
            # Chunk 관련 메타데이터를 추가한다.
            # (원본 문서에는 없는 정보)
            chunk_metadata = dict(metadata)
            chunk_metadata["source_record_id"] = source_id
            chunk_metadata["chunk_index"] = chunk_index
            chunk_metadata["chunk_size"] = len(chunk_text)

            chunk_records.append(
                {
                    # 원본 문서(source_id)의 Chunk 고유 ID 생성
                    # 구성:
                    #   source_id   : 원본 문서 ID
                    #   "chunk"     : Chunk 데이터 구분자
                    #   chunk_index : Chunk 순번
                    # 예)
                    #   source_id = "abc123"
                    #   chunk_index = 0
                    #   stable_id("abc123", "chunk", 0)
                    # 동일한 문서와 Chunk 순번에 대해서는 항상 동일한 ID가 생성된다.
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
