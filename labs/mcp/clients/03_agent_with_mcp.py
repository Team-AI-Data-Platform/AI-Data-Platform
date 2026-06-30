import asyncio
import json
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


BASE_DIR = Path(__file__).resolve().parents[1]


def select_mcp_tool(user_input: str) -> tuple[str, dict[str, Any]]:
    """
    사용자 입력을 기반으로 호출할 MCP Tool을 선택한다.
    실제 Agent에서는 이 판단을 LLM이 수행할 수 있다.
    """
    text = user_input.strip()

    if "문서 목록" in text:
        return "list_sample_docs", {}

    if "검색" in text or "찾아" in text:
        query = (
            text.replace("검색해줘", "")
            .replace("검색", "")
            .replace("찾아줘", "")
            .replace("찾아", "")
            .strip()
        )

        return "search_docs", {"query": query, "top_k": 3}

    if "상태" in text:
        return "get_platform_status", {}

    if "직원" in text or "employees" in text:
        return "run_select_query", {
            "sql": "SELECT * FROM employees",
            "limit": 10,
        }

    return "", {}


async def run_agent() -> None:
    server_script = BASE_DIR / "servers" / "06_all_tools_mcp_server.py"

    server_params = StdioServerParameters(
        command="python",
        args=[str(server_script)],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            user_input = input("질문을 입력하세요: ").strip()

            tool_name, arguments = select_mcp_tool(user_input)

            if not tool_name:
                print("처리할 수 있는 요청이 아닙니다.")
                print("예: 문서 목록 보여줘 / Agent 검색해줘 / 플랫폼 상태 확인해줘 / 직원 테이블 조회해줘")
                return

            print("=" * 80)
            print("MCP Tool Call")
            print("=" * 80)
            print(
                json.dumps(
                    {
                        "tool_name": tool_name,
                        "arguments": arguments,
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )

            result = await session.call_tool(tool_name, arguments)

            print("=" * 80)
            print("MCP Tool Result")
            print("=" * 80)
            print(result)


if __name__ == "__main__":
    asyncio.run(run_agent())
