import json
import sqlite3
from pathlib import Path

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("ai-data-platform-mcp-server")

BASE_DIR = Path(__file__).resolve().parents[1]
SAMPLE_DOCS_DIR = BASE_DIR / "sample_docs"
API_DATA_PATH = BASE_DIR / "sample_data" / "sample_api.json"
DB_PATH = BASE_DIR / "database" / "sample.db"


@mcp.tool()
def list_sample_docs() -> list[str]:
    """
    sample_docs 디렉터리의 Markdown 파일 목록을 반환한다.
    """
    return sorted(path.name for path in SAMPLE_DOCS_DIR.glob("*.md"))


@mcp.tool()
def read_sample_doc(filename: str) -> str:
    """
    sample_docs 디렉터리의 Markdown 파일을 읽는다.
    """
    if not filename or not filename.strip():
        raise ValueError("파일명이 비어 있습니다.")

    if "/" in filename or "\\" in filename or ".." in filename:
        raise ValueError("파일명에는 경로 문자를 사용할 수 없습니다.")

    path = (SAMPLE_DOCS_DIR / filename).resolve()

    if not str(path).startswith(str(SAMPLE_DOCS_DIR.resolve())):
        raise ValueError("sample_docs 밖의 파일은 읽을 수 없습니다.")

    if path.suffix != ".md":
        raise ValueError("Markdown 파일만 읽을 수 있습니다.")

    if not path.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {filename}")

    return path.read_text(encoding="utf-8")


@mcp.tool()
def search_docs(query: str, top_k: int = 3) -> list[dict[str, str]]:
    """
    sample_docs Markdown 문서에서 query가 포함된 문서를 검색한다.
    """
    if not query or not query.strip():
        raise ValueError("검색어가 비어 있습니다.")

    query_lower = query.lower()
    results: list[dict[str, str]] = []

    for path in sorted(SAMPLE_DOCS_DIR.glob("*.md")):
        content = path.read_text(encoding="utf-8")

        if query_lower in content.lower() or query_lower in path.stem.lower():
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


@mcp.tool()
def get_platform_status() -> dict:
    """
    AI DATA Platform 상태 정보를 조회한다.
    """
    data = json.loads(API_DATA_PATH.read_text(encoding="utf-8"))
    return data["platform_status"]


@mcp.tool()
def list_tables() -> list[str]:
    """
    SQLite DB 테이블 목록을 조회한다.
    """
    if not DB_PATH.exists():
        raise FileNotFoundError("sample.db가 없습니다. create_sample_db.py를 먼저 실행하세요.")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )

    rows = cursor.fetchall()
    conn.close()

    return [row["name"] for row in rows]


@mcp.tool()
def run_select_query(sql: str, limit: int = 20) -> list[dict]:
    """
    SELECT 쿼리만 실행한다.
    """
    normalized = sql.strip().lower()

    if not normalized.startswith("select"):
        raise ValueError("SELECT 쿼리만 실행할 수 있습니다.")

    blocked_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "replace",
        "truncate",
    ]

    for keyword in blocked_keywords:
        if keyword in normalized:
            raise ValueError(f"허용되지 않은 SQL 키워드입니다: {keyword}")

    safe_limit = min(max(limit, 1), 100)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = f"SELECT * FROM ({sql}) LIMIT {safe_limit}"
    cursor.execute(query)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


if __name__ == "__main__":
    mcp.run()
