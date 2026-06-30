import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "sample.db"


def main() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE projects (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            status TEXT NOT NULL
        )
        """
    )

    cursor.executemany(
        "INSERT INTO employees VALUES (?, ?, ?, ?)",
        [
            (1, "김철수", "AI플랫폼", "AI Engineer"),
            (2, "이영희", "R&D", "Data Scientist"),
            (3, "박민수", "플랫폼개발", "Backend Developer"),
        ],
    )

    cursor.executemany(
        "INSERT INTO projects VALUES (?, ?, ?, ?)",
        [
            (1, "Local LLM 구축", "LLM", "done"),
            (2, "RAG 실습", "RAG", "done"),
            (3, "AI Agent 연구", "Agent", "in_progress"),
            (4, "MCP 연동", "MCP", "planned"),
        ],
    )

    conn.commit()
    conn.close()

    print(f"DB 생성 완료: {DB_PATH}")


if __name__ == "__main__":
    main()
