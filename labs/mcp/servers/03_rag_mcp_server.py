from pathlib import Path

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("rag-mcp-server")

BASE_DIR = Path(__file__).resolve().parents[1]
SAMPLE_DOCS_DIR = BASE_DIR / "sample_docs"


@mcp.tool()
def search_docs(query: str, top_k: int = 3) -> list[dict[str, str]]:
    """
    sample_docs Markdown 문서에서 query가 포함된 문서를 검색한다.

    실제 운영 RAG에서는 이 부분을 Embedding + Vector DB 검색으로 교체할 수 있다.
    """
    if not query or not query.strip():
        raise ValueError("검색어가 비어 있습니다.")

    query_lower = query.lower()
    results: list[dict[str, str]] = []

    for path in sorted(SAMPLE_DOCS_DIR.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        content_lower = content.lower()

        if query_lower in content_lower or query_lower in path.stem.lower():
            preview = content.replace("\n", " ").strip()

            if len(preview) > 200:
                preview = preview[:200] + "..."

            results.append(
                {
                    "filename": path.name,
                    "title": path.stem,
                    "preview": preview,
                }
            )

    return results[:top_k]


if __name__ == "__main__":
    mcp.run()
