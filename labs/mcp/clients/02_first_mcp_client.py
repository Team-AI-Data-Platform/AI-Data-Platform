import asyncio
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


BASE_DIR = Path(__file__).resolve().parents[1]


async def main() -> None:
    server_script = BASE_DIR / "servers" / "06_all_tools_mcp_server.py"

    server_params = StdioServerParameters(
        command="python",
        args=[str(server_script)],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()

            print("=" * 80)
            print("Tool 목록")
            print("=" * 80)

            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            print("=" * 80)
            print("Tool 호출: list_sample_docs")
            print("=" * 80)

            result = await session.call_tool("list_sample_docs", {})
            print(result)

            print("=" * 80)
            print("Tool 호출: search_docs")
            print("=" * 80)

            result = await session.call_tool(
                "search_docs",
                {
                    "query": "Agent",
                    "top_k": 3,
                },
            )
            print(result)


if __name__ == "__main__":
    asyncio.run(main())
