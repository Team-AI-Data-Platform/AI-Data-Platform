from __future__ import annotations

import json
from typing import Any

from common.tool_executor import execute_tool


def run_tool_call(tool_call: dict[str, Any]) -> Any:
    """
    Tool Call dictionary를 받아 실제 도구를 실행한다.
    """
    tool_name = tool_call.get("tool_name", "")
    arguments = tool_call.get("arguments", {})

    return execute_tool(tool_name, arguments)


def main() -> None:
    """
    Tool Calling 구조만 별도로 확인하는 실습이다.
    """
    tool_calls = [
        {
            "tool_name": "calculator",
            "arguments": {
                "expression": "12500 * 17"
            },
        },
        {
            "tool_name": "search",
            "arguments": {
                "query": "ReAct"
            },
        },
        {
            "tool_name": "file_reader",
            "arguments": {
                "relative_path": "sample_docs/agent_sample.md"
            },
        },
        {
            "tool_name": "employee_search",
            "arguments": {
                "keyword": "AI플랫폼"
            },
        },
    ]

    for tool_call in tool_calls:
        print("=" * 80)
        print("Tool Call")
        print("=" * 80)
        print(json.dumps(tool_call, ensure_ascii=False, indent=2))

        try:
            result = run_tool_call(tool_call)

            print("=" * 80)
            print("Tool Result")
            print("=" * 80)
            print(result)

        except Exception as error:
            print("=" * 80)
            print("Tool Error")
            print("=" * 80)
            print(error)


if __name__ == "__main__":
    main()
