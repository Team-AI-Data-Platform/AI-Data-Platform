from __future__ import annotations

from typing import Any, Callable

from tools.calculator import calculate
from tools.employee_search import search_employees
from tools.file_reader import read_text_file
from tools.search import search_documents


ToolFunction = Callable[..., Any]


TOOLS: dict[str, ToolFunction] = {
    "calculator": calculate,
    "search": search_documents,
    "file_reader": read_text_file,
    "employee_search": search_employees,
}


TOOL_SCHEMAS: list[dict[str, Any]] = [
    {
        "name": "calculator",
        "description": "수학 계산이 필요할 때 사용하는 도구이다.",
        "parameters": {
            "expression": {
                "type": "string",
                "description": "계산할 수식. 예: 12500 * 17",
                "required": True,
            }
        },
    },
    {
        "name": "search",
        "description": "sample_docs 디렉터리의 Markdown 문서에서 키워드를 검색할 때 사용하는 도구이다.",
        "parameters": {
            "query": {
                "type": "string",
                "description": "검색어. 예: Agent, RAG, Tool Calling",
                "required": True,
            }
        },
    },
    {
        "name": "file_reader",
        "description": "labs/agent 디렉터리 내부의 텍스트 파일을 읽을 때 사용하는 도구이다.",
        "parameters": {
            "relative_path": {
                "type": "string",
                "description": "labs/agent 기준 상대 경로. 예: sample_docs/agent_sample.md",
                "required": True,
            }
        },
    },
    {
        "name": "employee_search",
        "description": "sample_data/employees.json 파일에서 직원 이름, 부서, 역할, 기술 키워드를 검색하는 도구이다.",
        "parameters": {
            "keyword": {
                "type": "string",
                "description": "직원 검색 키워드. 예: 김철수, AI플랫폼, Data Scientist",
                "required": True,
            }
        },
    },
]


def get_tool(tool_name: str) -> ToolFunction:
    """
    도구 이름으로 실제 Python 함수를 조회한다.
    """
    if tool_name not in TOOLS:
        raise ValueError(f"등록되지 않은 도구입니다: {tool_name}")

    return TOOLS[tool_name]


def get_tool_schemas() -> list[dict[str, Any]]:
    """
    Agent가 사용할 수 있는 도구 설명 목록을 반환한다.
    """
    return TOOL_SCHEMAS
