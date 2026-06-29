# Step3-3. 첫 번째 AI Agent 구현 가이드

> AI DATA Platform 연구 프로젝트  
> Step3. AI Agent  
> Part1. AI Agent 기초  
> 문서 경로: `docs/study/step3/step3_3_first_ai_agent_guide.md`  
> 작성일: 2026-06-29

---

## 1. 문서 목적

이 문서는 `Step3-2. ReAct와 Tool Calling`에서 학습한 개념을 바탕으로, Python으로 **첫 번째 AI Agent 구조**를 직접 구현하기 위한 가이드 문서이다.

앞 단계에서는 다음 내용을 개념적으로 학습했다.

```text
1. ReAct
2. Thought / Action / Observation
3. Tool Calling
4. Tool Schema
5. Tool Executor
6. Tool Registry
```

이번 단계에서는 이 개념을 실제 코드 구조로 옮긴다.

단, 이번 문서의 목표는 완성형 Agent Framework를 만드는 것이 아니다.  
LangGraph, MCP, Multi Agent 같은 고급 구조는 뒤 단계에서 다룬다.

이번 단계의 목표는 다음과 같다.

```text
LLM이 도구를 사용할 수 있다는 구조를 이해하기 위해,
가장 단순한 Agent 실행 흐름을 Python 코드로 직접 구현한다.
```

---

## 2. 이번 문서의 위치

전체 Step3 목차에서 이 문서의 위치는 다음과 같다.

```text
Step3. AI Agent
│
├─ Part1. AI Agent 기초
│   ├─ Step3-1. AI Agent 개요
│   ├─ Step3-2. ReAct와 Tool Calling
│   ├─ Step3-3. 첫 번째 AI Agent 구현   ← 현재 문서
│   └─ Step3-4. Agent Memory와 상태 관리
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

Step3-3은 **이론에서 구현으로 넘어가는 첫 번째 실습 문서**이다.

```text
Step3-1:
AI Agent의 큰 그림 이해

Step3-2:
ReAct와 Tool Calling 동작 원리 이해

Step3-3:
첫 번째 Agent를 Python 코드로 구현

Step3-4:
Agent가 대화와 작업 상태를 기억하도록 확장
```

---

## 3. 학습 목표

이 문서를 마치면 다음 내용을 이해하고 직접 실행할 수 있어야 한다.

```text
1. Python 함수 하나가 Agent Tool이 될 수 있음을 이해한다.
2. 여러 도구를 Tool Registry로 관리할 수 있다.
3. Tool Schema가 도구 설명서 역할을 한다는 것을 이해한다.
4. Tool Call 요청을 받아 실제 도구를 실행하는 Tool Executor를 구현할 수 있다.
5. 사용자 질문을 분석하여 필요한 도구를 선택하는 흐름을 이해한다.
6. 첫 번째 단일 Agent 실행 구조를 만들 수 있다.
7. ReAct의 Thought / Action / Observation 흐름이 코드에서 어떻게 표현되는지 이해한다.
```

---

## 4. 이번 실습에서 만들 구조

이번 실습에서는 다음 구조를 만든다.

```text
사용자 질문
   ↓
질문 분석
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

이번 단계에서는 실제 LLM API를 바로 연결하지 않고, 먼저 **규칙 기반 Agent**로 구현한다.

이유는 다음과 같다.

```text
1. Agent 구조를 먼저 이해하기 위해서이다.
2. LLM API 연결 전에 Tool Registry와 Executor 개념을 명확히 하기 위해서이다.
3. 실행 흐름을 눈으로 확인하기 쉽기 때문이다.
4. 오류가 발생했을 때 원인을 쉽게 찾기 위해서이다.
```

즉, 이번 문서에서는 LLM 대신 간단한 규칙 기반 판단 함수를 사용한다.

```text
사용자 입력에 "계산"이 있으면 calculator 도구 사용
사용자 입력에 "검색"이 있으면 search 도구 사용
사용자 입력에 "파일"이 있으면 file_reader 도구 사용
```

이후 문서에서는 이 판단 역할을 LLM으로 바꿔 나갈 수 있다.

---

## 5. 최종 실습 디렉터리 구조

이번 문서에서 만들 디렉터리 구조는 다음과 같다.

```text
labs
└── agent
    ├── README.md
    │
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
    ├── sample_docs
    │   └── agent_sample.md
    │
    ├── 01_first_agent.py
    └── 02_tool_calling.py
```

각 파일의 역할은 다음과 같다.

| 파일 | 역할 |
|---|---|
| `tools/calculator.py` | 계산 도구 |
| `tools/search.py` | 샘플 문서 검색 도구 |
| `tools/file_reader.py` | 프로젝트 내부 파일 읽기 도구 |
| `common/tool_registry.py` | 사용 가능한 도구 목록과 Schema 관리 |
| `common/tool_executor.py` | Tool Call 요청을 받아 실제 도구 실행 |
| `sample_docs/agent_sample.md` | 파일 읽기 실습용 샘플 문서 |
| `01_first_agent.py` | 가장 단순한 Agent 실행 예제 |
| `02_tool_calling.py` | Tool Registry와 Executor를 사용하는 Agent 예제 |

---

## 6. 실습 준비

프로젝트 루트에서 아래 명령을 실행한다.

```bash
mkdir -p labs/agent/tools
mkdir -p labs/agent/common
mkdir -p labs/agent/sample_docs

touch labs/agent/tools/__init__.py
touch labs/agent/common/__init__.py
```

`__init__.py` 파일은 해당 디렉터리를 Python 패키지처럼 사용할 수 있게 해준다.

```text
tools/
common/
```

디렉터리 안에 `__init__.py`가 있으면 다음과 같은 import 문을 사용할 수 있다.

```python
from tools.calculator import calculate
from common.tool_executor import execute_tool
```

---

## 7. 샘플 문서 만들기

파일 경로:

```text
labs/agent/sample_docs/agent_sample.md
```

내용:

```markdown
# AI Agent 샘플 문서

AI Agent는 사용자의 목표를 이해하고, 필요한 도구를 선택하여 작업을 수행하는 AI 시스템이다.

일반 Chatbot은 사용자의 질문에 답변을 생성하는 데 집중한다.

RAG는 외부 문서를 검색하여 LLM 답변의 근거로 활용한다.

AI Agent는 RAG를 포함한 여러 도구를 사용하여 실제 업무 흐름을 수행할 수 있다.

예를 들어 Agent는 문서를 검색하고, 파일을 읽고, 계산을 수행하고, 결과를 요약할 수 있다.
```

이 문서는 파일 읽기 도구 테스트에 사용한다.

---

# Part A. Tool 만들기

Agent가 사용할 첫 번째 도구들을 만든다.

이번 실습에서는 세 가지 도구를 만든다.

```text
1. calculator
2. search
3. file_reader
```

---

## 8. 계산기 도구 만들기

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

    이 함수는 Agent가 사용할 수 있는 첫 번째 Tool이다.

    Args:
        expression:
            계산할 수식 문자열.
            예: "12500 * 17"

    Returns:
        계산 결과를 문자열로 반환한다.

    Raises:
        ValueError:
            수식이 비어 있거나 허용되지 않은 문자가 포함된 경우 발생한다.

    주의:
        eval()은 임의의 Python 코드를 실행할 수 있기 때문에 실제 운영 환경에서는 위험하다.
        여기서는 Agent Tool 개념을 이해하기 위한 실습용 예제로만 사용한다.
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

## 9. 계산기 도구 코드 분석

### 9.1 함수 시그니처

```python
def calculate(expression: str) -> str:
```

의미는 다음과 같다.

```text
calculate:
- 함수 이름

expression: str:
- expression이라는 파라미터를 받는다.
- 타입은 문자열(str)이다.

-> str:
- 함수의 반환값은 문자열(str)이라는 의미이다.
```

즉, 이 함수는 문자열 수식을 받아 문자열 결과를 반환한다.

---

### 9.2 입력값 검증

```python
if not expression or not expression.strip():
    raise ValueError("계산할 수식이 비어 있습니다.")
```

이 코드는 입력 수식이 비어 있는지 확인한다.

```text
expression이 None이거나 빈 문자열이면 오류
expression.strip() 결과가 빈 문자열이면 오류
```

`strip()`은 문자열 앞뒤의 공백을 제거한다.

예를 들어 다음 값은 모두 비어 있는 입력으로 처리된다.

```text
""
"   "
None
```

---

### 9.3 허용 문자 제한

```python
allowed_chars = "0123456789+-*/(). "
```

이번 실습에서는 안전을 위해 숫자와 기본 연산자만 허용한다.

```text
허용:
0~9
+
-
*
/
(
)
.
공백
```

다음 코드는 허용되지 않은 문자가 있는지 검사한다.

```python
if any(char not in allowed_chars for char in expression):
    raise ValueError("허용되지 않은 문자가 포함되어 있습니다.")
```

이렇게 제한하지 않으면 `eval()`이 위험한 Python 코드를 실행할 수 있다.

---

### 9.4 eval() 사용

```python
result = eval(expression, {"__builtins__": {}}, {})
```

`eval()`은 문자열을 Python 코드로 해석하여 실행하는 함수이다.

예를 들어 다음 코드는

```python
eval("12500 * 17")
```

아래 계산을 수행한다.

```text
12500 * 17 = 212500
```

하지만 `eval()`은 위험할 수 있다.  
운영 환경에서는 수식 계산 전용 라이브러리나 직접 만든 안전한 Parser를 사용하는 것이 좋다.

---

## 10. 검색 도구 만들기

파일 경로:

```text
labs/agent/tools/search.py
```

코드:

```python
from __future__ import annotations


DOCUMENTS: list[dict[str, str]] = [
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
    {
        "title": "ReAct",
        "content": "ReAct는 Reasoning과 Acting을 결합한 Agent 동작 패턴이다.",
    },
]


def search_documents(query: str) -> list[dict[str, str]]:
    """
    샘플 문서 목록에서 검색어가 포함된 문서를 찾는다.

    Args:
        query:
            검색어.
            예: "Agent", "RAG", "Tool Calling"

    Returns:
        검색된 문서 목록.
        각 문서는 title과 content를 가진 dictionary이다.

    Raises:
        ValueError:
            검색어가 비어 있는 경우 발생한다.
    """
    if not query or not query.strip():
        raise ValueError("검색어가 비어 있습니다.")

    normalized_query = query.lower()
    results: list[dict[str, str]] = []

    for document in DOCUMENTS:
        title = document["title"].lower()
        content = document["content"].lower()

        if normalized_query in title or normalized_query in content:
            results.append(document)

    return results
```

---

## 11. 검색 도구 코드 분석

### 11.1 DOCUMENTS

```python
DOCUMENTS: list[dict[str, str]] = [
    ...
]
```

`DOCUMENTS`는 샘플 문서 목록이다.

타입 힌트의 의미는 다음과 같다.

```text
list:
- 여러 개의 값을 담는 리스트

dict[str, str]:
- key는 문자열
- value도 문자열
```

즉, `DOCUMENTS`는 다음과 같은 딕셔너리 여러 개를 담은 리스트이다.

```python
{
    "title": "AI Agent 개요",
    "content": "AI Agent는 목표를 이해하고..."
}
```

---

### 11.2 검색어 정규화

```python
normalized_query = query.lower()
```

`lower()`는 문자열을 소문자로 바꾼다.

검색어와 문서 내용을 모두 소문자로 바꿔 비교하면 대소문자 차이 때문에 검색이 실패하는 일을 줄일 수 있다.

---

### 11.3 검색 조건

```python
if normalized_query in title or normalized_query in content:
    results.append(document)
```

`in` 연산자는 어떤 값이 포함되어 있는지 확인한다.

예를 들어 다음 코드는 참이다.

```python
"agent" in "ai agent 개요"
```

검색어가 제목이나 본문에 포함되어 있으면 결과 목록에 추가한다.

---

## 12. 파일 읽기 도구 만들기

파일 경로:

```text
labs/agent/tools/file_reader.py
```

코드:

```python
from __future__ import annotations

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]


def read_text_file(relative_path: str) -> str:
    """
    labs/agent 디렉터리 내부의 텍스트 파일을 읽는다.

    Args:
        relative_path:
            labs/agent 디렉터리를 기준으로 한 상대 경로.
            예: "sample_docs/agent_sample.md"

    Returns:
        파일 내용을 문자열로 반환한다.

    Raises:
        ValueError:
            경로가 비어 있거나, labs/agent 밖의 파일을 읽으려는 경우 발생한다.

        FileNotFoundError:
            파일이 존재하지 않는 경우 발생한다.
    """
    if not relative_path or not relative_path.strip():
        raise ValueError("파일 경로가 비어 있습니다.")

    target_path = (BASE_DIR / relative_path).resolve()

    if not str(target_path).startswith(str(BASE_DIR)):
        raise ValueError("labs/agent 디렉터리 밖의 파일은 읽을 수 없습니다.")

    if not target_path.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {target_path}")

    if not target_path.is_file():
        raise ValueError(f"파일이 아닙니다: {target_path}")

    return target_path.read_text(encoding="utf-8")
```

---

## 13. 파일 읽기 도구 코드 분석

### 13.1 pathlib.Path

```python
from pathlib import Path
```

`Path`는 파일 경로를 객체로 다룰 수 있게 해주는 Python 표준 라이브러리이다.

문자열로 경로를 직접 다루는 것보다 안전하고 읽기 쉽다.

---

### 13.2 BASE_DIR

```python
BASE_DIR = Path(__file__).resolve().parents[1]
```

이 코드는 현재 파일을 기준으로 `labs/agent` 디렉터리를 찾는다.

예를 들어 파일 위치가 다음과 같다면

```text
labs/agent/tools/file_reader.py
```

각 값은 대략 다음과 같다.

```text
Path(__file__)              → labs/agent/tools/file_reader.py
Path(__file__).resolve()    → 절대 경로
parents[0]                  → labs/agent/tools
parents[1]                  → labs/agent
```

따라서 `BASE_DIR`은 `labs/agent`가 된다.

---

### 13.3 경로 탈출 방지

```python
if not str(target_path).startswith(str(BASE_DIR)):
    raise ValueError("labs/agent 디렉터리 밖의 파일은 읽을 수 없습니다.")
```

이 코드는 사용자가 `../` 같은 경로를 사용해서 허용된 디렉터리 밖의 파일을 읽지 못하도록 막는다.

예를 들어 다음 경로는 차단되어야 한다.

```text
../../secret.txt
/etc/passwd
```

Agent에게 파일 읽기 도구를 제공할 때는 반드시 접근 범위를 제한해야 한다.

---

# Part B. Tool Registry 만들기

Tool Registry는 Agent가 사용할 수 있는 도구 목록을 관리하는 구성 요소이다.

---

## 14. Tool Registry란 무엇인가?

Tool Registry는 다음 정보를 관리한다.

```text
1. 도구 이름
2. 실제 Python 함수
3. 도구 설명
4. 파라미터 정보
5. 사용 가능 여부
```

Agent 입장에서 Tool Registry는 도구 목록표와 같다.

```text
calculator    → 계산 도구
search        → 검색 도구
file_reader   → 파일 읽기 도구
```

실제 Enterprise 환경에서는 Tool Registry가 매우 중요하다.

```text
1. 어떤 도구를 사용할 수 있는가?
2. 누가 사용할 수 있는가?
3. 읽기 도구인가, 쓰기 도구인가?
4. 승인 절차가 필요한가?
5. 실행 로그를 남겨야 하는가?
```

이번 실습에서는 단순한 Python 딕셔너리로 Tool Registry를 구현한다.

---

## 15. Tool Registry 코드 만들기

파일 경로:

```text
labs/agent/common/tool_registry.py
```

코드:

```python
from __future__ import annotations

from typing import Any, Callable

from tools.calculator import calculate
from tools.file_reader import read_text_file
from tools.search import search_documents


ToolFunction = Callable[..., Any]


TOOLS: dict[str, ToolFunction] = {
    "calculator": calculate,
    "search": search_documents,
    "file_reader": read_text_file,
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
        "description": "샘플 문서 목록에서 키워드를 검색할 때 사용하는 도구이다.",
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
]


def get_tool(tool_name: str) -> ToolFunction:
    """
    도구 이름으로 실제 Python 함수를 조회한다.

    Args:
        tool_name:
            조회할 도구 이름.
            예: "calculator", "search", "file_reader"

    Returns:
        도구 이름에 해당하는 Python 함수.

    Raises:
        ValueError:
            등록되지 않은 도구 이름이 들어온 경우 발생한다.
    """
    if tool_name not in TOOLS:
        raise ValueError(f"등록되지 않은 도구입니다: {tool_name}")

    return TOOLS[tool_name]


def get_tool_schemas() -> list[dict[str, Any]]:
    """
    Agent가 사용할 수 있는 도구 설명 목록을 반환한다.

    Returns:
        Tool Schema 목록.
    """
    return TOOL_SCHEMAS
```

---

## 16. Tool Registry 코드 분석

### 16.1 Callable

```python
from typing import Any, Callable
```

`Callable`은 호출 가능한 객체를 의미한다.

Python에서 함수는 호출 가능한 객체이다.

```python
calculate("12500 * 17")
search_documents("Agent")
read_text_file("sample_docs/agent_sample.md")
```

이런 함수들을 모두 하나의 타입으로 표현하기 위해 `Callable`을 사용한다.

---

### 16.2 ToolFunction 타입 별칭

```python
ToolFunction = Callable[..., Any]
```

이 코드는 타입 별칭을 만든다.

의미는 다음과 같다.

```text
ToolFunction:
- 어떤 파라미터든 받을 수 있고
- 어떤 값이든 반환할 수 있는 함수
```

`...`은 파라미터 형태가 다양할 수 있다는 의미이다.

도구마다 파라미터가 다를 수 있다.

```text
calculator(expression)
search(query)
file_reader(relative_path)
```

그래서 공통 타입을 느슨하게 잡았다.

---

### 16.3 TOOLS 딕셔너리

```python
TOOLS: dict[str, ToolFunction] = {
    "calculator": calculate,
    "search": search_documents,
    "file_reader": read_text_file,
}
```

이 딕셔너리는 도구 이름과 실제 함수를 연결한다.

```text
"calculator"  → calculate 함수
"search"      → search_documents 함수
"file_reader" → read_text_file 함수
```

즉, Agent가 `"calculator"`라는 도구를 선택하면 실제로는 `calculate()` 함수가 실행된다.

---

### 16.4 TOOL_SCHEMAS

`TOOL_SCHEMAS`는 도구 설명 목록이다.

실제 LLM 기반 Tool Calling에서는 이 Schema를 LLM에게 전달한다.  
LLM은 이 설명을 보고 어떤 도구를 사용할지 판단한다.

이번 실습에서는 LLM을 사용하지 않지만, 구조를 미리 동일하게 잡아둔다.

---

# Part C. Tool Executor 만들기

Tool Executor는 Tool Call 요청을 받아 실제 도구를 실행하는 구성 요소이다.

---

## 17. Tool Executor란 무엇인가?

Tool Executor는 다음 역할을 한다.

```text
1. Tool Call 요청을 받는다.
2. 도구 이름을 확인한다.
3. 등록된 도구인지 검증한다.
4. 입력값을 실제 함수에 전달한다.
5. 도구 실행 결과를 반환한다.
6. 오류가 발생하면 예외를 처리한다.
```

Tool Calling 구조에서 LLM은 도구 호출 요청을 생성할 뿐이다.  
실제 실행은 Tool Executor가 담당한다.

```text
LLM:
calculator 도구를 expression="12500 * 17"로 호출해야 한다.

Tool Executor:
calculate(expression="12500 * 17") 실행

Tool Result:
212500
```

---

## 18. Tool Executor 코드 만들기

파일 경로:

```text
labs/agent/common/tool_executor.py
```

코드:

```python
from __future__ import annotations

from typing import Any

from common.tool_registry import get_tool


def execute_tool(tool_name: str, arguments: dict[str, Any]) -> Any:
    """
    도구 이름과 입력값을 받아 실제 도구 함수를 실행한다.

    Args:
        tool_name:
            실행할 도구 이름.
            예: "calculator", "search", "file_reader"

        arguments:
            도구 함수에 전달할 인자 dictionary.
            예: {"expression": "12500 * 17"}

    Returns:
        도구 실행 결과.

    Raises:
        ValueError:
            등록되지 않은 도구이거나 입력값이 잘못된 경우 발생할 수 있다.
    """
    if not tool_name or not tool_name.strip():
        raise ValueError("도구 이름이 비어 있습니다.")

    if arguments is None:
        arguments = {}

    tool_function = get_tool(tool_name)

    return tool_function(**arguments)
```

---

## 19. Tool Executor 코드 분석

### 19.1 arguments

```python
arguments: dict[str, Any]
```

`arguments`는 도구에 전달할 입력값이다.

예를 들어 계산기 도구를 호출한다면 다음과 같다.

```python
{
    "expression": "12500 * 17"
}
```

파일 읽기 도구를 호출한다면 다음과 같다.

```python
{
    "relative_path": "sample_docs/agent_sample.md"
}
```

---

### 19.2 함수 조회

```python
tool_function = get_tool(tool_name)
```

`get_tool()` 함수는 Tool Registry에서 도구 이름에 해당하는 실제 함수를 가져온다.

예를 들어 `tool_name`이 `"calculator"`라면 `calculate` 함수가 반환된다.

---

### 19.3 키워드 인자 전달

```python
return tool_function(**arguments)
```

`**arguments`는 딕셔너리를 함수의 키워드 인자로 풀어서 전달한다.

예를 들어 다음 코드가 있다고 하자.

```python
arguments = {
    "expression": "12500 * 17"
}
```

아래 코드는

```python
calculate(**arguments)
```

다음 코드와 같다.

```python
calculate(expression="12500 * 17")
```

이 문법은 Tool Calling 구현에서 매우 자주 사용된다.

---

# Part D. 첫 번째 Agent 만들기

이제 Agent 실행 파일을 만든다.

---

## 20. 첫 번째 Agent의 목표

이번 첫 번째 Agent는 다음 세 가지 요청을 처리한다.

```text
1. 계산 요청
2. 검색 요청
3. 파일 읽기 요청
```

예시 입력은 다음과 같다.

```text
12500 * 17 계산해줘
Agent 검색해줘
파일 읽어줘
```

이번 단계에서는 실제 LLM 대신 단순한 규칙 기반 함수가 도구를 선택한다.

---

## 21. 가장 단순한 Agent 코드 만들기

파일 경로:

```text
labs/agent/01_first_agent.py
```

코드:

```python
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

    Args:
        user_input:
            사용자가 입력한 질문 또는 요청.

    Returns:
        Tool Call 형식의 dictionary.
        예:
        {
            "tool_name": "calculator",
            "arguments": {
                "expression": "12500 * 17"
            }
        }
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

    Args:
        tool_name:
            실행한 도구 이름.

        tool_result:
            도구 실행 결과.

    Returns:
        사용자에게 출력할 최종 답변 문자열.
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


def main() -> None:
    """
    첫 번째 Agent 실행 함수이다.

    실행 흐름:
    1. 사용 가능한 도구 목록 출력
    2. 사용자 질문 입력
    3. 질문을 기반으로 도구 선택
    4. Tool Call 내용 출력
    5. Tool Executor로 실제 도구 실행
    6. 도구 결과를 최종 답변으로 변환
    7. 최종 답변 출력
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
        print("예: 12500 * 17 계산해줘 / Agent 검색해줘 / 파일 읽어줘")
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
```

---

## 22. 첫 번째 Agent 코드 분석

### 22.1 print_available_tools 함수

```python
def print_available_tools() -> None:
```

이 함수는 Agent가 사용할 수 있는 도구 목록을 출력한다.

```python
for schema in get_tool_schemas():
```

`get_tool_schemas()`는 Tool Registry에 등록된 도구 설명 목록을 가져온다.

실제 LLM Agent에서는 이 Tool Schema를 LLM에게 전달한다.  
이번 실습에서는 사용자가 눈으로 확인할 수 있도록 출력한다.

---

### 22.2 select_tool 함수

```python
def select_tool(user_input: str) -> dict[str, Any]:
```

이 함수는 사용자 입력을 보고 어떤 도구를 사용할지 결정한다.

실제 Agent에서는 LLM이 이 역할을 수행한다.

이번 실습에서는 다음 규칙을 사용한다.

```text
입력에 "계산" 또는 사칙연산 기호가 있으면 calculator
입력에 "검색" 또는 "찾아"가 있으면 search
입력에 "파일"과 "읽"이 있으면 file_reader
```

이 함수의 반환값은 Tool Call 형식이다.

```python
{
    "tool_name": "calculator",
    "arguments": {
        "expression": "12500 * 17"
    }
}
```

---

### 22.3 format_final_answer 함수

```python
def format_final_answer(tool_name: str, tool_result: Any) -> str:
```

이 함수는 도구 실행 결과를 사람이 읽기 좋은 최종 답변으로 바꾼다.

Agent 구조에서 보면 다음 단계에 해당한다.

```text
Observation → Final Answer
```

도구 결과는 시스템 내부 데이터일 수 있으므로, 사용자가 이해하기 쉽게 정리하는 과정이 필요하다.

---

### 22.4 main 함수

`main()` 함수는 Agent 실행 흐름 전체를 담당한다.

```text
1. 도구 목록 출력
2. 사용자 입력 받기
3. 도구 선택
4. Tool Call 출력
5. 도구 실행
6. Observation 출력
7. Final Answer 출력
```

이 흐름은 ReAct 구조와 연결된다.

```text
Thought:
select_tool 함수가 수행

Action:
Tool Call 생성

Observation:
execute_tool 실행 결과

Final Answer:
format_final_answer 결과
```

---

### 22.5 if __name__ == "__main__"

```python
if __name__ == "__main__":
    main()
```

이 코드는 Python 파일을 직접 실행했을 때만 `main()` 함수를 실행하겠다는 의미이다.

예를 들어 다음 명령으로 실행하면

```bash
python labs/agent/01_first_agent.py
```

`__name__` 값이 `"__main__"`이 되므로 `main()`이 실행된다.

반면 다른 파일에서 import할 때는 자동으로 실행되지 않는다.

---

## 23. 실행 방법

프로젝트 루트에서 실행한다.

```bash
python labs/agent/01_first_agent.py
```

만약 import 오류가 발생하면 아래처럼 `labs/agent` 디렉터리로 이동해서 실행한다.

```bash
cd labs/agent
python 01_first_agent.py
```

이 경우 import 경로가 더 단순하게 맞을 수 있다.

---

## 24. 실행 예시 1: 계산 요청

입력:

```text
12500 * 17 계산해줘
```

예상 출력:

```text
================================================================================
Tool Call
================================================================================
{
  "tool_name": "calculator",
  "arguments": {
    "expression": "12500 * 17"
  }
}
================================================================================
Observation
================================================================================
212500
================================================================================
Final Answer
================================================================================
계산 결과는 212500입니다.
```

이 흐름을 ReAct로 해석하면 다음과 같다.

```text
Thought:
계산이 필요하다.

Action:
calculator 도구를 사용한다.

Observation:
212500

Final Answer:
계산 결과는 212500입니다.
```

---

## 25. 실행 예시 2: 검색 요청

입력:

```text
Agent 검색해줘
```

예상 출력:

```text
================================================================================
Tool Call
================================================================================
{
  "tool_name": "search",
  "arguments": {
    "query": "Agent"
  }
}
================================================================================
Observation
================================================================================
[{'title': 'AI Agent 개요', 'content': 'AI Agent는 목표를 이해하고 도구를 사용하여 작업을 수행하는 AI 시스템이다.'}]
================================================================================
Final Answer
================================================================================
검색 결과는 다음과 같습니다.
1. AI Agent 개요 - AI Agent는 목표를 이해하고 도구를 사용하여 작업을 수행하는 AI 시스템이다.
```

이 예시는 검색 도구가 Agent의 Action으로 사용되는 구조를 보여준다.

---

## 26. 실행 예시 3: 파일 읽기 요청

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

AI Agent는 사용자의 목표를 이해하고...
================================================================================
Final Answer
================================================================================
파일 내용을 읽었습니다.

# AI Agent 샘플 문서

AI Agent는 사용자의 목표를 이해하고...
```

이 예시는 Agent가 파일 읽기 도구를 사용하여 외부 데이터를 가져오는 구조를 보여준다.

---

# Part E. Tool Calling 흐름을 명확히 분리하기

`01_first_agent.py`는 가장 단순한 Agent 예제이다.  
이제 Tool Calling 흐름을 조금 더 명확하게 분리한 `02_tool_calling.py`를 만든다.

---

## 27. Tool Calling 전용 예제 만들기

파일 경로:

```text
labs/agent/02_tool_calling.py
```

코드:

```python
from __future__ import annotations

import json
from typing import Any

from common.tool_executor import execute_tool


def run_tool_call(tool_call: dict[str, Any]) -> Any:
    """
    Tool Call dictionary를 받아 실제 도구를 실행한다.

    Args:
        tool_call:
            도구 호출 요청.
            예:
            {
                "tool_name": "calculator",
                "arguments": {
                    "expression": "12500 * 17"
                }
            }

    Returns:
        도구 실행 결과.
    """
    tool_name = tool_call.get("tool_name", "")
    arguments = tool_call.get("arguments", {})

    return execute_tool(tool_name, arguments)


def main() -> None:
    """
    Tool Calling 구조만 별도로 확인하는 실습이다.
    """
    tool_calls = [
        {
            "tool_name": "calculator",
            "arguments": {
                "expression": "12500 * 17"
            },
        },
        {
            "tool_name": "search",
            "arguments": {
                "query": "ReAct"
            },
        },
        {
            "tool_name": "file_reader",
            "arguments": {
                "relative_path": "sample_docs/agent_sample.md"
            },
        },
    ]

    for tool_call in tool_calls:
        print("=" * 80)
        print("Tool Call")
        print("=" * 80)
        print(json.dumps(tool_call, ensure_ascii=False, indent=2))

        try:
            result = run_tool_call(tool_call)

            print("=" * 80)
            print("Tool Result")
            print("=" * 80)
            print(result)

        except Exception as error:
            print("=" * 80)
            print("Tool Error")
            print("=" * 80)
            print(error)


if __name__ == "__main__":
    main()
```

---

## 28. 02_tool_calling.py 코드 분석

이 파일은 사용자 입력 없이 미리 정의된 Tool Call 목록을 실행한다.

목적은 다음과 같다.

```text
1. Tool Call 구조를 명확히 이해한다.
2. Tool Executor가 도구 이름과 arguments를 어떻게 처리하는지 확인한다.
3. LLM이 나중에 생성할 Tool Call 형식이 어떤 모습인지 미리 확인한다.
```

실제 LLM 기반 Tool Calling에서는 LLM이 다음과 같은 구조를 생성하게 된다.

```json
{
  "tool_name": "calculator",
  "arguments": {
    "expression": "12500 * 17"
  }
}
```

이번 실습에서는 이 구조를 사람이 직접 작성해서 실행한다.

---

## 29. Tool Call 구조 이해

Tool Call은 보통 다음 구조를 가진다.

```json
{
  "tool_name": "도구 이름",
  "arguments": {
    "파라미터 이름": "파라미터 값"
  }
}
```

예를 들어 계산기 도구는 다음과 같다.

```json
{
  "tool_name": "calculator",
  "arguments": {
    "expression": "12500 * 17"
  }
}
```

검색 도구는 다음과 같다.

```json
{
  "tool_name": "search",
  "arguments": {
    "query": "ReAct"
  }
}
```

파일 읽기 도구는 다음과 같다.

```json
{
  "tool_name": "file_reader",
  "arguments": {
    "relative_path": "sample_docs/agent_sample.md"
  }
}
```

도구마다 필요한 파라미터 이름이 다르다.

```text
calculator  → expression
search      → query
file_reader → relative_path
```

이 파라미터 정보가 Tool Schema에 정의되어 있어야 한다.

---

## 30. 실행 방법

```bash
cd labs/agent
python 02_tool_calling.py
```

예상 출력:

```text
================================================================================
Tool Call
================================================================================
{
  "tool_name": "calculator",
  "arguments": {
    "expression": "12500 * 17"
  }
}
================================================================================
Tool Result
================================================================================
212500
...
```

---

# Part F. Enterprise 관점에서 보기

이번 실습은 단순하지만, Enterprise Agent 구조의 기본과 같다.

---

## 31. 이번 실습 구조와 Enterprise 구조 비교

이번 실습 구조:

```text
01_first_agent.py
   ↓
tool_registry.py
   ↓
tool_executor.py
   ↓
calculator.py / search.py / file_reader.py
```

Enterprise 구조:

```text
Agent Runtime
   ↓
Tool Registry
   ↓
Policy Guard
   ↓
Tool Executor
   ↓
MCP Server / 업무 API / DB / 파일 시스템
```

이번 실습에서는 Policy Guard, 인증, 권한, 감사 로그를 생략했다.  
하지만 구조는 동일하다.

---

## 32. 실제 기업 환경에서 추가되어야 할 것

Enterprise 환경에서는 다음 기능이 추가되어야 한다.

```text
1. 사용자 인증
2. 사용자별 도구 권한
3. 읽기 도구와 쓰기 도구 구분
4. 입력 파라미터 검증
5. 파일 접근 경로 제한
6. API Key 관리
7. 도구 실행 로그
8. 승인 절차
9. 예외 처리와 재시도
10. 민감정보 마스킹
```

예를 들어 메일 발송 도구를 만든다면 바로 발송하면 안 된다.

좋은 흐름은 다음과 같다.

```text
1. Agent가 메일 초안을 작성한다.
2. 사용자에게 Preview를 보여준다.
3. 사용자가 승인한다.
4. send_email 도구를 실행한다.
5. 발송 로그를 남긴다.
```

---

## 33. Tool Registry 확장 방향

이번 실습의 Tool Registry는 단순한 Python 딕셔너리이다.

```python
TOOLS = {
    "calculator": calculate,
    "search": search_documents,
    "file_reader": read_text_file,
}
```

하지만 실제 시스템에서는 다음 정보를 함께 관리해야 한다.

```text
1. 도구 이름
2. 도구 설명
3. 도구 유형
4. 읽기/쓰기 여부
5. 승인 필요 여부
6. 필요한 권한
7. Rate Limit
8. Timeout
9. 재시도 정책
10. 로그 저장 여부
```

예시:

```json
{
  "name": "send_email",
  "type": "write",
  "description": "사용자 승인 후 이메일을 발송한다.",
  "permission": "mail.send",
  "approval_required": true,
  "timeout_seconds": 10,
  "logging": true
}
```

---

## 34. 이번 실습의 한계

이번 실습은 Agent 구조를 이해하기 위한 첫 번째 단계이다.  
따라서 다음 한계가 있다.

```text
1. 실제 LLM을 연결하지 않았다.
2. 도구 선택이 규칙 기반이다.
3. Memory가 없다.
4. 대화 이력을 저장하지 않는다.
5. 복잡한 Planning을 수행하지 않는다.
6. Workflow 제어가 없다.
7. MCP를 사용하지 않는다.
8. Multi Agent 구조가 아니다.
```

하지만 이 한계는 의도적인 것이다.

처음부터 모든 기능을 넣으면 Agent의 기본 구조를 이해하기 어렵다.  
이번 단계에서는 다음 구조를 확실히 이해하는 것이 중요하다.

```text
사용자 입력
   ↓
도구 선택
   ↓
Tool Call
   ↓
Tool Executor
   ↓
Tool Result
   ↓
Final Answer
```

---

## 35. 자주 발생하는 오류

---

### 35.1 ModuleNotFoundError

오류 예시:

```text
ModuleNotFoundError: No module named 'tools'
```

원인:

```text
Python 실행 위치와 import 경로가 맞지 않기 때문이다.
```

해결 방법:

```bash
cd labs/agent
python 01_first_agent.py
```

또는 프로젝트 루트에서 실행할 수 있도록 `PYTHONPATH`를 설정한다.

```bash
PYTHONPATH=./labs/agent python labs/agent/01_first_agent.py
```

---

### 35.2 파일을 찾을 수 없는 오류

오류 예시:

```text
FileNotFoundError: 파일을 찾을 수 없습니다
```

원인:

```text
sample_docs/agent_sample.md 파일이 없거나 실행 위치가 다르기 때문이다.
```

해결:

```text
1. labs/agent/sample_docs/agent_sample.md 파일이 있는지 확인한다.
2. cd labs/agent 후 다시 실행한다.
```

---

### 35.3 계산식 오류

오류 예시:

```text
허용되지 않은 문자가 포함되어 있습니다.
```

원인:

```text
계산식에 한글이나 허용되지 않은 문자가 남아 있을 수 있다.
```

예를 들어 다음 입력은 문제가 될 수 있다.

```text
12,500원 * 17개 계산해줘
```

이번 실습 계산기는 콤마와 한글 단위를 처리하지 않는다.

좋은 입력:

```text
12500 * 17 계산해줘
```

---

## 36. 핵심 정리

이번 문서의 핵심은 다음과 같다.

```text
1. Python 함수 하나가 Agent Tool이 될 수 있다.
2. Tool Registry는 도구 이름과 실제 함수를 연결한다.
3. Tool Schema는 도구 사용 방법을 설명한다.
4. Tool Executor는 Tool Call 요청을 받아 실제 함수를 실행한다.
5. Agent는 사용자 요청을 보고 도구를 선택한다.
6. 도구 실행 결과는 Observation이 된다.
7. Observation을 바탕으로 최종 답변을 만든다.
8. 이번 실습은 LLM 없이 규칙 기반으로 Agent 구조를 이해하기 위한 단계이다.
9. 실제 LLM 기반 Agent는 다음 단계에서 이 구조를 확장하면 된다.
```

한 문장으로 정리하면 다음과 같다.

> **첫 번째 Agent 구현의 핵심은 "질문 → 도구 선택 → 도구 실행 → 결과 확인 → 답변" 흐름을 코드로 이해하는 것이다.**

---

## 37. 다음 단계 예고

다음 문서는 다음과 같다.

```text
Step3-4. Agent Memory와 상태 관리
docs/study/step3/step3_4_agent_memory_guide.md
```

다음 단계에서는 Agent가 이전 대화와 작업 상태를 기억하도록 확장한다.

다음 문서에서 다룰 내용은 다음과 같다.

```text
1. Memory가 필요한 이유
2. Conversation Memory
3. Task State
4. Tool Execution History
5. JSON 기반 Memory
6. SQLite 기반 Memory
7. Memory와 보안
8. Agent 실행 흐름에 Memory 연결
```

---

## 38. 부록: 전체 코드 작성 순서

처음부터 다시 만든다면 아래 순서로 진행하면 된다.

```bash
mkdir -p labs/agent/tools
mkdir -p labs/agent/common
mkdir -p labs/agent/sample_docs

touch labs/agent/tools/__init__.py
touch labs/agent/common/__init__.py
touch labs/agent/sample_docs/agent_sample.md

touch labs/agent/tools/calculator.py
touch labs/agent/tools/search.py
touch labs/agent/tools/file_reader.py

touch labs/agent/common/tool_registry.py
touch labs/agent/common/tool_executor.py

touch labs/agent/01_first_agent.py
touch labs/agent/02_tool_calling.py
```

작성 순서는 다음을 추천한다.

```text
1. sample_docs/agent_sample.md
2. tools/calculator.py
3. tools/search.py
4. tools/file_reader.py
5. common/tool_registry.py
6. common/tool_executor.py
7. 01_first_agent.py
8. 02_tool_calling.py
```

---

## 39. 부록: ReAct와 이번 코드의 매핑

이번 코드와 ReAct 구조를 연결하면 다음과 같다.

| ReAct 개념 | 이번 코드에서의 위치 |
|---|---|
| Question | `input("질문을 입력하세요: ")` |
| Thought | `select_tool()` |
| Action | Tool Call dictionary |
| Action Input | `arguments` |
| Observation | `execute_tool()` 결과 |
| Final Answer | `format_final_answer()` |

즉, 이번 실습은 ReAct를 완전한 LLM 방식으로 구현한 것은 아니지만, ReAct의 기본 구조를 Python 코드로 단순화해서 보여준다.

---

## 40. 부록: 향후 확장 방향

이번 Agent는 다음 방향으로 확장할 수 있다.

```text
1. 규칙 기반 select_tool을 LLM 호출로 교체
2. Tool Schema를 LLM 프롬프트에 전달
3. LLM 응답에서 Tool Call JSON 파싱
4. Tool Result를 다시 LLM에 전달
5. 대화 이력 Memory 추가
6. RAG 검색 도구 연결
7. LangGraph Workflow로 실행 흐름 제어
8. MCP Server 기반 외부 시스템 연동
9. Multi Agent 구조로 역할 분리
10. Enterprise Agent Gateway로 통합
```

이 확장 흐름이 바로 Step3 전체 학습 과정이다.

---
