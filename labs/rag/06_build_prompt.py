"""
Step2-3. RAG 질의응답 구현 - 06_build_prompt.py

역할:
- Vector DB에서 검색된 문서를 Context로 구성한다.
- 사용자 질문과 Context를 결합하여 LLM에 전달할 Prompt를 만든다.

실행 예시:
    python labs/rag/06_build_prompt.py
"""

from typing import List, Dict

from pathlib import Path
import sys

# 같은 디렉터리의 05_search_documents.py를 import하기 위한 설정
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

from importlib import import_module

search_module = import_module("05_search_documents")
search_documents = search_module.search_documents


def build_context(search_results: List[Dict]) -> str:
    """검색 결과를 LLM이 참고할 Context 문자열로 변환한다."""
    context_parts = []

    for result in search_results:
        context_parts.append(
            f"[문서 {result['rank']}]\n{result['document']}"
        )

    return "\n\n".join(context_parts)


def build_prompt(question: str, search_results: List[Dict]) -> str:
    """질문과 검색 문서를 결합하여 RAG Prompt를 생성한다."""
    context = build_context(search_results)

    prompt = f"""
당신은 사내 AI Data Platform 연구 프로젝트를 지원하는 AI Assistant입니다.
아래의 참고 문서를 기반으로 사용자의 질문에 답변하세요.

답변 규칙:
1. 참고 문서에 근거하여 답변합니다.
2. 참고 문서에 없는 내용은 추측하지 않습니다.
3. 답변은 이해하기 쉽게 정리합니다.
4. 필요한 경우 항목으로 구분하여 설명합니다.

[참고 문서]
{context}

[사용자 질문]
{question}

[답변]
""".strip()

    return prompt


if __name__ == "__main__":
    user_query = "MicroServer 프레임워크의 주요 구성요소는 무엇인가?"

    search_results = search_documents(user_query, top_k=3)
    prompt = build_prompt(user_query, search_results)

    print(prompt)
