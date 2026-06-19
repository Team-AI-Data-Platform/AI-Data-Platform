# Step2-5A. 문서 전처리 파이프라인 구축 가이드

> PDF, PPTX, DOCX, XLSX 문서를 Python으로 추출하고 Chunking, Embedding, ChromaDB 저장, RAG 검색까지 수행하는 실습 문서

---

## 1. 문서 작성 목적

이 문서는 Step2-5의 하위 실습인 **Step2-5A. 문서 전처리 파이프라인**을 설명한다.

Step2-5A의 목적은 Open WebUI 같은 도구를 사용하기 전에, RAG 내부에서 실제로 어떤 일이 일어나는지 Python 코드로 직접 확인하는 것이다. 기업 문서 RAG의 품질은 단순히 LLM 성능만으로 결정되지 않는다. 문서를 어떻게 읽고, 어떤 기준으로 나누고, 어떤 Metadata를 붙이고, 어떤 Vector DB에 저장하는지가 검색 품질과 답변 신뢰도를 크게 좌우한다.

따라서 이 실습에서는 다음 흐름을 직접 구현한다.

```text
사내 문서 파일
   ↓
문서 유형별 텍스트 추출
   ↓
JSONL 추출 결과 저장
   ↓
Chunk 생성
   ↓
Embedding 생성
   ↓
ChromaDB 저장
   ↓
질문 기반 유사 문서 검색
   ↓
Ollama 기반 RAG 답변 생성
```

---

## 2. 이 실습에서 다루는 문서 유형

이번 실습에서는 다음 문서 유형을 대상으로 한다.

| 문서 유형 | 처리 방식 | 실습 파일 |
|---|---|---|
| PDF | 페이지별 텍스트 추출 | `09_extract_pdf.py` |
| PPTX | 슬라이드별 텍스트 추출 | `10_extract_pptx.py` |
| DOCX | 문단, 제목, 표 추출 | `11_extract_docx.py` |
| XLSX | Sheet, Row 단위 텍스트 변환 | `12_extract_xlsx.py` |

HWP, 이미지, 스캔 PDF는 실무에서 중요하지만 초기 실습 난이도가 높다. 따라서 이번 단계에서는 직접 처리하지 않고, HWP는 PDF 또는 DOCX로 변환한 뒤 처리하고, 스캔 문서는 OCR이 필요하다는 개념 수준으로 다룬다.

---

## 3. 권장 디렉터리 구조

프로젝트 루트 기준으로 다음 구조를 사용한다.

```text
AI-Data-Platform/

├─ docs/
│  └─ study/
│     └─ step2/
│        ├─ step2_5_enterprise_document_rag_guide.md
│        ├─ step2_5a_enterprise_ingestion_guide.md
│        └─ step2_5b_openwebui_enterprise_knowledge_guide.md
│
├─ labs/
│  └─ rag/
│     ├─ enterprise_docs/
│     │  ├─ pdf/
│     │  ├─ pptx/
│     │  ├─ docx/
│     │  ├─ xlsx/
│     │  └─ hwp/
│     │
│     ├─ extracted_text/
│     │  ├─ pdf/
│     │  ├─ pptx/
│     │  ├─ docx/
│     │  └─ xlsx/
│     │
│     ├─ chroma_db/
│     │
│     ├─ requirements.txt
│     ├─ common_enterprise_rag.py
│     ├─ 09_extract_pdf.py
│     ├─ 10_extract_pptx.py
│     ├─ 11_extract_docx.py
│     ├─ 12_extract_xlsx.py
│     ├─ 13_build_enterprise_chunks.py
│     ├─ 14_insert_enterprise_docs_to_chroma.py
│     └─ 15_enterprise_rag_search.py
```

---

## 4. 실습 파일 역할

| 파일명 | 역할 |
|---|---|
| `requirements.txt` | 필요한 Python 라이브러리 목록 |
| `common_enterprise_rag.py` | 공통 경로, JSONL 처리, 텍스트 정제, Chunk 분할 함수 |
| `09_extract_pdf.py` | PDF 페이지별 텍스트 추출 |
| `10_extract_pptx.py` | PPTX 슬라이드별 텍스트 추출 |
| `11_extract_docx.py` | DOCX 제목, 문단, 표 텍스트 추출 |
| `12_extract_xlsx.py` | XLSX Sheet, Row 데이터를 텍스트로 변환 |
| `13_build_enterprise_chunks.py` | 추출 결과를 Chunk 단위로 변환 |
| `14_insert_enterprise_docs_to_chroma.py` | Chunk를 Embedding하여 ChromaDB에 저장 |
| `15_enterprise_rag_search.py` | 질문 기반 검색 및 Ollama RAG 답변 생성 |

---

## 5. 실행 준비

### 5.1 실습 위치로 이동

```bash
cd AI-Data-Platform/labs/rag
```

### 5.2 Python 가상환경 생성

macOS 또는 Linux에서는 다음 명령을 사용한다.

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows에서는 다음 명령을 사용한다.

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 5.3 라이브러리 설치

```bash
pip install -r requirements.txt
```

---

## 6. 실습 문서 준비

문서 유형별 폴더에 테스트 문서를 넣는다.

```text
labs/rag/enterprise_docs/pdf/     → PDF 파일
labs/rag/enterprise_docs/pptx/    → PPTX 파일
labs/rag/enterprise_docs/docx/    → DOCX 파일
labs/rag/enterprise_docs/xlsx/    → XLSX 파일
```

처음에는 보안 문서가 아닌 샘플 문서를 사용하는 것이 좋다. 실제 고객사 제안서, RFP, 설계서, 개인정보 포함 문서는 Public GitHub에 올리면 안 된다.

---

## 7. 실행 순서

### 7.1 문서 유형별 텍스트 추출

```bash
python 09_extract_pdf.py
python 10_extract_pptx.py
python 11_extract_docx.py
python 12_extract_xlsx.py
```

실행 후 다음 위치에 JSONL 파일이 생성된다.

```text
extracted_text/pdf/pdf_extracted.jsonl
extracted_text/pptx/pptx_extracted.jsonl
extracted_text/docx/docx_extracted.jsonl
extracted_text/xlsx/xlsx_extracted.jsonl
```

### 7.2 Chunk 생성

```bash
python 13_build_enterprise_chunks.py
```

결과 파일은 다음 위치에 생성된다.

```text
enterprise_chunks.jsonl
```

만약 입력 문서가 하나도 없으면 실습이 중단되지 않도록 샘플 Chunk 1건을 자동 생성한다. 이 처리는 처음 실행하는 사용자가 에러 없이 전체 흐름을 확인할 수 있도록 하기 위한 장치이다.

### 7.3 ChromaDB 저장

```bash
python 14_insert_enterprise_docs_to_chroma.py
```

이 단계에서는 `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` 모델을 사용하여 Chunk를 Embedding하고 ChromaDB에 저장한다.

### 7.4 RAG 검색 및 답변 생성

```bash
python 15_enterprise_rag_search.py "전자금융 장애 대응 절차를 알려줘"
```

Ollama가 실행 중이고 `llama3.1:8b` 모델이 준비되어 있으면 검색 결과를 기반으로 답변까지 생성한다. Ollama가 실행 중이 아니면 답변 생성은 실패할 수 있지만, 검색 결과는 정상적으로 확인할 수 있다.

---

## 8. 실행 결과 이해

검색 결과에는 다음 정보가 출력된다.

```text
파일명
문서 유형
페이지 번호
슬라이드 번호
시트명
행 번호
검색된 Chunk 내용
거리 값
```

거리 값은 검색 유사도 판단에 사용된다. ChromaDB에서 cosine 기반 검색을 사용하므로 값이 작을수록 더 유사한 결과로 이해하면 된다.

---

## 9. 설계 포인트

### 9.1 JSONL을 중간 산출물로 사용하는 이유

각 문서 Parser가 추출한 결과를 바로 Vector DB에 넣지 않고 JSONL로 저장하는 이유는 다음과 같다.

```text
1. 추출 결과를 사람이 직접 확인할 수 있다.
2. Parser 오류를 추적하기 쉽다.
3. Chunking 전략을 여러 번 바꿔가며 재실행할 수 있다.
4. 문서 추출 단계와 Vector DB 저장 단계를 분리할 수 있다.
5. 나중에 Airflow, Dagster, 배치 프로그램으로 확장하기 쉽다.
```

### 9.2 Metadata를 함께 저장하는 이유

RAG 답변은 반드시 근거를 추적할 수 있어야 한다. PDF는 페이지 번호, PPTX는 슬라이드 번호, XLSX는 시트명과 행 번호가 있어야 사용자가 원본 문서로 돌아가 검증할 수 있다.

### 9.3 문서별 Chunk 기준이 다른 이유

모든 문서를 같은 기준으로 자르면 검색 품질이 떨어진다. PPTX는 슬라이드 단위, XLSX는 Row 단위, PDF는 페이지 단위, DOCX는 Heading과 문단 단위를 고려해야 한다.

---

## 10. 전체 실습 코드

아래는 Step2-5A 실습에 필요한 전체 파일 내용이다. 문서를 GitHub에 올릴 때 이 내용을 함께 포함하면, 학습자가 별도 파일을 열지 않아도 실습 코드를 확인할 수 있다.

### requirements.txt

```text
chromadb==0.5.23
sentence-transformers==3.3.1
pypdf==5.1.0
python-pptx==1.0.2
python-docx==1.1.2
openpyxl==3.1.5
requests==2.32.3
```

### common_enterprise_rag.py

```python
from __future__ import annotations

import json
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "enterprise_docs"
EXTRACTED_DIR = BASE_DIR / "extracted_text"
CHROMA_DIR = BASE_DIR / "chroma_db"
CHUNKS_PATH = BASE_DIR / "enterprise_chunks.jsonl"
COLLECTION_NAME = "enterprise_docs"
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def ensure_dirs() -> None:
    for path in [
        DOCS_DIR / "pdf",
        DOCS_DIR / "pptx",
        DOCS_DIR / "docx",
        DOCS_DIR / "xlsx",
        DOCS_DIR / "hwp",
        EXTRACTED_DIR / "pdf",
        EXTRACTED_DIR / "pptx",
        EXTRACTED_DIR / "docx",
        EXTRACTED_DIR / "xlsx",
        CHROMA_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def clean_text(text: str | None) -> str:
    if not text:
        return ""
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def stable_id(*parts: Any) -> str:
    key = "|".join(str(p) for p in parts)
    return str(uuid.uuid5(uuid.NAMESPACE_URL, key))


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def split_text(text: str, chunk_size: int = 800, overlap: int = 120) -> list[str]:
    text = clean_text(text)
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        piece = text[start:end]
        if end < len(text):
            cut = max(piece.rfind("\n"), piece.rfind(". "), piece.rfind("다. "))
            if cut > chunk_size * 0.5:
                end = start + cut + 1
                piece = text[start:end]
        piece = clean_text(piece)
        if piece:
            chunks.append(piece)
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
    return chunks
```

### 09_extract_pdf.py

```python
from pathlib import Path
from pypdf import PdfReader
from common_enterprise_rag import DOCS_DIR, EXTRACTED_DIR, clean_text, ensure_dirs, now_iso, stable_id, write_jsonl


def extract_pdf_file(pdf_path: Path) -> list[dict]:
    rows = []
    reader = PdfReader(str(pdf_path))
    for page_no, page in enumerate(reader.pages, start=1):
        text = clean_text(page.extract_text())
        if not text:
            continue
        rows.append({
            "id": stable_id(pdf_path.name, "pdf", page_no),
            "file_name": pdf_path.name,
            "source_path": str(pdf_path),
            "document_type": "pdf",
            "page_no": page_no,
            "text": text,
            "extracted_at": now_iso(),
        })
    return rows


def main() -> None:
    ensure_dirs()
    input_dir = DOCS_DIR / "pdf"
    output_path = EXTRACTED_DIR / "pdf" / "pdf_extracted.jsonl"
    all_rows = []
    for pdf_path in sorted(input_dir.glob("*.pdf")):
        try:
            all_rows.extend(extract_pdf_file(pdf_path))
        except Exception as e:
            print(f"[WARN] PDF 추출 실패: {pdf_path.name} / {e}")
    write_jsonl(output_path, all_rows)
    print(f"PDF 추출 완료: {len(all_rows)}건 -> {output_path}")
    if not all_rows:
        print(f"PDF 파일이 없거나 텍스트가 없습니다. 파일을 넣을 위치: {input_dir}")


if __name__ == "__main__":
    main()
```

### 10_extract_pptx.py

```python
from pathlib import Path
from pptx import Presentation
from common_enterprise_rag import DOCS_DIR, EXTRACTED_DIR, clean_text, ensure_dirs, now_iso, stable_id, write_jsonl


def shape_texts(shape) -> list[str]:
    texts = []
    if hasattr(shape, "text"):
        text = clean_text(shape.text)
        if text:
            texts.append(text)
    if getattr(shape, "has_table", False):
        for row in shape.table.rows:
            cells = [clean_text(cell.text) for cell in row.cells if clean_text(cell.text)]
            if cells:
                texts.append(" | ".join(cells))
    return texts


def extract_pptx_file(pptx_path: Path) -> list[dict]:
    rows = []
    presentation = Presentation(str(pptx_path))
    for slide_no, slide in enumerate(presentation.slides, start=1):
        texts = []
        for shape in slide.shapes:
            texts.extend(shape_texts(shape))
        text = clean_text("\n".join(texts))
        if not text:
            continue
        rows.append({
            "id": stable_id(pptx_path.name, "pptx", slide_no),
            "file_name": pptx_path.name,
            "source_path": str(pptx_path),
            "document_type": "pptx",
            "slide_no": slide_no,
            "text": text,
            "extracted_at": now_iso(),
        })
    return rows


def main() -> None:
    ensure_dirs()
    input_dir = DOCS_DIR / "pptx"
    output_path = EXTRACTED_DIR / "pptx" / "pptx_extracted.jsonl"
    all_rows = []
    for pptx_path in sorted(input_dir.glob("*.pptx")):
        try:
            all_rows.extend(extract_pptx_file(pptx_path))
        except Exception as e:
            print(f"[WARN] PPTX 추출 실패: {pptx_path.name} / {e}")
    write_jsonl(output_path, all_rows)
    print(f"PPTX 추출 완료: {len(all_rows)}건 -> {output_path}")
    if not all_rows:
        print(f"PPTX 파일이 없거나 텍스트가 없습니다. 파일을 넣을 위치: {input_dir}")


if __name__ == "__main__":
    main()
```

### 11_extract_docx.py

```python
from pathlib import Path
from docx import Document
from common_enterprise_rag import DOCS_DIR, EXTRACTED_DIR, clean_text, ensure_dirs, now_iso, stable_id, write_jsonl


def extract_docx_file(docx_path: Path) -> list[dict]:
    rows = []
    document = Document(str(docx_path))
    section = ""
    buffer = []
    part_no = 0

    def flush():
        nonlocal buffer, part_no
        text = clean_text("\n".join(buffer))
        if text:
            part_no += 1
            rows.append({
                "id": stable_id(docx_path.name, "docx", part_no),
                "file_name": docx_path.name,
                "source_path": str(docx_path),
                "document_type": "docx",
                "section": section,
                "part_no": part_no,
                "text": text,
                "extracted_at": now_iso(),
            })
        buffer = []

    for paragraph in document.paragraphs:
        text = clean_text(paragraph.text)
        if not text:
            continue
        style_name = paragraph.style.name if paragraph.style else ""
        if style_name.lower().startswith("heading") or style_name.startswith("제목"):
            flush()
            section = text
        buffer.append(text)
    flush()

    for table_no, table in enumerate(document.tables, start=1):
        table_lines = []
        for row in table.rows:
            cells = [clean_text(cell.text) for cell in row.cells if clean_text(cell.text)]
            if cells:
                table_lines.append(" | ".join(cells))
        table_text = clean_text("\n".join(table_lines))
        if table_text:
            rows.append({
                "id": stable_id(docx_path.name, "docx_table", table_no),
                "file_name": docx_path.name,
                "source_path": str(docx_path),
                "document_type": "docx",
                "section": f"table_{table_no}",
                "table_no": table_no,
                "text": table_text,
                "extracted_at": now_iso(),
            })
    return rows


def main() -> None:
    ensure_dirs()
    input_dir = DOCS_DIR / "docx"
    output_path = EXTRACTED_DIR / "docx" / "docx_extracted.jsonl"
    all_rows = []
    for docx_path in sorted(input_dir.glob("*.docx")):
        try:
            all_rows.extend(extract_docx_file(docx_path))
        except Exception as e:
            print(f"[WARN] DOCX 추출 실패: {docx_path.name} / {e}")
    write_jsonl(output_path, all_rows)
    print(f"DOCX 추출 완료: {len(all_rows)}건 -> {output_path}")
    if not all_rows:
        print(f"DOCX 파일이 없거나 텍스트가 없습니다. 파일을 넣을 위치: {input_dir}")


if __name__ == "__main__":
    main()
```

### 12_extract_xlsx.py

```python
from pathlib import Path
from openpyxl import load_workbook
from common_enterprise_rag import DOCS_DIR, EXTRACTED_DIR, clean_text, ensure_dirs, now_iso, stable_id, write_jsonl


def value_to_text(value) -> str:
    if value is None:
        return ""
    return clean_text(str(value))


def extract_xlsx_file(xlsx_path: Path) -> list[dict]:
    rows = []
    workbook = load_workbook(str(xlsx_path), data_only=True, read_only=True)
    for sheet in workbook.worksheets:
        all_rows = list(sheet.iter_rows(values_only=True))
        if not all_rows:
            continue
        headers = [value_to_text(v) or f"column_{idx}" for idx, v in enumerate(all_rows[0], start=1)]
        for row_no, row in enumerate(all_rows[1:], start=2):
            pairs = []
            for header, value in zip(headers, row):
                value_text = value_to_text(value)
                if value_text:
                    pairs.append(f"{header}: {value_text}")
            text = clean_text(", ".join(pairs))
            if not text:
                continue
            rows.append({
                "id": stable_id(xlsx_path.name, sheet.title, row_no),
                "file_name": xlsx_path.name,
                "source_path": str(xlsx_path),
                "document_type": "xlsx",
                "sheet_name": sheet.title,
                "row_no": row_no,
                "text": text,
                "extracted_at": now_iso(),
            })
    return rows


def main() -> None:
    ensure_dirs()
    input_dir = DOCS_DIR / "xlsx"
    output_path = EXTRACTED_DIR / "xlsx" / "xlsx_extracted.jsonl"
    all_rows = []
    for xlsx_path in sorted(input_dir.glob("*.xlsx")):
        try:
            all_rows.extend(extract_xlsx_file(xlsx_path))
        except Exception as e:
            print(f"[WARN] XLSX 추출 실패: {xlsx_path.name} / {e}")
    write_jsonl(output_path, all_rows)
    print(f"XLSX 추출 완료: {len(all_rows)}건 -> {output_path}")
    if not all_rows:
        print(f"XLSX 파일이 없거나 데이터가 없습니다. 파일을 넣을 위치: {input_dir}")


if __name__ == "__main__":
    main()
```

### 13_build_enterprise_chunks.py

```python
from pathlib import Path
from common_enterprise_rag import EXTRACTED_DIR, CHUNKS_PATH, clean_text, ensure_dirs, read_jsonl, split_text, stable_id, write_jsonl


def main() -> None:
    ensure_dirs()
    extracted_files = [
        EXTRACTED_DIR / "pdf" / "pdf_extracted.jsonl",
        EXTRACTED_DIR / "pptx" / "pptx_extracted.jsonl",
        EXTRACTED_DIR / "docx" / "docx_extracted.jsonl",
        EXTRACTED_DIR / "xlsx" / "xlsx_extracted.jsonl",
    ]

    chunks = []
    for extracted_file in extracted_files:
        for row in read_jsonl(extracted_file):
            text = clean_text(row.get("text", ""))
            if not text:
                continue
            for chunk_index, chunk_text in enumerate(split_text(text), start=1):
                metadata = {k: v for k, v in row.items() if k not in ["id", "text"] and v not in [None, ""]}
                metadata["chunk_index"] = chunk_index
                chunks.append({
                    "id": stable_id(row.get("id"), "chunk", chunk_index),
                    "text": chunk_text,
                    "metadata": metadata,
                })

    if not chunks:
        sample_text = "전자금융 장애 발생 시에는 거래 오류 로그, 대외계 연계 상태, 네트워크 연결, 배치 처리 결과를 우선 확인한다. 장애 영향도를 파악한 뒤 담당자에게 전파하고 복구 절차를 수행한다."
        chunks.append({
            "id": stable_id("sample", "enterprise", 1),
            "text": sample_text,
            "metadata": {
                "file_name": "sample_enterprise_document.txt",
                "document_type": "sample",
                "section": "전자금융 장애 대응",
                "chunk_index": 1,
                "source_path": "generated_sample",
            },
        })
        print("추출된 문서가 없어 샘플 Chunk 1건을 생성했습니다.")

    write_jsonl(CHUNKS_PATH, chunks)
    print(f"Chunk 생성 완료: {len(chunks)}건 -> {CHUNKS_PATH}")


if __name__ == "__main__":
    main()
```

### 14_insert_enterprise_docs_to_chroma.py

```python
import chromadb
from sentence_transformers import SentenceTransformer
from common_enterprise_rag import CHROMA_DIR, CHUNKS_PATH, COLLECTION_NAME, MODEL_NAME, ensure_dirs, read_jsonl


def main() -> None:
    ensure_dirs()
    chunks = read_jsonl(CHUNKS_PATH)
    if not chunks:
        raise RuntimeError("enterprise_chunks.jsonl 파일이 비어 있습니다. 먼저 13_build_enterprise_chunks.py를 실행하세요.")

    print(f"임베딩 모델 로딩: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)
    documents = [row["text"] for row in chunks]
    ids = [row["id"] for row in chunks]
    metadatas = [row["metadata"] for row in chunks]
    embeddings = model.encode(documents, normalize_embeddings=True).tolist()

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection(name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"})

    # 재실행해도 동일 ID는 upsert로 갱신되도록 처리한다.
    collection.upsert(ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings)
    print(f"ChromaDB 저장 완료: {collection.count()}건 / collection={COLLECTION_NAME} / path={CHROMA_DIR}")


if __name__ == "__main__":
    main()
```

### 15_enterprise_rag_search.py

```python
import sys
import requests
import chromadb
from sentence_transformers import SentenceTransformer
from common_enterprise_rag import CHROMA_DIR, COLLECTION_NAME, MODEL_NAME, ensure_dirs

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.1:8b"


def search_documents(query: str, top_k: int = 5) -> list[dict]:
    ensure_dirs()
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection(name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"})
    if collection.count() == 0:
        raise RuntimeError("ChromaDB에 저장된 문서가 없습니다. 먼저 14_insert_enterprise_docs_to_chroma.py를 실행하세요.")

    model = SentenceTransformer(MODEL_NAME)
    query_embedding = model.encode([query], normalize_embeddings=True).tolist()[0]
    result = collection.query(query_embeddings=[query_embedding], n_results=top_k, include=["documents", "metadatas", "distances"])

    rows = []
    for i, document in enumerate(result["documents"][0]):
        rows.append({
            "rank": i + 1,
            "document": document,
            "metadata": result["metadatas"][0][i],
            "distance": result["distances"][0][i],
        })
    return rows


def build_prompt(query: str, rows: list[dict]) -> str:
    contexts = []
    for row in rows:
        meta = row["metadata"]
        source = f"파일명={meta.get('file_name', '')}, 유형={meta.get('document_type', '')}, 페이지={meta.get('page_no', '')}, 슬라이드={meta.get('slide_no', '')}, 시트={meta.get('sheet_name', '')}, 행={meta.get('row_no', '')}, 섹션={meta.get('section', '')}"
        contexts.append(f"[근거 {row['rank']}] {source}\n{row['document']}")
    context_text = "\n\n".join(contexts)
    return f"""너는 사내 문서 기반 RAG 어시스턴트다.
아래 근거 문서만 사용해서 답변해라.
근거가 부족하면 부족하다고 말해라.
답변 마지막에는 참고한 파일명과 위치를 요약해라.

[사용자 질문]
{query}

[근거 문서]
{context_text}

[답변]
"""


def generate_with_ollama(prompt: str) -> str | None:
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=60,
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        print(f"[WARN] Ollama 답변 생성 실패: {e}")
        print("[INFO] Ollama가 실행 중이 아니면 `ollama serve` 또는 Open WebUI/Ollama 상태를 확인하세요.")
        return None


def print_search_results(rows: list[dict]) -> None:
    print("\n=== 검색 결과 ===")
    for row in rows:
        meta = row["metadata"]
        print(f"\n[{row['rank']}] distance={row['distance']:.4f}")
        print(f"파일명: {meta.get('file_name')}")
        print(f"유형: {meta.get('document_type')}")
        if meta.get("page_no"):
            print(f"페이지: {meta.get('page_no')}")
        if meta.get("slide_no"):
            print(f"슬라이드: {meta.get('slide_no')}")
        if meta.get("sheet_name"):
            print(f"시트/행: {meta.get('sheet_name')} / {meta.get('row_no')}")
        print(row["document"][:500])


def main() -> None:
    query = " ".join(sys.argv[1:]).strip() or "전자금융 장애 대응 절차를 알려줘"
    rows = search_documents(query)
    print_search_results(rows)

    prompt = build_prompt(query, rows)
    answer = generate_with_ollama(prompt)
    print("\n=== RAG 답변 ===")
    if answer:
        print(answer)
    else:
        print("Ollama 답변 생성은 실패했지만, 위 검색 결과를 통해 RAG 검색은 정상 동작했습니다.")


if __name__ == "__main__":
    main()
```


---

## 11. 완료 기준

다음 조건을 만족하면 Step2-5A 실습을 완료한 것으로 판단한다.

```text
1. requirements.txt 설치가 완료되었다.
2. PDF, PPTX, DOCX, XLSX 중 하나 이상의 문서를 enterprise_docs 하위에 배치했다.
3. 09~12 추출 스크립트를 실행했다.
4. extracted_text 하위에 JSONL 결과가 생성되었다.
5. 13번 스크립트로 enterprise_chunks.jsonl이 생성되었다.
6. 14번 스크립트로 ChromaDB에 Chunk가 저장되었다.
7. 15번 스크립트로 질문 검색 결과가 출력되었다.
8. Ollama가 실행 중인 경우 RAG 답변까지 생성되었다.
```

---

## 12. 다음 단계

Step2-5A를 완료한 뒤에는 Step2-5B로 이동한다. Step2-5B에서는 Open WebUI Knowledge 기능을 사용하여 사용자가 웹 화면에서 문서를 업로드하고 질문하는 과정을 실습한다.

Step2-5A가 내부 파이프라인 이해라면, Step2-5B는 실제 사용자 활용 방식 이해에 해당한다.
