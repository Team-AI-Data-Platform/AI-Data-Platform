# Step3-2. ReAct와 Tool Calling 가이드

> AI DATA Platform 연구 프로젝트  
> Step3. AI Agent  
> Part1. AI Agent 기초  
> 문서 경로: `docs/study/step3/step3_2_react_and_tool_calling_guide.md`  
> 작성일: 2026-06-29

---

## 1. 학습 목표

이 문서의 목표는 AI Agent의 핵심 동작 방식인 **ReAct**와 **Tool Calling**을 이해하는 것이다.

Step3-1에서 AI Agent가 무엇인지 개념적으로 살펴봤다면, Step3-2에서는 Agent가 실제로 어떻게 판단하고 행동하는지 학습한다.

이번 문서에서 다룰 핵심 질문은 다음과 같다.

```text
1. LLM은 왜 도구가 필요한가?
2. ReAct는 무엇인가?
3. Thought, Action, Observation 구조는 무엇인가?
4. Tool Calling은 무엇인가?
5. Function Calling과 Tool Calling은 어떤 관계인가?
6. Python에서는 도구를 어떻게 함수로 구현하는가?
7. Enterprise 환경에서는 Tool Calling을 어떻게 통제해야 하는가?
```

이 문서를 마치면 다음 내용을 설명할 수 있어야 한다.

```text
LLM은 답변을 생성할 수 있지만, 직접 파일을 읽거나 계산하거나 DB를 조회하지는 못한다.
Agent는 LLM의 판단 능력과 외부 도구 실행 능력을 결합한 구조이다.
ReAct는 생각과 행동을 반복하는 Agent 동작 패턴이다.
Tool Calling은 LLM이 필요한 도구를 구조화된 방식으로 호출하게 하는 방법이다.
```

---

## 2. 왜 필요한가?

LLM은 많은 지식을 가지고 있고 자연어 답변을 잘 생성한다.  
하지만 LLM만으로는 실제 업무를 처리하기 어렵다.

예를 들어 사용자가 다음과 같이 요청했다고 가정한다.

```text
"프로젝트 폴더에 있는 제안서 파일을 읽고 핵심 내용을 요약해줘."
```

LLM은 제안서 요약 방법을 설명할 수는 있지만, 실제 로컬 파일 시스템에 접근해서 파일을 읽지는 못한다.

또 다른 예를 보자.

```text
"지난달 장애 건수를 DB에서 조회해서 표로 정리해줘."
```

LLM은 SQL 예시를 만들어줄 수는 있지만, 실제 데이터베이스에 접속해서 결과를 가져오려면 별도의 도구가 필요하다.

즉, LLM은 다음과 같은 한계를 가진다.

```text
1. 최신 정보를 직접 조회하지 못한다.
2. 로컬 파일을 직접 읽지 못한다.
3. 데이터베이스를 직접 조회하지 못한다.
4. 계산은 가능하지만 정확성이 항상 보장되지는 않는다.
5. 외부 API를 직접 호출하지 못한다.
6. 운영 시스템에 직접 작업을 수행하지 못한다.
```

이 문제를 해결하기 위해 Agent는 LLM에게 **도구 사용 능력**을 부여한다.

---

## 3. 기존 방식의 한계

기존 챗봇 구조는 대략 다음과 같다.

```text
사용자 질문
   ↓
LLM
   ↓
답변 생성
```

이 구조는 간단한 질의응답에는 충분하다.  
하지만 실제 업무에서는 답변 생성만으로 끝나지 않는다.

업무 요청은 보통 다음 과정을 포함한다.

```text
1. 요청 의도 파악
2. 필요한 정보 확인
3. 외부 시스템 조회
4. 계산 또는 분석
5. 결과 정리
6. 보고서 작성
7. 필요 시 후속 작업 수행
```

기존 LLM 단독 구조에서는 3번 이후의 작업을 직접 수행하기 어렵다.

그래서 Agent 구조에서는 다음과 같이 바뀐다.

```text
사용자 질문
   ↓
LLM 판단
   ↓
필요한 도구 선택
   ↓
도구 실행
   ↓
실행 결과 확인
   ↓
최종 답변 생성
```

이때 중요한 개념이 바로 **ReAct**와 **Tool Calling**이다.

---

## 4. AI Agent가 해결하는 문제

AI Agent는 LLM이 가진 자연어 이해 능력과 외부 도구 실행 능력을 결합한다.

```text
LLM 단독:
- 질문을 이해한다.
- 답변을 생성한다.
- 하지만 실제 시스템 작업은 수행하지 못한다.

AI Agent:
- 질문을 이해한다.
- 필요한 작업을 판단한다.
- 도구를 선택한다.
- 도구를 실행한다.
- 실행 결과를 다시 해석한다.
- 최종 답변을 만든다.
```

예를 들어 다음 요청을 보자.

```text
"12,500원짜리 상품을 17개 구매하면 총액이 얼마야?"
```

LLM이 직접 계산할 수도 있지만, 더 안정적인 방식은 계산기 도구를 호출하는 것이다.

```text
사용자 질문
   ↓
Agent 판단: 계산이 필요하다.
   ↓
calculator 도구 호출
   ↓
결과: 212500
   ↓
최종 답변: 총액은 212,500원입니다.
```

이처럼 Agent는 LLM의 약점을 도구로 보완한다.

---

## 5. 핵심 개념

---

### 5.1 ReAct란 무엇인가?

ReAct는 **Reasoning + Acting**의 줄임말이다.

```text
Reasoning = 생각하기
Acting    = 행동하기
```

ReAct 방식에서는 LLM이 단순히 답변을 바로 생성하지 않는다.  
먼저 문제를 어떻게 해결할지 생각하고, 필요한 행동을 수행한 뒤, 그 결과를 다시 관찰한다.

기본 흐름은 다음과 같다.

```text
Thought
   ↓
Action
   ↓
Observation
   ↓
Thought
   ↓
Action
   ↓
Observation
   ↓
Final Answer
```

각 단계의 의미는 다음과 같다.

```text
Thought:
- 현재 문제를 어떻게 해결할지 생각하는 단계
- 어떤 정보가 필요한지 판단한다.

Action:
- 필요한 도구를 선택하고 호출하는 단계
- 예: 검색, 계산, 파일 읽기, DB 조회

Observation:
- 도구 실행 결과를 확인하는 단계
- 결과가 충분한지, 추가 작업이 필요한지 판단한다.

Final Answer:
- 모든 판단과 실행 결과를 바탕으로 최종 답변을 생성한다.
```

ReAct는 2022년에 발표된 논문인 **ReAct: Synergizing Reasoning and Acting in Language Models**에서 널리 알려졌다.  
이 논문은 LLM이 추론 과정과 행동을 번갈아 수행하도록 하면, 외부 지식이나 환경과 상호작용하면서 더 나은 문제 해결이 가능하다는 점을 제안했다.

---

### 5.2 ReAct 예시

사용자 질문이 다음과 같다고 하자.

```text
"세종대왕이 태어난 해와 이순신 장군이 태어난 해의 차이는 몇 년이야?"
```

Agent는 바로 답을 만들 수도 있지만, 정확한 처리를 위해 다음과 같이 동작할 수 있다.

```text
Thought:
두 인물의 출생 연도를 알아야 한다.

Action:
search("세종대왕 출생 연도")

Observation:
세종대왕은 1397년에 태어났다.

Thought:
이순신 장군의 출생 연도도 필요하다.

Action:
search("이순신 출생 연도")

Observation:
이순신은 1545년에 태어났다.

Thought:
1545 - 1397을 계산해야 한다.

Action:
calculator("1545 - 1397")

Observation:
148

Final Answer:
세종대왕과 이순신 장군의 출생 연도 차이는 148년입니다.
```

이 예시는 ReAct의 핵심을 잘 보여준다.

```text
1. 생각한다.
2. 필요한 도구를 사용한다.
3. 결과를 관찰한다.
4. 다시 생각한다.
5. 최종 답변을 만든다.
```

---

### 5.3 Tool Calling이란 무엇인가?

Tool Calling은 LLM이 외부 도구를 호출할 수 있게 하는 방식이다.

여기서 도구는 반드시 거창한 시스템일 필요가 없다.  
Python 함수 하나도 도구가 될 수 있다.

예를 들면 다음과 같다.

```text
계산기 도구
- 입력: 수식
- 출력: 계산 결과

파일 읽기 도구
- 입력: 파일 경로
- 출력: 파일 내용

검색 도구
- 입력: 검색어
- 출력: 검색 결과

DB 조회 도구
- 입력: SQL 또는 조회 조건
- 출력: 조회 결과

메일 발송 도구
- 입력: 수신자, 제목, 본문
- 출력: 발송 결과
```

Tool Calling 구조에서는 LLM이 도구를 직접 실행하는 것이 아니라, **도구 호출 요청을 구조화된 형태로 생성**한다.  
실제 실행은 애플리케이션 코드가 담당한다.

---

### 5.4 Tool Calling의 기본 흐름

```text
사용자 요청
   ↓
LLM
   ↓
도구 호출 필요 여부 판단
   ↓
도구명과 입력값 생성
   ↓
애플리케이션이 도구 실행
   ↓
실행 결과를 LLM에게 다시 전달
   ↓
LLM이 최종 답변 생성
```

예를 들어 계산기 도구를 사용할 경우 흐름은 다음과 같다.

```text
사용자:
"10000 * 1.1 계산해줘."

LLM:
calculator 도구를 호출해야 한다.
입력값은 {"expression": "10000 * 1.1"} 이다.

애플리케이션:
calculator("10000 * 1.1") 실행

도구 결과:
11000

LLM:
계산 결과는 11,000입니다.
```

---

### 5.5 Function Calling과 Tool Calling의 관계

예전에는 LLM이 외부 함수를 호출하는 기능을 주로 **Function Calling**이라고 불렀다.  
최근에는 더 넓은 의미로 **Tool Calling**이라는 표현을 많이 사용한다.

차이를 단순화하면 다음과 같다.

```text
Function Calling:
- LLM이 특정 함수를 호출하도록 구조화된 요청을 생성하는 방식
- 함수 이름과 파라미터가 중요하다.

Tool Calling:
- Function Calling을 포함하는 더 넓은 개념
- 함수뿐 아니라 검색, 파일, 코드 실행, MCP, 웹 검색, DB 조회 등 다양한 도구를 포함한다.
```

즉, Function Calling은 Tool Calling의 한 형태라고 이해하면 된다.

---

### 5.6 Tool Schema란 무엇인가?

Tool Schema는 LLM에게 도구의 사용 방법을 알려주는 설명서이다.

도구를 잘 호출하려면 LLM은 다음 정보를 알아야 한다.

```text
1. 도구 이름
2. 도구 설명
3. 언제 사용해야 하는지
4. 입력 파라미터
5. 각 파라미터의 타입
6. 필수값 여부
7. 반환 결과의 의미
```

예를 들어 계산기 도구의 Schema는 다음과 같이 표현할 수 있다.

```json
{
  "name": "calculator",
  "description": "수학 계산이 필요할 때 사용하는 도구입니다.",
  "parameters": {
    "type": "object",
    "properties": {
      "expression": {
        "type": "string",
        "description": "계산할 수식입니다. 예: 10000 * 1.1"
      }
    },
    "required": ["expression"]
  }
}
```

Schema가 명확해야 LLM이 도구를 정확하게 호출할 수 있다.

---

## 6. 전체 아키텍처

ReAct와 Tool Calling을 포함한 단일 Agent 구조는 다음과 같다.

```text
사용자
  │
  ▼
Agent Application
  │
  ├─ Prompt
  ├─ Tool Schema
  ├─ Conversation History
  └─ Agent Loop
        │
        ▼
      LLM
        │
        ├─ 일반 답변
        │
        └─ Tool Call 요청
                │
                ▼
            Tool Executor
                │
      ┌─────────┼─────────┐
      ▼         ▼         ▼
 calculator  file_reader  search
      │         │         │
      └─────────┼─────────┘
                ▼
          Tool Result
                │
                ▼
              LLM
                │
                ▼
            Final Answer
```

이 구조에서 핵심은 **LLM과 도구 실행 코드를 분리하는 것**이다.

LLM은 판단한다.

```text
"어떤 도구가 필요한가?"
"도구에 어떤 값을 넘겨야 하는가?"
"도구 결과를 어떻게 해석해야 하는가?"
```

애플리케이션은 실행한다.

```text
"도구 호출 요청을 파싱한다."
"허용된 도구인지 확인한다."
"도구를 실행한다."
"결과를 LLM에게 전달한다."
```

---

## 7. 동작 과정

Tool Calling 기반 Agent의 일반적인 실행 과정은 다음과 같다.

```text
1. 사용자 질문 입력
2. Agent가 사용 가능한 도구 목록을 LLM에게 전달
3. LLM이 질문을 분석
4. LLM이 도구 호출 필요 여부 판단
5. 도구가 필요 없으면 바로 답변 생성
6. 도구가 필요하면 도구명과 입력값 생성
7. 애플리케이션이 도구 호출 요청을 검증
8. 실제 Python 함수 실행
9. 실행 결과를 LLM에게 전달
10. LLM이 결과를 해석
11. 추가 도구 호출이 필요하면 반복
12. 충분하면 최종 답변 생성
```

이를 Agent Loop라고 부른다.

```text
while 작업이 끝나지 않음:
    LLM에게 현재 상태 전달
    LLM 응답 확인

    if 도구 호출 요청:
        도구 실행
        결과를 대화에 추가
    else:
        최종 답변 반환
        break
```

---

## 8. 실습 준비

이번 실습에서는 복잡한 라이브러리 없이 Python 기본 코드로 Tool Calling 개념을 이해한다.

### 8.1 실습 디렉터리

프로젝트 루트에서 아래 구조를 사용한다.

```text
labs
└── agent
    ├── tools
    │   ├── calculator.py
    │   ├── file_reader.py
    │   └── search.py
    │
    └── 02_tool_calling.py
```

### 8.2 디렉터리 생성

```bash
mkdir -p labs/agent/tools
```

### 8.3 실습 목표

이번 실습의 목표는 다음과 같다.

```text
1. Python 함수를 도구로 만든다.
2. 도구 목록을 딕셔너리로 관리한다.
3. 사용자 질문에 따라 도구를 선택한다.
4. 도구 실행 결과를 최종 답변에 반영한다.
```

이번 단계에서는 실제 LLM API를 연결하기 전에, 규칙 기반으로 도구 호출 흐름을 먼저 이해한다.

---

## 9. Python 실습

---

### 9.1 계산기 도구 만들기

파일 경로:

```text
labs/agent/tools/calculator.py
```

코드:

```python
from __future__ import annotations


def calculate(expression: str) -> str:
    """
    문자열로 전달된 간단한 수식을 계산한다.

    주의:
    eval()은 임의의 Python 코드를 실행할 수 있기 때문에 실제 운영 환경에서는 위험하다.
    여기서는 Tool Calling 개념을 설명하기 위한 실습용 예제로만 사용한다.

    Args:
        expression:
            계산할 수식 문자열.
            예: "10000 * 1.1"

    Returns:
        계산 결과를 문자열로 반환한다.
    """
    if not expression or not expression.strip():
        raise ValueError("계산할 수식이 비어 있습니다.")

    allowed_chars = "0123456789+-*/(). "

    if any(char not in allowed_chars for char in expression):
        raise ValueError("허용되지 않은 문자가 포함되어 있습니다.")

    result = eval(expression, {"__builtins__": {}}, {})

    return str(result)
```

---

### 9.2 파일 읽기 도구 만들기

파일 경로:

```text
labs/agent/tools/file_reader.py
```

코드:

```python
from __future__ import annotations

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]


def read_text_file(relative_path: str) -> str:
    """
    프로젝트 내부의 텍스트 파일을 읽는다.

    Args:
        relative_path:
            프로젝트 루트를 기준으로 한 상대 경로.
            예: "docs/index.md"

    Returns:
        파일 내용을 문자열로 반환한다.
    """
    if not relative_path or not relative_path.strip():
        raise ValueError("파일 경로가 비어 있습니다.")

    target_path = (BASE_DIR / relative_path).resolve()

    if not str(target_path).startswith(str(BASE_DIR)):
        raise ValueError("프로젝트 디렉터리 밖의 파일은 읽을 수 없습니다.")

    if not target_path.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {target_path}")

    if not target_path.is_file():
        raise ValueError(f"파일이 아닙니다: {target_path}")

    return target_path.read_text(encoding="utf-8")
```

---

### 9.3 간단한 검색 도구 만들기

파일 경로:

```text
labs/agent/tools/search.py
```

코드:

```python
from __future__ import annotations


DOCUMENTS = [
    {
        "title": "AI Agent 개요",
        "content": "AI Agent는 목표를 이해하고 도구를 사용하여 작업을 수행하는 AI 시스템이다.",
    },
    {
        "title": "RAG 개요",
        "content": "RAG는 외부 문서를 검색하여 LLM 답변의 근거로 사용하는 방식이다.",
    },
    {
        "title": "Tool Calling",
        "content": "Tool Calling은 LLM이 계산기, 검색, 파일 읽기 같은 외부 도구를 호출하는 방식이다.",
    },
]


def search_documents(query: str) -> list[dict[str, str]]:
    """
    샘플 문서 목록에서 검색어가 포함된 문서를 찾는다.

    Args:
        query:
            검색어.

    Returns:
        검색된 문서 목록.
    """
    if not query or not query.strip():
        raise ValueError("검색어가 비어 있습니다.")

    normalized_query = query.lower()

    results = []

    for document in DOCUMENTS:
        title = document["title"].lower()
        content = document["content"].lower()

        if normalized_query in title or normalized_query in content:
            results.append(document)

    return results
```

---

### 9.4 Tool Calling 실행 파일 만들기

파일 경로:

```text
labs/agent/02_tool_calling.py
```

코드:

```python
from __future__ import annotations

import json
from typing import Any, Callable

from tools.calculator import calculate
from tools.file_reader import read_text_file
from tools.search import search_documents


ToolFunction = Callable[..., Any]


TOOLS: dict[str, ToolFunction] = {
    "calculator": calculate,
    "file_reader": read_text_file,
    "search": search_documents,
}


TOOL_SCHEMAS: list[dict[str, Any]] = [
    {
        "name": "calculator",
        "description": "수학 계산이 필요할 때 사용한다.",
        "parameters": {
            "expression": "계산할 수식 문자열. 예: 10000 * 1.1"
        },
    },
    {
        "name": "file_reader",
        "description": "프로젝트 내부 텍스트 파일을 읽을 때 사용한다.",
        "parameters": {
            "relative_path": "프로젝트 루트 기준 상대 경로. 예: docs/index.md"
        },
    },
    {
        "name": "search",
        "description": "샘플 문서 목록에서 키워드를 검색할 때 사용한다.",
        "parameters": {
            "query": "검색어"
        },
    },
]


def print_tool_schemas() -> None:
    """
    현재 Agent가 사용할 수 있는 도구 목록을 출력한다.
    """
    print("=" * 80)
    print("사용 가능한 도구 목록")
    print("=" * 80)

    for tool in TOOL_SCHEMAS:
        print(f"- 도구명: {tool['name']}")
        print(f"  설명: {tool['description']}")
        print(f"  파라미터: {tool['parameters']}")
        print()


def simple_tool_selector(user_input: str) -> dict[str, Any]:
    """
    사용자 입력을 보고 어떤 도구를 호출할지 결정한다.

    실제 Agent에서는 LLM이 이 판단을 수행한다.
    여기서는 실습을 위해 단순한 규칙 기반으로 구현한다.
    """
    text = user_input.strip()

    if "계산" in text or any(op in text for op in ["+", "-", "*", "/"]):
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

    if "파일" in text and "읽" in text:
        return {
            "tool_name": "file_reader",
            "arguments": {
                "relative_path": "docs/index.md"
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

    return {
        "tool_name": "",
        "arguments": {},
    }


def execute_tool(tool_name: str, arguments: dict[str, Any]) -> Any:
    """
    도구 이름과 입력값을 받아 실제 Python 함수를 실행한다.
    """
    if tool_name not in TOOLS:
        raise ValueError(f"등록되지 않은 도구입니다: {tool_name}")

    tool_function = TOOLS[tool_name]

    return tool_function(**arguments)


def main() -> None:
    print_tool_schemas()

    user_input = input("질문을 입력하세요: ").strip()

    if not user_input:
        print("질문이 비어 있습니다.")
        return

    tool_call = simple_tool_selector(user_input)

    tool_name = tool_call["tool_name"]
    arguments = tool_call["arguments"]

    if not tool_name:
        print("도구 호출 없이 일반 답변을 생성해야 합니다.")
        print("이번 실습에서는 일반 답변 생성은 구현하지 않았습니다.")
        return

    print("=" * 80)
    print("Tool Call 요청")
    print("=" * 80)
    print(json.dumps(tool_call, ensure_ascii=False, indent=2))

    try:
        result = execute_tool(tool_name, arguments)

        print("=" * 80)
        print("Tool 실행 결과")
        print("=" * 80)
        print(result)

    except Exception as error:
        print("=" * 80)
        print("Tool 실행 오류")
        print("=" * 80)
        print(error)


if __name__ == "__main__":
    main()
```

---

## 10. 코드 분석

---

### 10.1 TOOLS 딕셔너리

```python
TOOLS: dict[str, ToolFunction] = {
    "calculator": calculate,
    "file_reader": read_text_file,
    "search": search_documents,
}
```

이 코드는 도구 이름과 실제 Python 함수를 연결한다.

```text
"calculator"  → calculate 함수
"file_reader" → read_text_file 함수
"search"      → search_documents 함수
```

Agent가 `"calculator"`라는 도구를 호출하겠다고 판단하면, 실제로는 `calculate()` 함수가 실행된다.

---

### 10.2 TOOL_SCHEMAS

```python
TOOL_SCHEMAS: list[dict[str, Any]] = [
    ...
]
```

`TOOL_SCHEMAS`는 LLM에게 알려줄 도구 설명이다.

실제 Tool Calling API에서는 이 정보가 매우 중요하다.  
LLM은 도구 이름만 보고 판단하지 않는다.  
도구 설명, 파라미터 설명, 필수값 여부를 보고 어떤 도구를 호출할지 판단한다.

---

### 10.3 simple_tool_selector 함수

```python
def simple_tool_selector(user_input: str) -> dict[str, Any]:
```

이 함수는 사용자의 입력을 보고 어떤 도구를 호출할지 결정한다.

실제 Agent에서는 이 판단을 LLM이 수행한다.  
하지만 처음부터 LLM API를 연결하면 구조가 복잡해질 수 있으므로, 이번 실습에서는 규칙 기반으로 단순하게 구현한다.

예를 들어 입력에 `"계산"`이라는 단어가 있으면 계산기 도구를 선택한다.

```python
if "계산" in text or any(op in text for op in ["+", "-", "*", "/"]):
```

---

### 10.4 execute_tool 함수

```python
def execute_tool(tool_name: str, arguments: dict[str, Any]) -> Any:
```

이 함수는 도구 이름과 입력값을 받아 실제 함수를 실행한다.

```python
tool_function = TOOLS[tool_name]
return tool_function(**arguments)
```

여기서 `**arguments`는 딕셔너리의 값을 함수의 키워드 인자로 풀어서 전달한다.

예를 들어 다음 딕셔너리가 있다고 하자.

```python
arguments = {
    "expression": "10000 * 1.1"
}
```

다음 코드는

```python
calculate(**arguments)
```

아래 코드와 같다.

```python
calculate(expression="10000 * 1.1")
```

---

## 11. 실행 결과

---

### 11.1 계산기 도구 실행

실행 명령:

```bash
python labs/agent/02_tool_calling.py
```

입력:

```text
10000 * 1.1 계산해줘
```

예상 결과:

```text
================================================================================
Tool Call 요청
================================================================================
{
  "tool_name": "calculator",
  "arguments": {
    "expression": "10000 * 1.1"
  }
}
================================================================================
Tool 실행 결과
================================================================================
11000.0
```

---

### 11.2 검색 도구 실행

입력:

```text
Tool Calling 검색해줘
```

예상 결과:

```text
================================================================================
Tool Call 요청
================================================================================
{
  "tool_name": "search",
  "arguments": {
    "query": "Tool Calling"
  }
}
================================================================================
Tool 실행 결과
================================================================================
[{'title': 'Tool Calling', 'content': 'Tool Calling은 LLM이 계산기, 검색, 파일 읽기 같은 외부 도구를 호출하는 방식이다.'}]
```

---

### 11.3 파일 읽기 도구 실행

입력:

```text
파일 읽어줘
```

예상 결과:

```text
================================================================================
Tool Call 요청
================================================================================
{
  "tool_name": "file_reader",
  "arguments": {
    "relative_path": "docs/index.md"
  }
}
================================================================================
Tool 실행 결과
================================================================================
...
```

단, `docs/index.md` 파일이 실제로 존재해야 정상 실행된다.

---

## 12. Enterprise 적용 사례

---

### 12.1 사내 문서 검색 Agent

사내 문서 검색 Agent는 다음 도구를 사용할 수 있다.

```text
1. 문서 목록 조회 도구
2. 파일 읽기 도구
3. RAG 검색 도구
4. 요약 도구
5. 출처 정리 도구
```

사용자 요청:

```text
"Step2 RAG 문서에서 ChromaDB 관련 내용을 찾아서 요약해줘."
```

Agent 동작:

```text
1. RAG 검색 도구 호출
2. ChromaDB 관련 Chunk 검색
3. 검색 결과를 LLM에게 전달
4. 요약 생성
5. 출처 표시
```

---

### 12.2 장애 보고서 작성 Agent

장애 보고서 작성 Agent는 다음 도구를 사용할 수 있다.

```text
1. Jira 조회 도구
2. Git Commit 조회 도구
3. 로그 검색 도구
4. 장애 이력 DB 조회 도구
5. 보고서 생성 도구
```

사용자 요청:

```text
"지난주 장애 내역을 보고서 초안으로 정리해줘."
```

Agent 동작:

```text
1. Jira에서 장애 티켓 조회
2. 장애 발생 시간과 조치 시간 확인
3. 관련 Git Commit 조회
4. 원인과 조치 내용 요약
5. 보고서 초안 작성
```

---

### 12.3 운영 점검 Agent

운영 점검 Agent는 다음 도구를 사용할 수 있다.

```text
1. Docker 상태 확인 도구
2. Ollama 상태 확인 도구
3. Open WebUI 상태 확인 도구
4. Vector DB 상태 확인 도구
5. 디스크 사용량 확인 도구
```

사용자 요청:

```text
"AI 플랫폼 상태 점검해줘."
```

Agent 동작:

```text
1. Docker 컨테이너 상태 확인
2. Ollama 모델 상태 확인
3. Open WebUI 접속 상태 확인
4. ChromaDB 파일 경로 확인
5. 종합 상태 보고
```

---

## 13. Best Practice

---

### 13.1 도구 이름은 명확하게 작성한다

좋은 예:

```text
read_text_file
search_documents
calculate_expression
query_customer_by_id
```

나쁜 예:

```text
run
do
process
handle
```

도구 이름만 봐도 어떤 일을 하는지 알 수 있어야 한다.

---

### 13.2 도구 설명은 구체적으로 작성한다

LLM은 도구 설명을 보고 도구 사용 여부를 판단한다.

좋은 설명:

```text
프로젝트 내부의 UTF-8 텍스트 파일을 읽을 때 사용한다.
프로젝트 루트 밖의 파일은 읽을 수 없다.
```

나쁜 설명:

```text
파일 도구입니다.
```

---

### 13.3 읽기 도구와 쓰기 도구를 분리한다

Enterprise 환경에서는 반드시 읽기 도구와 쓰기 도구를 구분해야 한다.

```text
읽기 도구:
- 파일 읽기
- DB 조회
- 상태 조회
- 검색

쓰기 도구:
- 파일 생성
- DB 수정
- 메일 발송
- 티켓 생성
- 배포 실행
```

쓰기 도구는 승인 절차를 거치는 것이 좋다.

---

### 13.4 위험한 도구는 기본 비활성화한다

다음 도구는 특히 조심해야 한다.

```text
1. Shell 실행 도구
2. 파일 삭제 도구
3. DB 수정 도구
4. 메일 발송 도구
5. 외부 API 호출 도구
6. 배포 실행 도구
```

처음에는 읽기 전용 도구부터 시작하는 것이 안전하다.

---

### 13.5 도구 실행 로그를 남긴다

Agent가 어떤 도구를 언제, 어떤 입력값으로 호출했는지 기록해야 한다.

로그 예시:

```json
{
  "timestamp": "2026-06-29T09:30:00+09:00",
  "user": "jangkwan",
  "tool_name": "search_documents",
  "arguments": {
    "query": "ChromaDB"
  },
  "status": "success"
}
```

운영 환경에서는 이 로그가 장애 분석과 감사에 중요하다.

---

## 14. 트러블슈팅

---

### 14.1 도구를 잘못 선택하는 경우

원인:

```text
1. 도구 설명이 모호하다.
2. 비슷한 도구가 너무 많다.
3. 프롬프트에 도구 사용 기준이 없다.
```

해결:

```text
1. 도구 설명을 더 구체적으로 작성한다.
2. 도구 이름을 명확하게 바꾼다.
3. 언제 어떤 도구를 사용해야 하는지 예시를 추가한다.
```

---

### 14.2 파라미터가 잘못 들어오는 경우

원인:

```text
1. 파라미터 설명이 부족하다.
2. 타입 정보가 명확하지 않다.
3. 필수값 정의가 없다.
```

해결:

```text
1. JSON Schema를 명확하게 작성한다.
2. 필수 파라미터를 지정한다.
3. 예시 입력값을 추가한다.
4. 실행 전에 입력값 검증을 수행한다.
```

---

### 14.3 도구 실행 중 오류가 나는 경우

원인:

```text
1. 파일이 존재하지 않는다.
2. 권한이 없다.
3. API Key가 없다.
4. 네트워크 오류가 발생했다.
5. 입력값 형식이 잘못되었다.
```

해결:

```text
1. 예외 처리를 추가한다.
2. 사용자에게 이해 가능한 오류 메시지를 반환한다.
3. 실행 로그를 남긴다.
4. 재시도 가능한 오류와 불가능한 오류를 구분한다.
```

---

### 14.4 Agent가 도구를 너무 자주 호출하는 경우

원인:

```text
1. 도구 사용 기준이 너무 느슨하다.
2. 프롬프트에서 항상 도구를 쓰라고 지시했다.
3. 이미 답변 가능한 질문에도 도구를 호출한다.
```

해결:

```text
1. 도구가 필요한 경우와 필요 없는 경우를 명확히 구분한다.
2. 안정적인 일반 지식 질문은 직접 답변하도록 한다.
3. 최신 정보, 파일, 계산, DB 조회가 필요할 때만 도구를 사용하도록 한다.
```

---

## 15. 핵심 정리

이번 문서의 핵심은 다음과 같다.

```text
1. LLM은 답변을 생성하지만, 실제 시스템 작업은 도구가 수행한다.
2. ReAct는 생각과 행동을 반복하는 Agent 동작 패턴이다.
3. Thought는 판단, Action은 도구 호출, Observation은 결과 확인이다.
4. Tool Calling은 LLM이 외부 도구를 구조화된 방식으로 호출하게 하는 방법이다.
5. Function Calling은 Tool Calling의 한 형태로 이해할 수 있다.
6. Tool Schema는 LLM에게 도구 사용법을 알려주는 설명서이다.
7. 실제 도구 실행은 LLM이 아니라 애플리케이션 코드가 담당한다.
8. Enterprise 환경에서는 권한, 로그, 승인, 보안 통제가 반드시 필요하다.
```

한 문장으로 정리하면 다음과 같다.

> **ReAct는 Agent가 생각하고 행동하는 방식이고, Tool Calling은 그 행동을 실제 도구 실행으로 연결하는 기술이다.**

---

## 16. 다음 단계 예고

다음 문서는 다음과 같다.

```text
Step3-3. 첫 번째 AI Agent 구현
docs/study/step3/step3_3_first_ai_agent_guide.md
```

Step3-3에서는 이번 문서에서 배운 Tool Calling 개념을 바탕으로, 실제로 첫 번째 AI Agent를 구현한다.

다음 단계에서는 다음 내용을 다룬다.

```text
1. Agent 실행 루프 구현
2. LLM 호출 구조 작성
3. 도구 호출 결과를 프롬프트에 다시 반영
4. 최종 답변 생성
5. 코드에 상세 주석 추가
```

---

## 17. 참고 자료

아래 자료는 ReAct와 Tool Calling 개념을 이해하기 위한 참고 자료이다.

```text
ReAct: Synergizing Reasoning and Acting in Language Models
https://arxiv.org/abs/2210.03629

Google Research Blog - ReAct: Synergizing Reasoning and Acting in Language Models
https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/

OpenAI Function Calling Guide
https://platform.openai.com/docs/guides/function-calling

LangChain Tools Documentation
https://docs.langchain.com/oss/python/langchain/tools

LangChain Agents Documentation
https://docs.langchain.com/oss/python/langchain/agents

Anthropic Tool Use Documentation
https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview
```

---
