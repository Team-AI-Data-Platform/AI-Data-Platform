"""
09_extract_pdf.py

PDF 문서에서 페이지별 텍스트를 추출한다.

입력:
- enterprise_docs/pdf/*.pdf

출력:
- extracted_text/pdf_extracted.jsonl

실행:
python 09_extract_pdf.py
"""

from __future__ import annotations

from pypdf import PdfReader

from step2_5_config import ENTERPRISE_DOCS_DIR, EXTRACTED_TEXT_DIR, ensure_directories
from step2_5_utils import clean_text, find_files, stable_id, write_jsonl, print_record_summary


def extract_pdf_files() -> list[dict]:

    ## 실습에 필요한 디렉토리들을 (없는경우) 미리 생성함.
    ensure_directories()

    pdf_dir = ENTERPRISE_DOCS_DIR / "pdf"
    pdf_files = find_files(pdf_dir, (".pdf",))

    records: list[dict] = []

    for pdf_path in pdf_files:
        print(f"11==========> pdf_path :: {pdf_path}")
        try:
            reader = PdfReader(str(pdf_path))
        except Exception as exc:
            print(f"[PDF 읽기 실패] {pdf_path.name}: {exc}")
            continue

        for page_index, page in enumerate(reader.pages, start=1):
            try:
                text = page.extract_text() or ""
            except Exception as exc:
                print(f"[PDF 페이지 추출 실패] {pdf_path.name} page={page_index}: {exc}")
                text = ""

            text = clean_text(text)

            if not text:
                continue

            records.append(
                {
                    "id": stable_id(pdf_path.name, "pdf", page_index),
                    "text": text,
                    "metadata": {
                        "file_name": pdf_path.name,
                        "document_type": "pdf",
                        "page_no": page_index,
                        "source_path": str(pdf_path),
                        "extractor": "pypdf",
                    },
                }
            )

    return records


def main() -> None:
    output_path = EXTRACTED_TEXT_DIR / "pdf_extracted.jsonl"
    records = extract_pdf_files()
    count = write_jsonl(output_path, records)
    print_record_summary("PDF 텍스트 추출 완료", count, output_path)


if __name__ == "__main__":
    main()
