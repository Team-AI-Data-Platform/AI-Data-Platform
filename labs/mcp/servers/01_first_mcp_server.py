from mcp.server.fastmcp import FastMCP


mcp = FastMCP("first-mcp-server")


@mcp.tool()
def hello(name: str) -> str:
    """
    이름을 입력받아 인사말을 반환한다.
    """
    return f"안녕하세요, {name}님. 첫 번째 MCP Tool 호출에 성공했습니다."


@mcp.tool()
def add(a: int, b: int) -> int:
    """
    두 숫자를 더한다.
    """
    return a + b


if __name__ == "__main__":
    mcp.run()
