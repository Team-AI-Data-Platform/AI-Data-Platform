from __future__ import annotations

import json
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parents[1]
EMPLOYEE_DATA_PATH = BASE_DIR / "sample_data" / "employees.json"


def load_employees() -> list[dict[str, Any]]:
    """
    sample_data/employees.json 파일을 읽어서 직원 목록을 반환한다.
    """
    return json.loads(EMPLOYEE_DATA_PATH.read_text(encoding="utf-8"))


def search_employees(keyword: str) -> list[dict[str, Any]]:
    """
    직원 샘플 데이터에서 이름, 부서, 역할에 keyword가 포함된 직원을 검색한다.

    Args:
        keyword:
            검색 키워드.
            예: "김철수", "AI플랫폼", "Data Scientist"

    Returns:
        검색된 직원 목록.
    """
    if not keyword or not keyword.strip():
        raise ValueError("직원 검색어가 비어 있습니다.")

    normalized_keyword = keyword.lower()
    results: list[dict[str, Any]] = []

    for employee in load_employees():
        searchable_text = " ".join(
            [
                str(employee.get("name", "")),
                str(employee.get("department", "")),
                str(employee.get("role", "")),
                str(employee.get("skills", "")),
            ]
        ).lower()

        if normalized_keyword in searchable_text:
            results.append(employee)

    return results
