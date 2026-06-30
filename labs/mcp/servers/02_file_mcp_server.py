from pathlib import Path

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("file-mcp-server")

BASE_DIR = Path(__file__).resolve().parents[1]
SAMPLE_DOCS_DIR = BASE_DIR / "sample_docs"


def resolve_doc_path(filename: str) -> Path:
    """
    sample_docs 내부의 Markdown 파일 경로만 허용한다.
    """
    if not filename or not filename.strip():
        raise ValueError("파일명이 비어 있습니다.")

    if "/" in filename or "\\" in filename or ".." in filename:
        raise ValueError("파일명에는 경로 문자를 사용할 수 없습니다.")

    path = (SAMPLE_DOCS_DIR / filename).resolve()

    if not str(path).startswith(str(SAMPLE_DOCS_DIR.resolve())):
        raise ValueError("sample_docs 디렉터리 밖의 파일은 읽을 수 없습니다.")

    if path.suffix != ".md":
        raise ValueError("Markdown 파일만 읽을 수 있습니다.")

    if not path.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {filename}")

    return path


@mcp.tool()
def list_sample_docs() -> list[str]:
    """
    sample_docs 디렉터리에 있는 Markdown 파일 목록을 반환한다.
    """
    return sorted(path.name for path in SAMPLE_DOCS_DIR.glob("*.md"))


@mcp.tool()
def read_sample_doc(filename: str) -> str:
    """
    sample_docs 디렉터리의 Markdown 파일 내용을 읽는다.
    """
    path = resolve_doc_path(filename)
    return path.read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run()
