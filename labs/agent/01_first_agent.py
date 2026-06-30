from __future__ import annotations

import json
from typing import Any

from common.tool_executor import execute_tool
from common.tool_registry import get_tool_schemas


def print_available_tools() -> None:
    """
    현재 Agent가 사용할 수 있는 도구 목록을 출력한다.
    """
    print("=" * 80)
    print("사용 가능한 도구 목록")
    print("=" * 80)

    for schema in get_tool_schemas():
        print(f"- 도구명: {schema['name']}")
        print(f"  설명: {schema['description']}")
        print(f"  파라미터: {schema['parameters']}")
        print()


def select_tool(user_input: str) -> dict[str, Any]:
    """
    사용자 입력을 보고 어떤 도구를 호출할지 결정한다.

    실제 AI Agent에서는 LLM이 이 판단을 수행한다.
    이번 실습에서는 Agent 구조를 이해하기 위해 규칙 기반으로 처리한다.
    """
    text = user_input.strip()

    if "계산" in text or any(operator in text for operator in ["+", "-", "*", "/"]):
        expression = (
            text.replace("계산해줘", "")
            .replace("계산", "")
            .replace("얼마야", "")
            .strip()
        )

        return {
            "tool_name": "calculator",
            "arguments": {
                "expression": expression
            },
        }

    if "직원" in text or "부서" in text:
        keyword = (
            text.replace("직원", "")
            .replace("부서", "")
            .replace("찾아줘", "")
            .replace("찾아", "")
            .replace("검색해줘", "")
            .replace("검색", "")
            .strip()
        )

        return {
            "tool_name": "employee_search",
            "arguments": {
                "keyword": keyword
            },
        }

    if "검색" in text or "찾아" in text:
        query = (
            text.replace("검색해줘", "")
            .replace("검색", "")
            .replace("찾아줘", "")
            .replace("찾아", "")
            .strip()
        )

        return {
            "tool_name": "search",
            "arguments": {
                "query": query
            },
        }

    if "파일" in text and ("읽" in text or "열" in text):
        return {
            "tool_name": "file_reader",
            "arguments": {
                "relative_path": "sample_docs/agent_sample.md"
            },
        }

    return {
        "tool_name": "",
        "arguments": {},
    }


def format_final_answer(tool_name: str, tool_result: Any) -> str:
    """
    도구 실행 결과를 사용자에게 보여줄 최종 답변 형태로 변환한다.
    """
    if tool_name == "calculator":
        return f"계산 결과는 {tool_result}입니다."

    if tool_name == "search":
        if not tool_result:
            return "검색 결과가 없습니다."

        lines = ["문서 검색 결과는 다음과 같습니다."]

        for index, document in enumerate(tool_result, start=1):
            lines.append(f"{index}. {document['title']} ({document['path']})")
            lines.append(f"   {document['content']}")

        return "\n".join(lines)

    if tool_name == "file_reader":
        return f"파일 내용을 읽었습니다.\n\n{tool_result}"

    if tool_name == "employee_search":
        if not tool_result:
            return "직원 검색 결과가 없습니다."

        lines = ["직원 검색 결과는 다음과 같습니다."]

        for index, employee in enumerate(tool_result, start=1):
            skills = ", ".join(employee.get("skills", []))
            lines.append(
                f"{index}. {employee['name']} / {employee['department']} / "
                f"{employee['role']} / 기술: {skills}"
            )

        return "\n".join(lines)

    return str(tool_result)


def main() -> None:
    """
    첫 번째 Agent 실행 함수이다.
    """
    print_available_tools()

    user_input = input("질문을 입력하세요: ").strip()

    if not user_input:
        print("질문이 비어 있습니다.")
        return

    tool_call = select_tool(user_input)

    tool_name = tool_call["tool_name"]
    arguments = tool_call["arguments"]

    if not tool_name:
        print("이번 Agent가 처리할 수 있는 요청이 아닙니다.")
        print("예: 12500 * 17 계산해줘 / Agent 검색해줘 / 파일 읽어줘 / 김철수 직원 찾아줘")
        return

    print("=" * 80)
    print("Tool Call")
    print("=" * 80)
    print(json.dumps(tool_call, ensure_ascii=False, indent=2))

    try:
        tool_result = execute_tool(tool_name, arguments)

        print("=" * 80)
        print("Observation")
        print("=" * 80)
        print(tool_result)

        final_answer = format_final_answer(tool_name, tool_result)

        print("=" * 80)
        print("Final Answer")
        print("=" * 80)
        print(final_answer)

    except Exception as error:
        print("=" * 80)
        print("Agent 실행 오류")
        print("=" * 80)
        print(error)


if __name__ == "__main__":
    main()
