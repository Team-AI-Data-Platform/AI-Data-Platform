import sqlite3
from pathlib import Path

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("database-mcp-server")

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "sample.db"


def connect_db() -> sqlite3.Connection:
    if not DB_PATH.exists():
        raise FileNotFoundError(
            "sample.db 파일이 없습니다. 먼저 database/create_sample_db.py를 실행하세요."
        )

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def validate_select_query(sql: str) -> None:
    """
    SELECT 쿼리만 허용한다.
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


@mcp.tool()
def list_tables() -> list[str]:
    """
    SQLite DB의 테이블 목록을 조회한다.
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )

    rows = cursor.fetchall()
    conn.close()

    return [row["name"] for row in rows]


@mcp.tool()
def describe_table(table_name: str) -> list[dict[str, str]]:
    """
    테이블 컬럼 정보를 조회한다.
    """
    if not table_name or not table_name.strip():
        raise ValueError("테이블명이 비어 있습니다.")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info({table_name})")

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "name": row["name"],
            "type": row["type"],
            "not_null": str(bool(row["notnull"])),
            "primary_key": str(bool(row["pk"])),
        }
        for row in rows
    ]


@mcp.tool()
def run_select_query(sql: str, limit: int = 20) -> list[dict]:
    """
    SELECT 쿼리를 실행한다.
    """
    validate_select_query(sql)

    safe_limit = min(max(limit, 1), 100)

    conn = connect_db()
    cursor = conn.cursor()

    query = f"SELECT * FROM ({sql}) LIMIT {safe_limit}"
    cursor.execute(query)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


if __name__ == "__main__":
    mcp.run()
