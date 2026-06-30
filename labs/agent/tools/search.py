from __future__ import annotations

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
SAMPLE_DOCS_DIR = BASE_DIR / "sample_docs"


def search_documents(query: str) -> list[dict[str, str]]:
    """
    sample_docs 디렉터리의 Markdown 문서에서 검색어가 포함된 문서를 찾는다.

    Args:
        query:
            검색어.
            예: "Agent", "RAG", "Tool Calling"

    Returns:
        검색된 문서 목록.
        각 문서는 title, path, content를 가진 dictionary이다.

    Raises:
        ValueError:
            검색어가 비어 있는 경우 발생한다.
    """
    if not query or not query.strip():
        raise ValueError("검색어가 비어 있습니다.")

    normalized_query = query.lower()
    results: list[dict[str, str]] = []

    for path in sorted(SAMPLE_DOCS_DIR.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        title = path.stem

        if normalized_query in title.lower() or normalized_query in content.lower():
            preview = content.replace("\n", " ").strip()
            if len(preview) > 160:
                preview = preview[:160] + "..."

            results.append(
                {
                    "title": title,
                    "path": str(path.relative_to(BASE_DIR)),
                    "content": preview,
                }
            )

    return results
