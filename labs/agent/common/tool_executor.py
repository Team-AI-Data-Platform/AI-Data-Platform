from __future__ import annotations

from typing import Any

from common.tool_registry import get_tool


def execute_tool(tool_name: str, arguments: dict[str, Any]) -> Any:
    """
    도구 이름과 입력값을 받아 실제 도구 함수를 실행한다.

    Args:
        tool_name:
            실행할 도구 이름.
            예: "calculator", "search", "file_reader", "employee_search"

        arguments:
            도구 함수에 전달할 인자 dictionary.
            예: {"expression": "12500 * 17"}

    Returns:
        도구 실행 결과.
    """
    if not tool_name or not tool_name.strip():
        raise ValueError("도구 이름이 비어 있습니다.")

    if arguments is None:
        arguments = {}

    tool_function = get_tool(tool_name)

    return tool_function(**arguments)
