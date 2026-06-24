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
            ############################################################
            # PyPDF2.PdfReader
            ############################################################
            # 라이브러리 :: PyPDF2
            # 역할
            #   PDF 파일을 읽기(Read) 위한 객체이다.
            # 주요 기능
            #   - PDF 문서 열기
            #   - 페이지 수 조회
            #   - 페이지 객체(Page) 접근
            #   - PDF 텍스트 추출
            #   - PDF 메타데이터 조회
            # 생성자 파라미터
            #   stream
            #       PDF 파일 경로(str) 또는 파일 객체
            #   예)
            #       PdfReader("sample.pdf")
            # 반환 객체 ::  PdfReader 객체 반환
            # 주요 속성
            #   pages
            #       PDF 페이지 목록(List 형태) :: 예)  reader.pages[0]
            #   metadata
            #       PDF 메타데이터 정보 :: 예)   reader.metadata
            #
            # 사용 예제
            #   reader = PdfReader("sample.pdf")
            #   total_pages = len(reader.pages)
            #   page = reader.pages[0]
            #   text = page.extract_text()
            # 참고
            #   PdfReader는 PDF 내부에 저장된 텍스트를 읽는다.
            #   따라서 스캔본 PDF(이미지 PDF)의 경우
            #   extract_text() 결과가 None 또는 빈 문자열이 될 수 있다.
            #   스캔 PDF는 OCR(Tesseract, AI OCR, Vision LLM 등)이 필요하다.
            ############################################################



        except Exception as exc:
            print(f"[PDF 읽기 실패] {pdf_path.name}: {exc}")
            continue

        ############################################################   
        # for page_index, page 문법은
        ############################################################
        # Tuple을 자동으로 분리(Unpacking)하여
        # page_index와 page 변수에 각각 저장한다.
        # start=1
        #   페이지 번호를 1부터 시작하도록 지정
        ##########################################################
        for page_index, page in enumerate(reader.pages, start=1):
            ############################################################
            # Python 내장 함수 enumerate()  : (index, value) 형태의 튜플(Tuple)을 반환
            ############################################################
            # 역할 :: 반복 가능한 객체(List, Tuple 등)를 순회하면서 순번(Index)과 값을 함께 반환한다.
            # 주요 기능
            #   - 현재 반복 순서를 확인할 수 있다.
            #   - Index와 데이터를 동시에 처리할 수 있다.
            # 함수 시그니처
            #   enumerate(
            #       iterable,
            #       start=0
            #   )
            # 파라미터
            #   iterable :: 반복할 컬렉션 객체
            #   start ::  시작 Index 값(기본값 : 0)
            # 반환값
            #   (index, value) 형태의 튜플(Tuple)을 반환
            # 예)
            #   enumerate(["A", "B", "C"])
            #
            # 결과
            #   (0, "A")
            #   (1, "B")
            #   (2, "C")
            ############################################################


            try:
                text = page.extract_text() or ""
                ############################################################
                # PyPDF2 Page.extract_text()
                ############################################################
                # 라이브러리 :: PyPDF2
                # 역할 :: PDF 페이지(Page)에서 텍스트를 추출한다.
                # 주요 기능
                #   - PDF 내부 텍스트 읽기
                #   - 추출된 텍스트를 문자열(str)로 반환
                # 반환값(Return)
                #   성공 시
                #       str (추출된 텍스트)
                #   실패 시
                #       None
                # 예)
                #   page = reader.pages[0]
                #   text = page.extract_text()
                #   print(text)
                # 참고
                #   PDF 내부에 실제 텍스트 데이터가 있어야 추출 가능하다.
                #   스캔본 PDF(이미지 PDF)의 경우 텍스트가 존재하지 않으므로 None 이 반환될 수 있다.
                #   이 경우 OCR 또는 Vision LLM이 필요하다.
                ############################################################


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









############################################################
# main() 함수
############################################################
# 역할  ::  이 파이썬 파일의 전체 실행 흐름을 담당하는 진입 함수이다.
# 설명
#   프로그램이 실행되었을 때 처리해야 할 주요 작업들을 순서대로 호출한다.
#   1. PDF 추출 결과를 저장할 파일 경로 생성
#   2. PDF 파일들에서 텍스트 추출
#   3. 추출 결과를 JSON 파일로 저장
#   4. 처리 결과 요약 출력
# 반환값  :: None
#   main() 함수는 결과값을 반환하기 위한 함수가 아니라
#   프로그램 실행 절차를 관리하기 위한 함수이다.
############################################################
def main() -> None:

    # 추출 결과를 저장할 JSON 파일 경로 생성
    # EXTRACTED_TEXT_DIR 경로 아래에 pdf_extracted.json 파일을 만든다.
    output_path = EXTRACTED_TEXT_DIR / "pdf_extracted.json"

    # PDF 파일을 읽고 텍스트를 추출한다.
    # 반환값은 추출된 텍스트 record 목록이다.
    records = extract_pdf_files()

    # 추출된 record 목록을 JSON 파일로 저장한다.
    # 반환값 count는 실제 저장된 record 개수이다.
    count = write_jsonl(output_path, records)

    # 처리 결과를 화면에 요약 출력한다.
    print_record_summary("PDF 텍스트 추출 완료", count, output_path)


############################################################
# Python 실행 진입점
############################################################
# __name__
#   파이썬이 자동으로 제공하는 특수 변수이다.
#
# "__main__"
#   이 파일이 직접 실행될 때 __name__ 변수에 들어가는 값이다.
#
# 의미
#   아래 조건문은 이 파일이 직접 실행될 때만 main()을 호출한다.
#
# 예)
#   python 09_extract_pdf.py
#   이 경우:
#       __name__ == "__main__"
#       main() 실행됨
#
# 반대로 다른 파일에서 import 할 경우:
#   import 09_extract_pdf
#   이 경우:
#       __name__ == "09_extract_pdf"
#       main() 실행 안 됨
#
# 사용하는 이유
#   이 파일을 직접 실행할 때는 프로그램을 실행하고,
#   다른 파일에서 import 할 때는 함수만 재사용할 수 있게 하기 위해서이다.
############################################################
if __name__ == "__main__":
    main()
