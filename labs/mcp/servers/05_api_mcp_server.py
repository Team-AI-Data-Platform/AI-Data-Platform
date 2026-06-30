import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("api-mcp-server")

BASE_DIR = Path(__file__).resolve().parents[1]
API_DATA_PATH = BASE_DIR / "sample_data" / "sample_api.json"


def load_api_data() -> dict:
    if not API_DATA_PATH.exists():
        raise FileNotFoundError(f"API 샘플 데이터를 찾을 수 없습니다: {API_DATA_PATH}")

    return json.loads(API_DATA_PATH.read_text(encoding="utf-8"))


@mcp.tool()
def get_platform_status() -> dict:
    """
    AI DATA Platform 상태 정보를 조회한다.
    """
    data = load_api_data()
    return data["platform_status"]


@mcp.tool()
def get_notices() -> list[dict]:
    """
    공지 목록을 조회한다.
    """
    data = load_api_data()
    return data["notices"]


@mcp.tool()
def get_notice_by_level(level: str) -> list[dict]:
    """
    level 기준으로 공지를 조회한다.
    예: info, warning
    """
    if not level or not level.strip():
        raise ValueError("level 값이 비어 있습니다.")

    data = load_api_data()

    return [
        notice
        for notice in data["notices"]
        if notice["level"].lower() == level.lower()
    ]


if __name__ == "__main__":
    mcp.run()
