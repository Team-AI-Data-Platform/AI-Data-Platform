"""
Step2-3. RAG 질의응답 구현 - 08_first_rag.py

역할:
- 사용자 질문을 입력받는다.
- Chroma Vector DB에서 관련 문서를 검색한다.
- 검색 결과를 Context로 구성한다.
- Prompt를 생성한다.
- Prompt를 Ollama LLM에 전달한다.
- 최종 RAG 답변을 출력한다.

실행 예시:
    python labs/rag/08_first_rag.py
"""

from pathlib import Path
import sys
from importlib import import_module


BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

search_module = import_module("05_search_documents")
prompt_module = import_module("06_build_prompt")
llm_module = import_module("07_ask_llm")

search_documents = search_module.search_documents
build_prompt = prompt_module.build_prompt
ask_llm = llm_module.ask_llm


def run_rag(question: str, top_k: int = 3) -> str:
    """검색부터 답변 생성까지 End-to-End RAG 흐름을 실행한다."""
    search_results = search_documents(question, top_k=top_k)
    prompt = build_prompt(question, search_results)
    answer = ask_llm(prompt)
    return answer


if __name__ == "__main__":
    print("Step2-3. RAG 질의응답 구현")
    print("=" * 80)

    question = input("질문을 입력하세요: ").strip()

    if not question:
        question = "MicroServer 프레임워크의 주요 구성요소는 무엇인가?"
        print(f"기본 질문을 사용합니다: {question}")

    print("\n1. Vector DB에서 관련 문서 검색")
    print("2. 검색 결과를 Context로 구성")
    print("3. Prompt 생성")
    print("4. LLM 답변 생성")
    print("\n처리 중...\n")

    rag_answer = run_rag(question, top_k=3)

    print("=" * 80)
    print("RAG 최종 답변")
    print("=" * 80)
    print(rag_answer)
