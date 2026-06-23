"""
09_extract_pdf_vision.py

PDF 문서에서 페이지별 텍스트를 추출한다.

추출 방식:
1. pypdf로 PDF 내부 일반 텍스트 추출
2. PyMuPDF로 PDF 페이지를 PNG 이미지로 렌더링
3. Ollama Vision LLM으로 이미지 속 텍스트, 표, 차트, 도식 설명 추출
4. 일반 텍스트와 Vision 결과를 병합하여 JSONL 저장

입력:
- enterprise_docs/pdf/*.pdf

출력:
- extracted_text/pdf_vision_extracted.jsonl
- rendered_pages/pdf/<PDF파일명>/page_001.png

실행:
python 11_extract_pdf_vision.py
"""

from __future__ import annotations

import base64
import json
import urllib.error
import urllib.request
from pathlib import Path

import fitz
from pypdf import PdfReader

from step2_5_config import (
    ENTERPRISE_DOCS_DIR,
    EXTRACTED_TEXT_DIR,
    ensure_directories,
)
from step2_5_utils import (
    clean_text,
    find_files,
    stable_id,
    write_jsonl,
    print_record_summary,
)


# ============================================================
# Vision LLM 설정
# ============================================================

# 이 파이썬 코드는 Windows PC에서 실행하므로 localhost를 사용한다.
OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"

# Vision 기능을 지원하는 Ollama 모델명으로 설정
# 예: gemma3:4b
VISION_MODEL_NAME = "gemma3:4b"

# Vision LLM 사용 여부
USE_VISION_LLM = True

# True:
# pypdf로 일반 텍스트가 추출되지 않는 페이지에만 Vision LLM 실행
# 스캔 PDF 중심으로 빠르게 처리할 때 사용
#
# False:
# 모든 PDF 페이지를 PNG로 렌더링하고 Vision LLM 실행
# 표, 차트, 이미지, 도식 분석까지 모두 수행
# 처리 시간과 PC 자원 사용량이 증가함
VISION_ONLY_WHEN_NATIVE_TEXT_EMPTY = True

# PDF 페이지 PNG 렌더링 해상도
# 성능이 낮으면 120~150
# 작은 표, 차트 글씨가 많으면 180~200
RENDER_DPI = 150

# PDF 페이지 이미지 저장 경로
RENDERED_PDF_DIR = EXTRACTED_TEXT_DIR.parent / "rendered_pages" / "pdf"


# ============================================================
# Vision LLM 응답 JSON 형식
# ============================================================

VISION_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "visible_text": {
            "type": "string",
            "description": "이미지에서 읽을 수 있는 텍스트",
        },
        "visual_summary": {
            "type": "string",
            "description": "표, 차트, 도식, 프로세스 흐름 설명",
        },
        "chart_summary": {
            "type": "string",
            "description": "차트가 있을 경우 사실 기반의 추세와 비교 설명",
        },
    },
    "required": [
        "visible_text",
        "visual_summary",
        "chart_summary",
    ],
}


def ensure_vision_directories() -> None:
    """출력 폴더를 생성한다."""
    ensure_directories()
    RENDERED_PDF_DIR.mkdir(parents=True, exist_ok=True)


def render_pdf_page_to_png(
    pdf_path: Path,
    page_no: int,
    page,
) -> Path:
    """PDF 한 페이지를 PNG 이미지로 렌더링한다."""

    output_dir = RENDERED_PDF_DIR / pdf_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    image_path = output_dir / f"page_{page_no:03d}.png"

    pixmap = page.get_pixmap(
        dpi=RENDER_DPI,
        alpha=False,
    )

    pixmap.save(str(image_path))

    return image_path


def image_to_base64(image_path: Path) -> str:
    """PNG 파일을 Ollama API 전송용 Base64 문자열로 변환한다."""

    image_bytes = image_path.read_bytes()

    return base64.b64encode(image_bytes).decode("utf-8")


def parse_vision_json(content: str) -> dict[str, str]:
    """Vision LLM 응답을 안전하게 JSON으로 변환한다."""

    content = content.strip()

    # 모델이 ```json ... ``` 형태로 응답한 경우를 대비
    if content.startswith("```json"):
        content = content.removeprefix("```json").strip()

    if content.startswith("```"):
        content = content.removeprefix("```").strip()

    if content.endswith("```"):
        content = content.removesuffix("```").strip()

    try:
        result = json.loads(content)

        if not isinstance(result, dict):
            result = {}

    except json.JSONDecodeError:
        result = {}

    return {
        "visible_text": clean_text(str(result.get("visible_text", ""))),
        "visual_summary": clean_text(str(result.get("visual_summary", ""))),
        "chart_summary": clean_text(str(result.get("chart_summary", ""))),
    }


def extract_vision_text(image_path: Path) -> dict[str, str]:
    """PNG 이미지 한 장을 Ollama Vision LLM으로 분석한다."""

    prompt = """
이 이미지는 PDF 문서의 한 페이지입니다.

다음 규칙을 지켜서 분석하세요.

1. 이미지에서 읽을 수 있는 텍스트를 가능한 한 정확히 추출하세요.
2. 스캔된 문서, 이미지 안의 글자, 표 안의 글자,
   차트 축·범례·라벨을 우선적으로 확인하세요.
3. 표가 있으면 행과 열의 관계를 간단히 설명하세요.
4. 차트가 있으면 상승, 하락, 비교, 비중 등
   이미지에서 확인되는 사실만 설명하세요.
5. 도식이나 프로세스 흐름이 있으면
   화살표 방향과 단계 관계를 설명하세요.
6. 읽기 어려운 글자나 수치는 추측하지 마세요.
7. 반드시 지정된 JSON 형식으로만 응답하세요.
""".strip()

    image_base64 = image_to_base64(image_path)

    payload = {
        "model": VISION_MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "images": [image_base64],
            }
        ],
        "format": VISION_RESPONSE_SCHEMA,
        "stream": False,
        "options": {
            "temperature": 0,
        },
    }

    request = urllib.request.Request(
        OLLAMA_CHAT_URL,
        data=json.dumps(
            payload,
            ensure_ascii=False,
        ).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            response_text = response.read().decode("utf-8")

    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode(
            "utf-8",
            errors="replace",
        )

        raise RuntimeError(
            f"Ollama Vision API 호출 실패: HTTP {exc.code}\n"
            f"{error_body}"
        ) from exc

    except urllib.error.URLError as exc:
        raise RuntimeError(
            "Ollama 서버에 연결하지 못했습니다.\n"
            f"확인 주소: {OLLAMA_CHAT_URL}\n"
            f"상세 오류: {exc.reason}"
        ) from exc

    response_json = json.loads(response_text)

    if "error" in response_json:
        raise RuntimeError(
            f"Ollama Vision 처리 오류: {response_json['error']}"
        )

    content = response_json.get(
        "message",
        {},
    ).get(
        "content",
        "",
    )

    return parse_vision_json(content)


def build_rag_text(
    native_text: str,
    vision_result: dict[str, str],
) -> str:
    """일반 PDF 텍스트와 Vision 분석 결과를 RAG용 텍스트로 합친다."""

    parts: list[str] = []

    if native_text:
        parts.append(
            f"[PDF 원본 텍스트]\n{native_text}"
        )

    if vision_result["visible_text"]:
        parts.append(
            f"[이미지 기반 보조 텍스트]\n"
            f"{vision_result['visible_text']}"
        )

    if vision_result["visual_summary"]:
        parts.append(
            f"[시각 요소 설명]\n"
            f"{vision_result['visual_summary']}"
        )

    if vision_result["chart_summary"]:
        parts.append(
            f"[차트 설명]\n"
            f"{vision_result['chart_summary']}"
        )

    return clean_text("\n\n".join(parts))


def extract_pdf_files() -> list[dict]:
    """PDF 파일별 페이지 텍스트와 Vision 분석 결과를 추출한다."""

    ensure_vision_directories()

    pdf_dir = ENTERPRISE_DOCS_DIR / "pdf"
    pdf_files = find_files(pdf_dir, (".pdf",))

    records: list[dict] = []

    for pdf_path in pdf_files:
        try:
            # 일반 텍스트 추출용
            reader = PdfReader(str(pdf_path))

            # PDF 페이지 PNG 렌더링용
            vision_document = fitz.open(str(pdf_path))

        except Exception as exc:
            print(f"[PDF 읽기 실패] {pdf_path.name}: {exc}")
            continue

        try:
            for page_no, page in enumerate(reader.pages, start=1):
                # ------------------------------------------------
                # 1. pypdf 기반 일반 텍스트 추출
                # ------------------------------------------------
                try:
                    native_text = page.extract_text() or ""

                except Exception as exc:
                    print(
                        f"[PDF 텍스트 추출 실패] "
                        f"{pdf_path.name} page={page_no}: {exc}"
                    )
                    native_text = ""

                native_text = clean_text(native_text)

                # ------------------------------------------------
                # 2. Vision LLM 적용 여부 결정
                # ------------------------------------------------
                should_use_vision = (
                    USE_VISION_LLM
                    and (
                        not VISION_ONLY_WHEN_NATIVE_TEXT_EMPTY
                        or not native_text
                    )
                )

                image_path = None
                vision_error = ""

                vision_result = {
                    "visible_text": "",
                    "visual_summary": "",
                    "chart_summary": "",
                }

                # ------------------------------------------------
                # 3. PDF 페이지 → PNG → Vision LLM 분석
                # ------------------------------------------------
                if should_use_vision:
                    try:
                        vision_page = vision_document.load_page(
                            page_no - 1
                        )

                        image_path = render_pdf_page_to_png(
                            pdf_path=pdf_path,
                            page_no=page_no,
                            page=vision_page,
                        )

                        print(
                            f"[Vision 분석] "
                            f"{pdf_path.name} page={page_no}"
                        )

                        vision_result = extract_vision_text(
                            image_path
                        )

                    except Exception as exc:
                        vision_error = str(exc)

                        print(
                            f"[Vision 분석 실패] "
                            f"{pdf_path.name} page={page_no}: {exc}"
                        )

                # ------------------------------------------------
                # 4. 일반 텍스트 + Vision 결과 병합
                # ------------------------------------------------
                rag_text = build_rag_text(
                    native_text=native_text,
                    vision_result=vision_result,
                )

                # 일반 텍스트도 없고 Vision 결과도 없으면 저장하지 않음
                if not rag_text:
                    continue

                records.append(
                    {
                        "id": stable_id(
                            pdf_path.name,
                            "pdf_vision",
                            page_no,
                        ),
                        "text": rag_text,
                        "native_text": native_text,
                        "vision_text": vision_result["visible_text"],
                        "visual_summary": vision_result["visual_summary"],
                        "chart_summary": vision_result["chart_summary"],
                        "metadata": {
                            "file_name": pdf_path.name,
                            "document_type": "pdf",
                            "page_no": page_no,
                            "source_path": str(pdf_path),
                            "page_image_path": (
                                str(image_path)
                                if image_path
                                else ""
                            ),
                            "extractor": (
                                "pypdf + pymupdf + ollama-vision"
                                if should_use_vision
                                else "pypdf"
                            ),
                            "vision_model": (
                                VISION_MODEL_NAME
                                if should_use_vision
                                else ""
                            ),
                            "vision_error": vision_error,
                        },
                    }
                )

        finally:
            vision_document.close()

    return records


def main() -> None:
    output_path = (
        EXTRACTED_TEXT_DIR
        / "pdf_vision_extracted.jsonl"
    )

    records = extract_pdf_files()

    count = write_jsonl(
        output_path,
        records,
    )

    print_record_summary(
        "PDF 텍스트 + Vision LLM 추출 완료",
        count,
        output_path,
    )


if __name__ == "__main__":
    main()