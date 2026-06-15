"""
Step2-3. RAG 질의응답 구현 - 07_ask_llm.py

역할:
- 생성된 Prompt를 로컬 LLM(Ollama)에 전달한다.
- LLM으로부터 답변을 받아 출력한다.

사전 조건:
- Ollama가 실행 중이어야 한다.
- 사용할 모델이 로컬에 설치되어 있어야 한다.

모델 확인:
    ollama list

실행 예시:
    python labs/rag/07_ask_llm.py
"""

import json
import urllib.request
import urllib.error


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen3:4b"


def ask_llm(prompt: str, model: str = OLLAMA_MODEL) -> str:
    """Ollama 로컬 LLM에 Prompt를 전달하고 답변을 반환한다."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            response_body = response.read().decode("utf-8")
            result = json.loads(response_body)
            return result.get("response", "")

    except urllib.error.URLError as error:
        raise RuntimeError(
            "Ollama 서버에 연결할 수 없습니다. "
            "'ollama serve' 또는 Ollama 앱 실행 상태를 확인하세요."
        ) from error


def ask_llm_with_simple_prompt():
    """LLM 연결 상태를 확인하기 위한 단순 테스트 함수."""
    prompt = "RAG가 무엇인지 한 문단으로 설명해줘."
    answer = ask_llm(prompt)
    return answer


if __name__ == "__main__":
    print("Ollama LLM 호출 테스트")
    print("=" * 80)

    answer = ask_llm_with_simple_prompt()
    print(answer)
