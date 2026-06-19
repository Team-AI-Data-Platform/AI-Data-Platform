# Step2-5A. 실전 사내 문서 RAG 실습파일

이 실습파일은 AI-Data-Platform `Step2-5A. 문서 전처리 파이프라인` 가이드와 함께 사용하는 Python 실습 코드입니다.

## 1. 실습 목표

사내 문서를 다음 흐름으로 처리합니다.

```text
PDF / PPTX / DOCX / XLSX / MD / TXT
   ↓
문서 유형별 텍스트 추출
   ↓
JSONL 추출 결과 생성
   ↓
Chunk 생성
   ↓
Embedding
   ↓
ChromaDB 저장
   ↓
질문 검색
   ↓
Ollama 기반 RAG 답변 생성
```

## 2. 실행 위치

압축을 풀고 프로젝트 루트에서 아래 위치로 이동합니다.

```bash
cd labs/rag
```

## 3. 가상환경 생성

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows는 다음을 사용합니다.

```bash
.venv\Scripts\activate
```

## 4. 라이브러리 설치

```bash
pip install -r requirements.txt
```

## 5. 실습 문서 배치

문서를 아래 폴더에 넣습니다.

```text
enterprise_docs/
 ├─ pdf/
 ├─ pptx/
 ├─ docx/
 ├─ xlsx/
 ├─ md/
 └─ txt/
```

처음 실행을 쉽게 하기 위해 샘플 `.md`, `.txt` 문서를 포함했습니다.

## 6. 실행 순서

```bash
python 09_extract_pdf.py
python 10_extract_pptx.py
python 11_extract_docx.py
python 12_extract_xlsx.py
python 13_build_enterprise_chunks.py
python 14_insert_enterprise_docs_to_chroma.py
python 15_enterprise_rag_search.py "전자금융 장애 대응 절차를 알려줘"
```

## 7. Ollama 사용

`15_enterprise_rag_search.py`는 Ollama가 실행 중이면 LLM 답변을 생성합니다.

```bash
ollama serve
ollama pull llama3.1:8b
```

Ollama가 실행되지 않아도 검색 결과는 출력되도록 구성되어 있습니다.

## 8. 생성되는 결과

```text
extracted_text/
 ├─ pdf_extracted.jsonl
 ├─ pptx_extracted.jsonl
 ├─ docx_extracted.jsonl
 ├─ xlsx_extracted.jsonl
 └─ text_extracted.jsonl

enterprise_chunks/
 └─ enterprise_chunks.jsonl

chroma_db/
 └─ ChromaDB 저장 데이터
```

## 9. GitHub 업로드 시 주의사항

실제 사내 문서를 GitHub Public Repository에 올리면 안 됩니다.

다음 정보는 반드시 제거하거나 샘플로 대체합니다.

```text
고객사명
계약금액
제안 전략
인력 정보
개인정보
내부 시스템 구성 정보
보안 정보
```
