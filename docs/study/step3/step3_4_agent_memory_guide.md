# Step3-4. Agent Memory와 상태 관리 가이드

> AI DATA Platform 연구 프로젝트  
> Step3. AI Agent  
> Part1. AI Agent 기초  
> 문서 경로: `docs/study/step3/step3_4_agent_memory_guide.md`  
> 작성일: 2026-06-29

---

## 1. 문서 목적

이 문서는 AI Agent가 **대화 이력**, **작업 상태**, **도구 실행 결과**, **사용자 맥락**을 어떻게 기억하고 관리하는지 학습하기 위한 가이드 문서이다.

앞 단계인 `Step3-3. 첫 번째 AI Agent 구현`에서는 다음 구조를 구현했다.

```text
사용자 질문
   ↓
도구 선택
   ↓
Tool Call 생성
   ↓
Tool Executor 실행
   ↓
Tool Result 반환
   ↓
최종 답변 출력
```

하지만 Step3-3의 Agent는 매번 새로운 요청을 독립적으로 처리했다.  
즉, 이전에 사용자가 무엇을 물어봤는지, 어떤 도구를 실행했는지, 어떤 파일을 읽었는지 기억하지 못한다.

이번 문서에서는 Agent에 Memory를 추가하여 다음과 같은 흐름을 만든다.

```text
사용자 질문
   ↓
이전 대화와 작업 상태 확인
   ↓
현재 요청 분석
   ↓
도구 선택 및 실행
   ↓
실행 결과 저장
   ↓
대화 이력 저장
   ↓
최종 답변 출력
```

이번 단계의 핵심은 다음이다.

> **Agent Memory는 단순한 대화 저장소가 아니라, Agent가 작업을 이어가기 위한 상태 관리 구조이다.**

---

## 2. 이번 문서의 위치

전체 Step3 목차에서 이 문서의 위치는 다음과 같다.

```text
Step3. AI Agent
│
├─ Part1. AI Agent 기초
│   ├─ Step3-1. AI Agent 개요
│   ├─ Step3-2. ReAct와 Tool Calling
│   ├─ Step3-3. 첫 번째 AI Agent 구현
│   └─ Step3-4. Agent Memory와 상태 관리   ← 현재 문서
│
├─ Part2. AI Agent 심화
│   ├─ Step3-5. Planning Agent와 Workflow
│   ├─ Step3-6. LangGraph 기반 Workflow Agent
│   ├─ Step3-7. MCP 아키텍처 이해
│   └─ Step3-8. MCP 기반 외부 시스템 연동
│
└─ Part3. Enterprise AI Agent
    ├─ Step3-9. Multi Agent 협업
    └─ Step3-10. Enterprise AI Agent Platform
```

Step3-4는 Part1의 마지막 문서이다.

Part1에서는 다음 순서로 Agent의 기본기를 다룬다.

```text
Step3-1:
Agent의 큰 그림 이해

Step3-2:
ReAct와 Tool Calling 동작 원리 이해

Step3-3:
첫 번째 Agent 구현

Step3-4:
Agent가 이전 대화와 작업 상태를 기억하도록 확장
```

Step3-4까지 완료하면 단일 Agent의 기본 구조는 어느 정도 갖추게 된다.

---

## 3. 학습 목표

이 문서를 마치면 다음 내용을 이해하고 직접 구현할 수 있어야 한다.

```text
1. Agent Memory가 왜 필요한지 설명할 수 있다.
2. Short-term Memory와 Long-term Memory의 차이를 설명할 수 있다.
3. Conversation Memory와 Task State의 차이를 설명할 수 있다.
4. Tool Execution History가 왜 중요한지 설명할 수 있다.
5. JSON 파일 기반 Memory를 구현할 수 있다.
6. Agent 실행 흐름에 Memory 저장 로직을 추가할 수 있다.
7. Memory에 저장하면 안 되는 정보가 무엇인지 이해할 수 있다.
8. Enterprise 환경에서 Memory를 설계할 때 고려해야 할 보안 요소를 설명할 수 있다.
```

---

## 4. 왜 Agent Memory가 필요한가?

Memory가 없는 Agent는 매 요청을 독립적으로 처리한다.

예를 들어 사용자가 다음과 같이 대화한다고 하자.

```text
사용자:
sample_docs/agent_sample.md 파일 읽어줘.

Agent:
파일 내용을 읽었습니다.

사용자:
방금 읽은 파일을 세 줄로 요약해줘.
```

Memory가 없는 Agent는 두 번째 요청에서 문제가 생긴다.

```text
"방금 읽은 파일"이 무엇인지 모른다.
이전에 어떤 파일을 읽었는지 모른다.
이전 도구 실행 결과를 가지고 있지 않다.
```

Memory가 있는 Agent는 다르게 동작한다.

```text
1. 이전에 읽은 파일 경로를 기억한다.
2. 이전 파일 내용을 기억하거나 다시 읽을 수 있다.
3. "방금 읽은 파일"이 무엇인지 이해한다.
4. 이어지는 요청을 자연스럽게 처리한다.
```

즉, Memory는 Agent가 대화를 이어가고 작업 상태를 유지하기 위해 필요하다.

---

## 5. Memory가 없는 Agent의 한계

Memory가 없는 Agent는 다음 한계를 가진다.

```text
1. 이전 대화 내용을 기억하지 못한다.
2. 이전에 실행한 도구 결과를 재사용하지 못한다.
3. 사용자가 말한 "아까", "방금", "그 파일", "이 내용"을 이해하기 어렵다.
4. 여러 단계로 이루어진 작업을 이어가기 어렵다.
5. 작업 중간 상태를 저장하지 못한다.
6. 오류가 발생했을 때 이전 상태로 복구하기 어렵다.
7. 도구 실행 이력을 감사하거나 분석하기 어렵다.
```

실제 업무 요청은 한 번의 질문으로 끝나지 않는 경우가 많다.

```text
1. 파일을 읽는다.
2. 요약한다.
3. 표로 바꾼다.
4. 문장을 다듬는다.
5. 보고서 형식으로 만든다.
6. 검토 의견을 반영한다.
```

이런 흐름을 처리하려면 Agent는 작업 상태를 기억해야 한다.

---

## 6. Agent Memory의 핵심 개념

Agent Memory는 단순히 채팅 내용을 저장하는 기능이 아니다.

Agent Memory는 다음 정보를 관리한다.

```text
1. 대화 이력
2. 사용자 요청
3. Agent 응답
4. 도구 호출 이력
5. 도구 실행 결과
6. 현재 작업 상태
7. 선택된 파일 또는 문서
8. 중간 산출물
9. 사용자 선호 또는 프로젝트 설정
```

Memory를 구조화하면 다음과 같이 나눌 수 있다.

```text
Agent Memory
│
├─ Conversation Memory
│   └─ 사용자와 Agent의 대화 이력
│
├─ Tool Execution History
│   └─ 어떤 도구를 어떤 입력값으로 실행했는지
│
├─ Task State
│   └─ 현재 진행 중인 작업 상태
│
└─ Long-term Memory
    └─ 세션을 넘어 유지되는 사용자/프로젝트 정보
```

---

## 7. Short-term Memory와 Long-term Memory

최신 Agent 프레임워크에서도 Memory는 일반적으로 **Short-term Memory**와 **Long-term Memory**로 나누어 설명한다.

LangChain/LangGraph 문서에서도 short-term memory는 현재 대화나 thread 범위의 상태로, long-term memory는 여러 세션이나 대화에 걸쳐 유지되는 정보로 설명된다.

---

### 7.1 Short-term Memory

Short-term Memory는 현재 대화 또는 현재 작업 안에서만 유지되는 기억이다.

예시는 다음과 같다.

```text
1. 방금 사용자가 한 질문
2. 직전 Agent 답변
3. 방금 읽은 파일 경로
4. 방금 검색한 결과
5. 현재 작업 단계
```

Short-term Memory는 보통 다음 용도로 사용된다.

```text
1. 이어지는 질문 이해
2. 대화 맥락 유지
3. 현재 작업 상태 추적
4. 도구 실행 결과 재사용
```

예시:

```text
사용자:
agent_sample.md 파일 읽어줘.

Agent:
파일을 읽었습니다.

사용자:
그 파일을 요약해줘.
```

여기서 "그 파일"을 이해하려면 Short-term Memory가 필요하다.

---

### 7.2 Long-term Memory

Long-term Memory는 여러 대화나 세션을 넘어 유지되는 기억이다.

예시는 다음과 같다.

```text
1. 사용자가 선호하는 문서 형식
2. 프로젝트 기본 경로
3. 자주 사용하는 모델 이름
4. 팀에서 사용하는 용어
5. 반복적으로 사용하는 업무 규칙
```

예를 들어 사용자가 항상 다음 형식을 선호한다고 하자.

```text
"마크다운 문서는 MkDocs 기준으로 작성해줘."
```

이런 정보는 Long-term Memory에 저장할 수 있다.

하지만 Long-term Memory는 신중하게 설계해야 한다.  
개인정보, 민감정보, 일시적인 정보까지 모두 저장하면 위험하다.

---

## 8. Conversation Memory

Conversation Memory는 사용자와 Agent가 주고받은 대화 이력을 저장한다.

예시 구조는 다음과 같다.

```json
[
  {
    "role": "user",
    "content": "파일 읽어줘",
    "timestamp": "2026-06-29T10:00:00+09:00"
  },
  {
    "role": "assistant",
    "content": "파일 내용을 읽었습니다.",
    "timestamp": "2026-06-29T10:00:03+09:00"
  }
]
```

Conversation Memory는 다음 상황에서 중요하다.

```text
1. 사용자가 이전 발화를 참조할 때
2. Agent가 답변 흐름을 유지해야 할 때
3. 대화 내용을 요약해야 할 때
4. 오류 발생 시 이전 대화를 확인해야 할 때
```

하지만 대화 이력을 무한정 LLM에 넣을 수는 없다.  
LLM에는 Context Window 한계가 있기 때문이다.

따라서 실제 시스템에서는 다음 전략이 필요하다.

```text
1. 최근 N개 대화만 유지
2. 오래된 대화는 요약해서 저장
3. 중요한 사실만 별도 Memory로 추출
4. 민감한 내용은 저장하지 않거나 마스킹
```

---

## 9. Task State

Task State는 현재 Agent가 수행 중인 작업 상태를 의미한다.

Conversation Memory가 대화 중심이라면, Task State는 작업 중심이다.

예시는 다음과 같다.

```json
{
  "current_task": "파일 요약",
  "last_file_path": "sample_docs/agent_sample.md",
  "last_tool_name": "file_reader",
  "last_tool_result_summary": "AI Agent 샘플 문서를 읽음",
  "status": "file_loaded"
}
```

Task State가 있으면 Agent는 다음과 같은 요청을 처리하기 쉬워진다.

```text
"방금 파일 요약해줘."
"아까 검색한 결과를 표로 만들어줘."
"이전 결과에서 핵심만 뽑아줘."
"그 내용을 보고서 문체로 바꿔줘."
```

Task State는 특히 Workflow Agent에서 중요해진다.  
Step3-5와 Step3-6에서 다룰 Planning Agent와 LangGraph는 상태 관리를 더 체계적으로 사용한다.

---

## 10. Tool Execution History

Tool Execution History는 Agent가 어떤 도구를 언제, 어떤 입력값으로 실행했는지 저장하는 기록이다.

예시는 다음과 같다.

```json
[
  {
    "tool_name": "file_reader",
    "arguments": {
      "relative_path": "sample_docs/agent_sample.md"
    },
    "status": "success",
    "timestamp": "2026-06-29T10:01:00+09:00"
  },
  {
    "tool_name": "search",
    "arguments": {
      "query": "Agent"
    },
    "status": "success",
    "timestamp": "2026-06-29T10:02:00+09:00"
  }
]
```

Tool Execution History가 필요한 이유는 다음과 같다.

```text
1. Agent가 이전 도구 결과를 참조할 수 있다.
2. 오류가 발생했을 때 원인을 추적할 수 있다.
3. 어떤 도구가 자주 사용되는지 분석할 수 있다.
4. 보안 감사 로그로 활용할 수 있다.
5. Agent 품질 개선에 사용할 수 있다.
```

Enterprise 환경에서는 Tool Execution History가 매우 중요하다.

Agent가 실제 업무 시스템을 조회하거나 수정한다면, 누가 어떤 도구를 어떤 입력값으로 실행했는지 기록해야 한다.

---

## 11. 이번 실습에서 만들 Memory 구조

이번 실습에서는 JSON 파일을 사용해 간단한 Memory를 만든다.

최종 구조는 다음과 같다.

```json
{
  "conversation": [],
  "tool_history": [],
  "task_state": {}
}
```

각 항목의 의미는 다음과 같다.

```text
conversation:
사용자와 Agent의 대화 이력

tool_history:
도구 실행 이력

task_state:
현재 작업 상태
```

이번 실습에서는 복잡한 DB를 사용하지 않고 JSON 파일을 사용한다.

이유는 다음과 같다.

```text
1. 구조를 눈으로 확인하기 쉽다.
2. 설치할 라이브러리가 없다.
3. 처음 Memory 개념을 이해하기 좋다.
4. 파일을 열어서 저장 결과를 바로 볼 수 있다.
```

운영 환경에서는 SQLite, PostgreSQL, Redis, Vector DB, LangGraph Store 등을 사용할 수 있다.

---

## 12. 실습 디렉터리 구조

Step3-3에서 만든 구조에 Memory 디렉터리를 추가한다.

```text
labs
└── agent
    ├── tools
    │   ├── __init__.py
    │   ├── calculator.py
    │   ├── search.py
    │   └── file_reader.py
    │
    ├── common
    │   ├── __init__.py
    │   ├── tool_registry.py
    │   └── tool_executor.py
    │
    ├── memory
    │   ├── __init__.py
    │   └── json_memory.py
    │
    ├── data
    │   └── agent_memory.json
    │
    ├── sample_docs
    │   └── agent_sample.md
    │
    ├── 01_first_agent.py
    ├── 02_tool_calling.py
    └── 03_memory_agent.py
```

---

## 13. 디렉터리 생성

프로젝트 루트에서 아래 명령을 실행한다.

```bash
mkdir -p labs/agent/memory
mkdir -p labs/agent/data

touch labs/agent/memory/__init__.py
```

Memory 저장 파일은 코드에서 자동으로 생성되도록 만들 예정이다.

---

# Part A. JSON Memory 구현

---

## 14. JSON Memory 코드 만들기

파일 경로:

```text
labs/agent/memory/json_memory.py
```

코드:

```python
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parents[1]
MEMORY_PATH = BASE_DIR / "data" / "agent_memory.json"


def now_iso() -> str:
    """
    현재 시간을 ISO 문자열로 반환한다.

    Returns:
        현재 시간 문자열.
        예: "2026-06-29T10:30:00"
    """
    return datetime.now().isoformat(timespec="seconds")


def default_memory() -> dict[str, Any]:
    """
    기본 Memory 구조를 생성한다.

    Returns:
        conversation, tool_history, task_state를 가진 dictionary.
    """
    return {
        "conversation": [],
        "tool_history": [],
        "task_state": {},
    }


def load_memory() -> dict[str, Any]:
    """
    JSON 파일에서 Memory를 읽어온다.

    Memory 파일이 없으면 기본 Memory 구조를 반환한다.

    Returns:
        Memory dictionary.
    """
    if not MEMORY_PATH.exists():
        return default_memory()

    with MEMORY_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_memory(memory: dict[str, Any]) -> None:
    """
    Memory dictionary를 JSON 파일로 저장한다.

    Args:
        memory:
            저장할 Memory dictionary.
    """
    MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)

    with MEMORY_PATH.open("w", encoding="utf-8") as file:
        json.dump(memory, file, ensure_ascii=False, indent=2)


def add_message(role: str, content: str) -> None:
    """
    대화 이력에 메시지를 추가한다.

    Args:
        role:
            메시지 역할.
            예: "user", "assistant"

        content:
            메시지 내용.
    """
    memory = load_memory()

    message = {
        "role": role,
        "content": content,
        "timestamp": now_iso(),
    }

    memory["conversation"].append(message)

    save_memory(memory)


def add_tool_history(
    tool_name: str,
    arguments: dict[str, Any],
    result: Any,
    status: str = "success",
) -> None:
    """
    도구 실행 이력을 저장한다.

    Args:
        tool_name:
            실행한 도구 이름.

        arguments:
            도구에 전달한 입력값.

        result:
            도구 실행 결과.

        status:
            실행 상태.
            예: "success", "error"
    """
    memory = load_memory()

    history = {
        "tool_name": tool_name,
        "arguments": arguments,
        "result": str(result),
        "status": status,
        "timestamp": now_iso(),
    }

    memory["tool_history"].append(history)

    save_memory(memory)


def update_task_state(key: str, value: Any) -> None:
    """
    Task State에 값을 저장하거나 갱신한다.

    Args:
        key:
            저장할 상태 이름.
            예: "last_file_path"

        value:
            저장할 값.
    """
    memory = load_memory()

    memory["task_state"][key] = value
    memory["task_state"]["updated_at"] = now_iso()

    save_memory(memory)


def get_task_state(key: str, default: Any = None) -> Any:
    """
    Task State에서 특정 값을 조회한다.

    Args:
        key:
            조회할 상태 이름.

        default:
            값이 없을 때 반환할 기본값.

    Returns:
        저장된 상태값.
    """
    memory = load_memory()

    return memory["task_state"].get(key, default)


def clear_memory() -> None:
    """
    Memory를 초기화한다.
    """
    save_memory(default_memory())
```

---

## 15. JSON Memory 코드 분석

---

### 15.1 MEMORY_PATH

```python
BASE_DIR = Path(__file__).resolve().parents[1]
MEMORY_PATH = BASE_DIR / "data" / "agent_memory.json"
```

`BASE_DIR`은 `labs/agent` 디렉터리를 의미한다.

파일 위치가 다음과 같다면

```text
labs/agent/memory/json_memory.py
```

`parents[1]`은 다음 위치를 가리킨다.

```text
labs/agent
```

따라서 Memory 파일은 다음 위치에 저장된다.

```text
labs/agent/data/agent_memory.json
```

---

### 15.2 default_memory 함수

```python
def default_memory() -> dict[str, Any]:
```

이 함수는 기본 Memory 구조를 만든다.

```python
{
    "conversation": [],
    "tool_history": [],
    "task_state": {},
}
```

각 항목의 의미는 다음과 같다.

```text
conversation:
대화 이력 목록

tool_history:
도구 실행 이력 목록

task_state:
현재 작업 상태 dictionary
```

---

### 15.3 load_memory 함수

```python
def load_memory() -> dict[str, Any]:
```

이 함수는 JSON 파일에서 Memory를 읽는다.

```python
if not MEMORY_PATH.exists():
    return default_memory()
```

Memory 파일이 아직 없으면 기본 구조를 반환한다.

이렇게 하면 첫 실행 시 파일이 없어도 오류가 나지 않는다.

---

### 15.4 save_memory 함수

```python
def save_memory(memory: dict[str, Any]) -> None:
```

이 함수는 Memory를 JSON 파일로 저장한다.

```python
json.dump(memory, file, ensure_ascii=False, indent=2)
```

`ensure_ascii=False`는 한글이 깨지지 않도록 저장하기 위한 설정이다.

`indent=2`는 JSON 파일을 사람이 읽기 좋게 들여쓰기해서 저장한다.

---

### 15.5 add_message 함수

```python
def add_message(role: str, content: str) -> None:
```

이 함수는 대화 이력에 메시지를 추가한다.

예를 들어 사용자가 질문하면 다음처럼 저장된다.

```json
{
  "role": "user",
  "content": "파일 읽어줘",
  "timestamp": "2026-06-29T10:30:00"
}
```

Agent가 답변하면 다음처럼 저장된다.

```json
{
  "role": "assistant",
  "content": "파일 내용을 읽었습니다.",
  "timestamp": "2026-06-29T10:30:03"
}
```

---

### 15.6 add_tool_history 함수

이 함수는 도구 실행 이력을 저장한다.

```python
history = {
    "tool_name": tool_name,
    "arguments": arguments,
    "result": str(result),
    "status": status,
    "timestamp": now_iso(),
}
```

도구 실행 결과는 어떤 타입이든 될 수 있으므로 문자열로 변환해서 저장한다.

```python
"result": str(result)
```

처음 실습에서는 단순하게 문자열로 저장하지만, 실제 운영 환경에서는 결과 원문 전체를 저장하지 않는 것이 좋다.  
민감정보가 포함될 수 있기 때문이다.

---

### 15.7 update_task_state 함수

이 함수는 현재 작업 상태를 저장한다.

예를 들어 파일을 읽었을 때 다음 상태를 저장할 수 있다.

```python
update_task_state("last_file_path", "sample_docs/agent_sample.md")
update_task_state("last_action", "file_read")
```

이렇게 저장하면 이후 사용자가 다음과 같이 물었을 때 활용할 수 있다.

```text
"방금 읽은 파일 요약해줘."
```

---

# Part B. Memory Agent 구현

이제 Step3-3에서 만든 Agent에 Memory를 연결한다.

---

## 16. Memory Agent 코드 만들기

파일 경로:

```text
labs/agent/03_memory_agent.py
```

코드:

```python
from __future__ import annotations

import json
from typing import Any

from common.tool_executor import execute_tool
from common.tool_registry import get_tool_schemas
from memory.json_memory import (
    add_message,
    add_tool_history,
    clear_memory,
    get_task_state,
    load_memory,
    update_task_state,
)


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
        print()


def print_memory_summary() -> None:
    """
    현재 저장된 Memory 요약을 출력한다.
    """
    memory = load_memory()

    print("=" * 80)
    print("현재 Memory 요약")
    print("=" * 80)
    print(f"대화 수: {len(memory['conversation'])}")
    print(f"도구 실행 수: {len(memory['tool_history'])}")
    print(f"현재 작업 상태: {memory['task_state']}")
    print()


def select_tool(user_input: str) -> dict[str, Any]:
    """
    사용자 입력과 Memory 상태를 바탕으로 어떤 도구를 호출할지 결정한다.

    실제 AI Agent에서는 LLM이 이 판단을 수행한다.
    이번 실습에서는 규칙 기반으로 처리한다.
    """
    text = user_input.strip()

    if text in ["초기화", "메모리 초기화", "memory clear"]:
        return {
            "tool_name": "clear_memory",
            "arguments": {},
        }

    if "방금" in text and ("파일" in text or "내용" in text or "요약" in text):
        last_file_path = get_task_state("last_file_path")

        if last_file_path:
            return {
                "tool_name": "file_reader",
                "arguments": {
                    "relative_path": last_file_path
                },
            }

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


def summarize_text(text: str, max_length: int = 200) -> str:
    """
    긴 텍스트를 Memory에 저장하기 위한 짧은 요약 문자열로 변환한다.

    Args:
        text:
            원본 텍스트.

        max_length:
            최대 길이.

    Returns:
        잘라낸 요약 텍스트.
    """
    if len(text) <= max_length:
        return text

    return text[:max_length] + "..."


def format_final_answer(tool_name: str, tool_result: Any) -> str:
    """
    도구 실행 결과를 최종 답변 문자열로 변환한다.
    """
    if tool_name == "calculator":
        return f"계산 결과는 {tool_result}입니다."

    if tool_name == "search":
        if not tool_result:
            return "검색 결과가 없습니다."

        lines = ["검색 결과는 다음과 같습니다."]

        for index, document in enumerate(tool_result, start=1):
            lines.append(f"{index}. {document['title']} - {document['content']}")

        return "\n".join(lines)

    if tool_name == "file_reader":
        return f"파일 내용을 읽었습니다.\n\n{tool_result}"

    return str(tool_result)


def update_state_after_tool(tool_name: str, arguments: dict[str, Any], result: Any) -> None:
    """
    도구 실행 후 Task State를 갱신한다.

    Args:
        tool_name:
            실행한 도구 이름.

        arguments:
            도구 입력값.

        result:
            도구 실행 결과.
    """
    update_task_state("last_tool_name", tool_name)
    update_task_state("last_tool_arguments", arguments)
    update_task_state("last_tool_result_summary", summarize_text(str(result)))

    if tool_name == "file_reader":
        update_task_state("last_file_path", arguments.get("relative_path"))
        update_task_state("last_action", "file_read")

    if tool_name == "search":
        update_task_state("last_search_query", arguments.get("query"))
        update_task_state("last_action", "search")

    if tool_name == "calculator":
        update_task_state("last_expression", arguments.get("expression"))
        update_task_state("last_action", "calculation")


def main() -> None:
    """
    Memory를 사용하는 Agent 실행 함수이다.

    실행 흐름:
    1. 도구 목록 출력
    2. 현재 Memory 요약 출력
    3. 사용자 입력 저장
    4. 도구 선택
    5. 도구 실행
    6. 도구 실행 이력 저장
    7. Task State 갱신
    8. Agent 답변 저장
    9. 최종 답변 출력
    """
    print_available_tools()
    print_memory_summary()

    user_input = input("질문을 입력하세요: ").strip()

    if not user_input:
        print("질문이 비어 있습니다.")
        return

    if user_input in ["초기화", "메모리 초기화", "memory clear"]:
        clear_memory()
        print("Memory를 초기화했습니다.")
        return

    add_message("user", user_input)

    tool_call = select_tool(user_input)

    tool_name = tool_call["tool_name"]
    arguments = tool_call["arguments"]

    if not tool_name:
        final_answer = "이번 Agent가 처리할 수 있는 요청이 아닙니다."
        add_message("assistant", final_answer)
        print(final_answer)
        return

    print("=" * 80)
    print("Tool Call")
    print("=" * 80)
    print(json.dumps(tool_call, ensure_ascii=False, indent=2))

    try:
        tool_result = execute_tool(tool_name, arguments)

        add_tool_history(
            tool_name=tool_name,
            arguments=arguments,
            result=tool_result,
            status="success",
        )

        update_state_after_tool(tool_name, arguments, tool_result)

        print("=" * 80)
        print("Observation")
        print("=" * 80)
        print(tool_result)

        final_answer = format_final_answer(tool_name, tool_result)

        add_message("assistant", final_answer)

        print("=" * 80)
        print("Final Answer")
        print("=" * 80)
        print(final_answer)

    except Exception as error:
        add_tool_history(
            tool_name=tool_name,
            arguments=arguments,
            result=str(error),
            status="error",
        )

        final_answer = f"Agent 실행 중 오류가 발생했습니다: {error}"
        add_message("assistant", final_answer)

        print("=" * 80)
        print("Agent 실행 오류")
        print("=" * 80)
        print(error)


if __name__ == "__main__":
    main()
```

---

## 17. Memory Agent 코드 분석

---

### 17.1 Memory 관련 import

```python
from memory.json_memory import (
    add_message,
    add_tool_history,
    clear_memory,
    get_task_state,
    load_memory,
    update_task_state,
)
```

각 함수의 역할은 다음과 같다.

```text
add_message:
대화 이력 저장

add_tool_history:
도구 실행 이력 저장

clear_memory:
Memory 초기화

get_task_state:
현재 작업 상태 조회

load_memory:
전체 Memory 읽기

update_task_state:
작업 상태 저장 또는 갱신
```

---

### 17.2 print_memory_summary 함수

```python
def print_memory_summary() -> None:
```

이 함수는 현재 Memory 상태를 요약해서 출력한다.

```text
대화 수
도구 실행 수
현재 작업 상태
```

Agent 실행 전에 Memory 상태를 보여주면, Agent가 이전 작업을 기억하고 있는지 확인할 수 있다.

---

### 17.3 select_tool 함수의 Memory 활용

```python
if "방금" in text and ("파일" in text or "내용" in text or "요약" in text):
    last_file_path = get_task_state("last_file_path")
```

이 코드는 사용자가 "방금 파일", "방금 내용"처럼 이전 작업을 참조할 때 Memory를 확인한다.

예를 들어 이전에 다음 작업을 했다면

```text
파일 읽어줘
```

Task State에는 다음 값이 저장된다.

```json
{
  "last_file_path": "sample_docs/agent_sample.md"
}
```

이후 사용자가 다음처럼 말하면

```text
방금 파일 다시 읽어줘
```

Agent는 `last_file_path` 값을 사용해 같은 파일을 다시 읽을 수 있다.

---

### 17.4 summarize_text 함수

```python
def summarize_text(text: str, max_length: int = 200) -> str:
```

이 함수는 긴 도구 실행 결과를 짧게 잘라서 저장한다.

Memory에 너무 긴 내용을 계속 저장하면 문제가 생길 수 있다.

```text
1. JSON 파일이 너무 커진다.
2. LLM Context에 넣기 어렵다.
3. 민감정보가 과도하게 저장될 수 있다.
4. 저장과 로딩이 느려진다.
```

따라서 처음에는 요약 문자열만 Task State에 저장한다.

---

### 17.5 update_state_after_tool 함수

```python
def update_state_after_tool(tool_name: str, arguments: dict[str, Any], result: Any) -> None:
```

이 함수는 도구 실행 후 Task State를 갱신한다.

공통으로 저장하는 값은 다음과 같다.

```text
last_tool_name
last_tool_arguments
last_tool_result_summary
```

도구별로 추가 저장하는 값도 있다.

```text
file_reader:
- last_file_path
- last_action = file_read

search:
- last_search_query
- last_action = search

calculator:
- last_expression
- last_action = calculation
```

이렇게 저장해두면 다음 요청에서 이전 작업을 참조할 수 있다.

---

# Part C. 실행 및 결과 확인

---

## 18. 실행 방법

프로젝트 루트에서 실행할 경우:

```bash
PYTHONPATH=./labs/agent python labs/agent/03_memory_agent.py
```

또는 `labs/agent` 디렉터리로 이동해서 실행한다.

```bash
cd labs/agent
python 03_memory_agent.py
```

---

## 19. 실행 예시 1: 파일 읽기

입력:

```text
파일 읽어줘
```

예상 출력:

```text
================================================================================
Tool Call
================================================================================
{
  "tool_name": "file_reader",
  "arguments": {
    "relative_path": "sample_docs/agent_sample.md"
  }
}
================================================================================
Observation
================================================================================
# AI Agent 샘플 문서
...
================================================================================
Final Answer
================================================================================
파일 내용을 읽었습니다.
...
```

실행 후 Memory 파일을 확인한다.

```text
labs/agent/data/agent_memory.json
```

저장 예시는 다음과 같다.

```json
{
  "conversation": [
    {
      "role": "user",
      "content": "파일 읽어줘",
      "timestamp": "2026-06-29T10:30:00"
    },
    {
      "role": "assistant",
      "content": "파일 내용을 읽었습니다...",
      "timestamp": "2026-06-29T10:30:01"
    }
  ],
  "tool_history": [
    {
      "tool_name": "file_reader",
      "arguments": {
        "relative_path": "sample_docs/agent_sample.md"
      },
      "result": "# AI Agent 샘플 문서...",
      "status": "success",
      "timestamp": "2026-06-29T10:30:01"
    }
  ],
  "task_state": {
    "last_tool_name": "file_reader",
    "last_tool_arguments": {
      "relative_path": "sample_docs/agent_sample.md"
    },
    "last_tool_result_summary": "# AI Agent 샘플 문서...",
    "last_file_path": "sample_docs/agent_sample.md",
    "last_action": "file_read",
    "updated_at": "2026-06-29T10:30:01"
  }
}
```

---

## 20. 실행 예시 2: 방금 파일 다시 읽기

앞에서 파일을 읽은 뒤 다시 실행한다.

입력:

```text
방금 파일 다시 읽어줘
```

Agent는 Memory에서 `last_file_path`를 조회한다.

```json
"last_file_path": "sample_docs/agent_sample.md"
```

그리고 같은 파일을 다시 읽는다.

이 예시의 핵심은 다음이다.

```text
사용자는 파일 경로를 다시 말하지 않았다.
Agent는 Memory를 통해 이전 파일 경로를 찾아냈다.
```

이것이 Memory의 가장 기본적인 효과이다.

---

## 21. 실행 예시 3: 검색 이력 저장

입력:

```text
Agent 검색해줘
```

실행 후 Task State에는 다음 값이 저장된다.

```json
{
  "last_search_query": "Agent",
  "last_action": "search"
}
```

Tool History에는 검색 도구 실행 이력이 저장된다.

```json
{
  "tool_name": "search",
  "arguments": {
    "query": "Agent"
  },
  "status": "success"
}
```

---

## 22. 실행 예시 4: Memory 초기화

입력:

```text
메모리 초기화
```

예상 출력:

```text
Memory를 초기화했습니다.
```

Memory 파일은 다음 구조로 초기화된다.

```json
{
  "conversation": [],
  "tool_history": [],
  "task_state": {}
}
```

실습 중 상태가 꼬였을 때 초기화하면 된다.

---

# Part D. Memory 설계 관점

---

## 23. Memory에 무엇을 저장할 것인가?

Memory 설계에서 가장 중요한 질문은 다음이다.

```text
무엇을 저장할 것인가?
```

처음에는 모든 것을 저장하고 싶어질 수 있다.  
하지만 실제 운영 환경에서는 모든 것을 저장하면 안 된다.

저장해도 좋은 정보는 다음과 같다.

```text
1. 대화 이력
2. 도구 실행 로그
3. 작업 상태
4. 선택된 파일 경로
5. 검색어
6. 중간 결과 요약
7. 사용자가 명시적으로 저장을 요청한 설정
```

주의해야 할 정보는 다음과 같다.

```text
1. 개인정보
2. 비밀번호
3. API Key
4. 인증 토큰
5. 주민등록번호
6. 계좌번호
7. 민감한 업무 문서 원문
8. 외부 반출이 금지된 정보
```

---

## 24. Memory 원문 저장 vs 요약 저장

도구 실행 결과를 Memory에 저장할 때 두 가지 방식이 있다.

```text
1. 원문 전체 저장
2. 요약만 저장
```

원문 전체 저장의 장점은 다음과 같다.

```text
1. 나중에 다시 사용할 수 있다.
2. 결과 재현이 쉽다.
3. 디버깅에 유리하다.
```

단점은 다음과 같다.

```text
1. 저장 용량이 커진다.
2. 민감정보 노출 위험이 있다.
3. LLM Context에 넣기 어렵다.
4. 불필요한 정보가 많아질 수 있다.
```

요약 저장의 장점은 다음과 같다.

```text
1. 저장 용량이 작다.
2. LLM에 다시 넣기 쉽다.
3. 민감정보 노출 위험을 줄일 수 있다.
```

단점은 다음과 같다.

```text
1. 원문 재현이 어렵다.
2. 요약 과정에서 정보가 누락될 수 있다.
```

처음에는 다음 방식을 추천한다.

```text
Tool History:
- 실행 로그 중심으로 저장

Task State:
- 최근 결과 요약만 저장

원문:
- 필요할 때 다시 도구로 읽기
```

---

## 25. Memory와 Context Window

LLM에는 한 번에 입력할 수 있는 텍스트 길이 제한이 있다.  
이를 Context Window라고 한다.

대화 이력을 계속 누적해서 LLM에 전달하면 다음 문제가 생긴다.

```text
1. 입력 길이가 너무 길어진다.
2. 비용이 증가한다.
3. 응답 속도가 느려진다.
4. 중요한 정보가 뒤섞인다.
5. 오래된 정보가 현재 판단을 방해할 수 있다.
```

따라서 Memory를 LLM에 넣을 때는 선별이 필요하다.

대표적인 전략은 다음과 같다.

```text
1. 최근 대화 N개만 전달
2. 오래된 대화는 요약해서 전달
3. 현재 작업과 관련 있는 Memory만 검색해서 전달
4. 도구 실행 결과 원문 대신 요약만 전달
5. 중요 정보는 별도 key-value로 관리
```

---

## 26. Memory와 RAG의 관계

Memory와 RAG는 비슷해 보이지만 목적이 다르다.

| 구분 | Memory | RAG |
|---|---|---|
| 목적 | 대화와 작업 상태 유지 | 외부 문서 검색 |
| 저장 대상 | 사용자 대화, 작업 상태, 도구 이력 | 문서 Chunk, 지식 데이터 |
| 사용 시점 | 이어지는 대화와 작업 처리 | 질문에 필요한 근거 검색 |
| 데이터 성격 | 개인/세션/작업 중심 | 문서/지식 중심 |
| 예시 | 방금 읽은 파일, 이전 검색어 | 사내 매뉴얼, 제안서, 가이드 |

Agent에서는 Memory와 RAG를 함께 사용한다.

```text
Memory:
사용자가 방금 무엇을 했는지 기억한다.

RAG:
업무 문서에서 필요한 근거를 찾는다.
```

예시:

```text
사용자:
Step2 문서에서 ChromaDB 찾아줘.

Agent:
RAG 검색 실행
Memory에 검색어와 결과 요약 저장

사용자:
방금 찾은 내용을 표로 정리해줘.

Agent:
Memory에서 직전 검색 결과 확인
필요하면 RAG 재검색
표로 정리
```

---

## 27. Memory와 Workflow의 관계

Step3-5와 Step3-6에서는 Planning Agent와 LangGraph를 학습한다.  
이때 Memory는 Workflow의 State로 확장된다.

이번 문서의 Task State는 단순한 dictionary이다.

```json
{
  "last_file_path": "sample_docs/agent_sample.md",
  "last_action": "file_read"
}
```

LangGraph에서는 이런 상태가 Graph State로 발전한다.

```text
Graph State:
- 현재 노드
- 사용자 질문
- 검색 결과
- 도구 실행 결과
- 승인 여부
- 다음 이동할 노드
```

즉, 이번 문서에서 배우는 Memory는 이후 Workflow Agent의 기초가 된다.

---

## 28. Enterprise Memory 설계 원칙

기업 환경에서는 Memory를 설계할 때 다음 원칙을 지켜야 한다.

```text
1. 저장 목적을 명확히 한다.
2. 저장 기간을 정한다.
3. 민감정보는 저장하지 않거나 마스킹한다.
4. 사용자별 접근 권한을 적용한다.
5. 프로젝트별 Memory를 분리한다.
6. 도구 실행 로그는 감사 가능하게 저장한다.
7. 삭제 요청에 대응할 수 있어야 한다.
8. Memory를 LLM에 전달하기 전에 필터링한다.
9. 원문 저장과 요약 저장을 구분한다.
10. 운영 로그와 Agent Memory를 분리한다.
```

특히 다음 원칙이 중요하다.

> **Memory는 Agent 성능을 높이지만, 잘못 설계하면 보안 위험이 된다.**

---

## 29. Memory 저장소 선택

처음에는 JSON 파일로 충분하다.  
하지만 규모가 커지면 다른 저장소를 고려해야 한다.

| 저장소 | 특징 | 적합한 경우 |
|---|---|---|
| JSON 파일 | 단순하고 확인 쉬움 | 학습, 실습 |
| SQLite | 파일 기반 DB | 개인용 Agent, 소규모 실습 |
| PostgreSQL | 안정적인 관계형 DB | 운영 시스템 |
| Redis | 빠른 Key-Value 저장 | 세션 상태, 캐시 |
| Vector DB | 의미 기반 검색 | 장기 기억, 유사 기억 검색 |
| LangGraph Store | Agent State 관리 | Workflow Agent |
| Object Storage | 대용량 파일 저장 | 원문 파일, 로그 아카이브 |

이번 단계에서는 JSON 파일로 시작하고, 이후 다음 순서로 확장하는 것이 좋다.

```text
JSON
  ↓
SQLite
  ↓
PostgreSQL / Redis
  ↓
Vector DB
  ↓
LangGraph Store
```

---

## 30. 자주 발생하는 오류

---

### 30.1 Memory 파일이 생성되지 않는 경우

원인:

```text
1. data 디렉터리가 없다.
2. 파일 쓰기 권한이 없다.
3. save_memory 함수가 호출되지 않았다.
```

해결:

```bash
mkdir -p labs/agent/data
```

그리고 Agent 실행 후 다음 파일이 생성되었는지 확인한다.

```text
labs/agent/data/agent_memory.json
```

---

### 30.2 JSONDecodeError

오류 예시:

```text
json.decoder.JSONDecodeError
```

원인:

```text
agent_memory.json 파일이 깨졌거나 비어 있을 수 있다.
```

해결:

```text
1. agent_memory.json 파일을 삭제한다.
2. 다시 Agent를 실행한다.
3. 또는 메모리 초기화 기능을 실행한다.
```

파일 삭제:

```bash
rm labs/agent/data/agent_memory.json
```

---

### 30.3 이전 파일을 기억하지 못하는 경우

원인:

```text
1. 파일 읽기 도구가 실행되지 않았다.
2. update_state_after_tool 함수가 호출되지 않았다.
3. last_file_path가 저장되지 않았다.
4. Memory가 초기화되었다.
```

확인할 파일:

```text
labs/agent/data/agent_memory.json
```

확인할 값:

```json
"last_file_path": "sample_docs/agent_sample.md"
```

---

### 30.4 Memory가 너무 커지는 경우

원인:

```text
1. 도구 실행 결과 원문을 계속 저장한다.
2. 대화 이력을 정리하지 않는다.
3. 검색 결과가 너무 많이 저장된다.
```

해결:

```text
1. 오래된 대화 삭제
2. 오래된 대화 요약
3. 도구 결과는 요약만 저장
4. 저장 개수 제한
5. 중요 정보만 별도 저장
```

---

## 31. 핵심 정리

이번 문서의 핵심은 다음과 같다.

```text
1. Memory가 없는 Agent는 이전 대화와 작업 상태를 기억하지 못한다.
2. Agent Memory는 대화 이력, 도구 실행 이력, 작업 상태를 관리한다.
3. Short-term Memory는 현재 대화나 작업 안에서 유지되는 기억이다.
4. Long-term Memory는 세션을 넘어 유지되는 기억이다.
5. Conversation Memory는 대화 중심이고, Task State는 작업 중심이다.
6. Tool Execution History는 감사와 디버깅에 중요하다.
7. JSON 파일 기반 Memory는 학습용으로 이해하기 쉽다.
8. 운영 환경에서는 Memory 저장 대상과 보안 정책을 신중히 설계해야 한다.
9. Memory는 이후 Workflow Agent와 LangGraph State의 기초가 된다.
```

한 문장으로 정리하면 다음과 같다.

> **Agent Memory는 Agent가 이전 대화와 작업 상태를 기억하고, 이어지는 요청을 자연스럽게 처리하도록 만드는 상태 관리 구조이다.**

---

## 32. 다음 단계 예고

다음 문서는 다음과 같다.

```text
Step3-5. Planning Agent와 Workflow
docs/study/step3/step3_5_planning_and_workflow_agent_guide.md
```

다음 단계에서는 Agent가 단순히 도구를 호출하는 수준을 넘어, 복잡한 요청을 여러 단계로 나누고 실행 순서를 계획하는 방법을 학습한다.

다음 문서에서 다룰 내용은 다음과 같다.

```text
1. Planning이 필요한 이유
2. Task Decomposition
3. Plan-and-Execute 패턴
4. Reflection과 Self-Correction
5. Workflow 기반 Agent 개념
6. Memory와 Workflow State의 관계
7. Enterprise 업무 프로세스에 Agent를 적용하는 방식
```

---

## 33. 참고 자료

아래 자료는 Agent Memory 개념과 최신 프레임워크 관점을 이해하는 데 참고할 수 있다.

```text
LangChain Memory Concepts
https://docs.langchain.com/oss/python/concepts/memory

LangChain Short-term Memory
https://docs.langchain.com/oss/python/langchain/short-term-memory

OpenAI Agents SDK - Context Personalization
https://developers.openai.com/cookbook/examples/agents_sdk/context_personalization

OpenAI Agents SDK - Session Memory
https://developers.openai.com/cookbook/examples/agents_sdk/session_memory

LangGraph Long-term Memory Blog
https://www.langchain.com/blog/launching-long-term-memory-support-in-langgraph

Model Context Protocol 공식 문서
https://modelcontextprotocol.io/docs/getting-started/intro
```

---

## 34. 부록: ReAct와 Memory의 관계

Step3-2에서 ReAct를 다음 구조로 배웠다.

```text
Thought
  ↓
Action
  ↓
Observation
  ↓
Thought
  ↓
Final Answer
```

Memory가 추가되면 구조는 다음처럼 확장된다.

```text
Memory Load
  ↓
Thought
  ↓
Action
  ↓
Observation
  ↓
Memory Save
  ↓
Thought
  ↓
Final Answer
  ↓
Conversation Save
```

즉, Memory는 ReAct의 앞뒤에 붙는다.

```text
시작할 때:
이전 상태를 불러온다.

도구 실행 후:
결과와 상태를 저장한다.

답변 후:
대화 이력을 저장한다.
```

---

## 35. 부록: Step3-3 코드와 Step3-4 코드의 차이

| 구분 | Step3-3 | Step3-4 |
|---|---|---|
| 목적 | 첫 번째 Agent 구현 | Memory 추가 |
| 입력 처리 | 현재 질문만 사용 | 이전 상태도 참고 |
| 도구 실행 | 실행 후 출력 | 실행 후 이력 저장 |
| 상태 관리 | 없음 | Task State 저장 |
| 대화 이력 | 없음 | Conversation 저장 |
| 파일 참조 | 매번 직접 입력 | 마지막 파일 기억 |
| 저장소 | 없음 | JSON 파일 |

Step3-4의 핵심 변화는 다음이다.

```text
Agent가 한 번 실행되고 끝나는 구조에서,
이전 실행 결과를 기억하고 다음 실행에 활용하는 구조로 발전했다.
```

---

## 36. 부록: 향후 확장 방향

이번 Memory Agent는 다음 방향으로 확장할 수 있다.

```text
1. Conversation 최근 N개만 유지
2. 오래된 대화 자동 요약
3. SQLite Memory로 변경
4. 사용자별 Memory 분리
5. 프로젝트별 Memory 분리
6. Tool Result 원문과 요약 분리
7. 민감정보 마스킹
8. RAG 검색 결과 Memory 연동
9. LangGraph State로 확장
10. Long-term Memory Store 적용
```

이 확장 방향은 이후 Step3-5, Step3-6, Step3-10에서 다시 다룬다.

---
