from __future__ import annotations

from tools.employee_search import search_employees


def main() -> None:
    """
    employees.json 샘플 데이터를 직접 검색해보는 실습 파일이다.
    """
    keywords = ["김철수", "AI플랫폼", "Data Scientist", "RAG"]

    for keyword in keywords:
        print("=" * 80)
        print(f"검색어: {keyword}")
        print("=" * 80)

        results = search_employees(keyword)

        if not results:
            print("검색 결과가 없습니다.")
            continue

        for employee in results:
            print(employee)


if __name__ == "__main__":
    main()
