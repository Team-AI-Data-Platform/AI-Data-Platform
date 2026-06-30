# Step3-6. LangGraph 기반 Workflow Agent 가이드

> AI DATA Platform 연구 프로젝트  
> Step3. AI Agent  
> Part2. AI Agent 심화  
> 문서 경로: `docs/study/step3/step3_6_langgraph_workflow_agent_guide.md`  
> 작성일: 2026-06-30

---

## 1. 문서 목적

이 문서는 `Step3-5. Planning Agent와 Workflow`에서 학습한 Planning과 Workflow 개념을 바탕으로, **LangGraph 기반 Workflow Agent**를 이해하기 위한 가이드 문서이다.

Step3-5에서는 다음 구조를 학습했다.

```text
사용자 요청
   ↓
Planning
   ↓
Task List
   ↓
Workflow
   ↓
Task 실행
   ↓
State 저장
   ↓
Final Answer
```

이번 Step3-6에서는 이 Workflow 구조를 LangGraph로 표현하는 방법을 학습한다.

LangGraph는 복잡한 Agent 실행 흐름을 **Graph** 구조로 표현할 수 있게 해준다.

기본 개념은 다음과 같다.

```text
State:
현재 Workflow의 상태

Node:
실제로 작업을 수행하는 함수

Edge:
다음에 어떤 Node로 이동할지 정의하는 연결

Conditional Edge:
조건에 따라 다음 Node를 선택하는 분기

Graph:
State, Node, Edge를 연결한 전체 실행 흐름
```

이번 문서의 핵심은 다음 한 문장으로 요약할 수 있다.

> **LangGraph는 Agent Workflow를 State, Node, Edge 기반의 Graph 구조로 제어하는 도구이다.**

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
│   └─ Step3-4. Agent Memory와 상태 관리
│
├─ Part2. AI Agent 심화
│   ├─ Step3-5. Planning Agent와 Workflow
│   ├─ Step3-6. LangGraph 기반 Workflow Agent   ← 현재 문서
│   ├─ Step3-7. MCP 아키텍처 이해
│   └─ Step3-8. MCP 기반 외부 시스템 연동
│
└─ Part3. Enterprise AI Agent
    ├─ Step3-9. Multi Agent 협업
    └─ Step3-10. Enterprise AI Agent Platform
```

Step3-6은 Step3-5에서 배운 Workflow를 실제 Graph 기반 코드 구조로 구현하기 위한 단계이다.

```text
Step3-5:
Workflow 개념 이해

Step3-6:
Workflow를 LangGraph로 구현

Step3-7:
외부 도구 연동 표준 구조인 MCP 이해

Step3-8:
MCP 기반 외부 시스템 연동 실습
```

즉, Step3-6은 Planning Agent를 실제 실행 가능한 Workflow Agent로 확장하는 핵심 단계이다.

---

## 3. 학습 목표

이 문서를 마치면 다음 내용을 설명할 수 있어야 한다.

```text
1. LangGraph가 왜 필요한지 설명할 수 있다.
2. LangGraph의 State, Node, Edge 개념을 설명할 수 있다.
3. StateGraph가 무엇인지 설명할 수 있다.
4. Node 함수가 State를 입력받고 State 일부를 반환하는 구조를 이해할 수 있다.
5. 일반 Edge와 Conditional Edge의 차이를 설명할 수 있다.
6. START와 END의 의미를 이해할 수 있다.
7. Graph를 compile하고 invoke하는 흐름을 이해할 수 있다.
8. Step3-5의 Planning Workflow를 LangGraph 구조로 변환할 수 있다.
9. Enterprise Workflow Agent에서 LangGraph가 어떤 역할을 하는지 설명할 수 있다.
```

---

## 4. 왜 LangGraph가 필요한가?

Step3-5에서는 Workflow를 다음처럼 단순한 Python 코드로 표현했다.

```python
for task in tasks:
    execute_task(task)
```

이 방식은 단순한 순차 작업에는 충분하다.

하지만 Workflow가 복잡해지면 문제가 생긴다.

```text
1. 조건 분기가 많아진다.
2. 중간 상태 관리가 어려워진다.
3. 실패한 지점부터 재실행하기 어렵다.
4. Human-in-the-Loop을 넣기 어렵다.
5. Agent가 특정 단계로 되돌아가는 루프를 만들기 어렵다.
6. 여러 Node가 같은 State를 읽고 갱신하는 구조를 관리하기 어렵다.
7. Workflow를 그림처럼 이해하기 어렵다.
```

예를 들어 다음 업무 흐름을 생각해보자.

```text
문서 검색
   ↓
검색 결과 있음?
   ├─ 예 → 문서 요약
   └─ 아니오 → 검색어 재작성
                    ↓
                다시 검색
```

이 구조는 단순한 for문보다 Graph 구조가 더 자연스럽다.

LangGraph는 이런 Agent Workflow를 다음처럼 표현할 수 있게 해준다.

```text
START
  ↓
search
  ↓
has_result?
  ├─ yes → summarize
  └─ no  → rewrite_query → search
  ↓
END
```

즉, LangGraph는 Agent 실행 흐름을 코드와 구조 양쪽에서 명확하게 관리하기 위한 도구이다.

---

## 5. LangGraph란 무엇인가?

LangGraph는 LangChain 생태계에서 제공하는 Graph 기반 Agent Workflow 프레임워크이다.

LangGraph의 핵심 아이디어는 다음과 같다.

```text
Agent 실행 흐름을 Graph로 표현한다.
각 실행 단위는 Node가 된다.
Node 사이의 이동은 Edge가 정의한다.
전체 실행 상태는 State로 관리한다.
```

LangGraph를 단순하게 표현하면 다음과 같다.

```text
LangGraph = State + Node + Edge + Graph Runtime
```

각 구성 요소는 다음 의미를 가진다.

```text
State:
Workflow 전체에서 공유되는 상태 데이터

Node:
State를 입력받아 작업을 수행하고 State를 갱신하는 함수

Edge:
한 Node가 끝난 후 다음 Node로 이동하는 규칙

Conditional Edge:
State 값을 보고 다음 Node를 동적으로 선택하는 규칙

Graph Runtime:
정의된 Graph를 실행하는 엔진
```

LangGraph 공식 문서에서도 Graph의 핵심 구성 요소를 State, Nodes, Edges로 설명한다.

---

## 6. LangChain과 LangGraph의 차이

LangChain은 LLM, Prompt, Tool, Chain을 연결하는 데 유용하다.

단순한 Chain은 다음처럼 한 방향으로 흐른다.

```text
Input
  ↓
Prompt
  ↓
LLM
  ↓
Parser
  ↓
Output
```

이 구조는 단순한 작업에는 적합하다.

하지만 Agent Workflow는 항상 직선으로 흐르지 않는다.

```text
1. 조건에 따라 분기한다.
2. 실패하면 다시 시도한다.
3. 중간에 사람 승인을 기다린다.
4. 여러 Tool을 반복 호출한다.
5. 이전 단계로 되돌아간다.
```

LangGraph는 이런 복잡한 흐름을 표현하기 위해 사용한다.

비교하면 다음과 같다.

| 구분 | LangChain 중심 구조 | LangGraph 중심 구조 |
|---|---|---|
| 실행 흐름 | 선형 Chain 중심 | Graph Workflow 중심 |
| 상태 관리 | 상대적으로 단순 | State 중심 |
| 조건 분기 | 직접 코드로 처리 | Conditional Edge로 표현 |
| 반복 실행 | 구현이 복잡할 수 있음 | Loop 구조 표현 가능 |
| Agent Workflow | 단순 Agent에 적합 | 복잡한 Agent에 적합 |
| Human-in-the-Loop | 별도 설계 필요 | Workflow 중단/재개 구조에 적합 |

한 문장으로 정리하면 다음과 같다.

```text
LangChain은 구성 요소를 연결하는 데 강하고,
LangGraph는 복잡한 실행 흐름을 제어하는 데 강하다.
```

---

## 7. LangGraph 기본 구성 요소

LangGraph를 이해하려면 다음 네 가지를 먼저 이해해야 한다.

```text
1. State
2. Node
3. Edge
4. Graph
```

이 네 가지는 Step3-5에서 배운 Workflow 개념과 연결된다.

| Step3-5 Workflow 개념 | LangGraph 개념 |
|---|---|
| Workflow State | State |
| Task 실행 함수 | Node |
| Task 실행 순서 | Edge |
| 조건부 분기 | Conditional Edge |
| 전체 Workflow | Graph |

---

## 8. State란 무엇인가?

State는 Workflow 전체에서 공유되는 데이터이다.

Agent Workflow가 실행되는 동안 여러 Node는 같은 State를 읽고, 필요한 값을 갱신한다.

예를 들어 문서 요약 Workflow의 State는 다음과 같이 표현할 수 있다.

```python
from typing import TypedDict


class AgentState(TypedDict):
    user_input: str
    query: str
    search_results: list[str]
    summary: str
    final_answer: str
```

State에는 다음과 같은 값이 들어갈 수 있다.

```text
1. 사용자 요청
2. 현재 검색어
3. 검색 결과
4. 읽은 파일 내용
5. 중간 요약
6. 오류 메시지
7. 최종 답변
8. 다음 실행 방향
```

LangGraph에서 Node는 이 State를 입력으로 받고, 변경할 값을 반환한다.

예를 들어 다음 Node를 보자.

```python
def prepare_query(state: AgentState) -> dict:
    return {
        "query": state["user_input"]
    }
```

이 Node는 전체 State를 입력받지만, 반환값은 변경할 일부 State만 포함한다.

즉, Node는 다음 구조를 가진다.

```text
State 입력
   ↓
작업 수행
   ↓
Partial State 반환
```

---

## 9. Node란 무엇인가?

Node는 Workflow에서 실제 작업을 수행하는 실행 단위이다.

Node는 Python 함수로 만들 수 있다.

예시는 다음과 같다.

```python
def search_node(state: AgentState) -> dict:
    query = state["query"]
    results = search_documents(query)

    return {
        "search_results": results
    }
```

이 Node의 역할은 다음과 같다.

```text
1. State에서 query를 읽는다.
2. search_documents 도구를 실행한다.
3. 검색 결과를 search_results에 저장한다.
```

Node는 다음과 같은 작업을 수행할 수 있다.

```text
1. LLM 호출
2. Tool 호출
3. 파일 읽기
4. DB 조회
5. API 호출
6. 상태 분석
7. 결과 요약
8. 오류 처리
```

중요한 점은 Node가 반드시 거대한 Agent일 필요는 없다는 것이다.

처음에는 작은 함수 하나를 Node로 만들면 된다.

```text
작은 Node를 여러 개 연결하면 Workflow가 된다.
```

---

## 10. Edge란 무엇인가?

Edge는 Node와 Node를 연결하는 흐름이다.

예를 들어 다음 Workflow가 있다고 하자.

```text
prepare_query
   ↓
search
   ↓
summarize
   ↓
final_answer
```

이를 LangGraph에서는 Edge로 연결한다.

```python
graph_builder.add_edge("prepare_query", "search")
graph_builder.add_edge("search", "summarize")
graph_builder.add_edge("summarize", "final_answer")
```

Edge는 다음 의미를 가진다.

```text
A Node가 끝나면 B Node를 실행한다.
```

즉, Edge는 Workflow의 순서를 정의한다.

---

## 11. Conditional Edge란 무엇인가?

Conditional Edge는 조건에 따라 다음 Node를 선택하는 Edge이다.

예를 들어 검색 결과가 없으면 검색어를 다시 만들고, 검색 결과가 있으면 요약으로 넘어가는 구조를 만들 수 있다.

```text
search
  ↓
검색 결과 있음?
  ├─ yes → summarize
  └─ no  → rewrite_query
```

이때 조건을 판단하는 함수를 Router라고 볼 수 있다.

```python
def route_after_search(state: AgentState) -> str:
    if state["search_results"]:
        return "summarize"

    return "rewrite_query"
```

Conditional Edge는 다음과 같이 연결한다.

```python
graph_builder.add_conditional_edges(
    "search",
    route_after_search,
    {
        "summarize": "summarize",
        "rewrite_query": "rewrite_query",
    }
)
```

Conditional Edge는 Workflow Agent에서 매우 중요하다.

왜냐하면 실제 업무는 항상 같은 순서로만 진행되지 않기 때문이다.

```text
검색 결과가 있으면 요약
검색 결과가 없으면 재검색
오류가 있으면 복구
승인이 필요하면 사용자 확인
정상이면 종료
```

---

## 12. START와 END

LangGraph에서는 Graph의 시작과 끝을 명확히 표현한다.

```text
START:
Workflow 시작 지점

END:
Workflow 종료 지점
```

예시는 다음과 같다.

```python
from langgraph.graph import START, END

graph_builder.add_edge(START, "prepare_query")
graph_builder.add_edge("final_answer", END)
```

이 구조는 Workflow를 읽기 쉽게 만든다.

```text
START
  ↓
prepare_query
  ↓
search
  ↓
summarize
  ↓
final_answer
  ↓
END
```

START와 END를 명시하면 전체 Graph의 시작점과 종료점을 쉽게 파악할 수 있다.

---

## 13. StateGraph란 무엇인가?

StateGraph는 LangGraph에서 State 기반 Workflow를 만들 때 사용하는 기본 Graph 클래스이다.

기본 사용 흐름은 다음과 같다.

```python
from langgraph.graph import StateGraph

graph_builder = StateGraph(AgentState)
```

여기서 `AgentState`는 Workflow에서 사용할 State 구조이다.

StateGraph를 사용하면 다음을 정의할 수 있다.

```text
1. 어떤 State를 사용할지
2. 어떤 Node가 있는지
3. Node 사이의 Edge는 무엇인지
4. 조건부 분기는 어떻게 할지
5. 어떤 지점에서 시작하고 끝날지
```

전체 흐름은 다음과 같다.

```text
State 정의
   ↓
StateGraph 생성
   ↓
Node 추가
   ↓
Edge 추가
   ↓
Graph Compile
   ↓
Graph Invoke
```

---

## 14. Graph Compile이란?

LangGraph에서 Node와 Edge를 모두 정의한 후에는 Graph를 compile해야 한다.

예시는 다음과 같다.

```python
graph = graph_builder.compile()
```

Compile은 실행 가능한 Graph 객체를 만드는 단계이다.

Compile 단계에서는 다음과 같은 확인을 수행할 수 있다.

```text
1. Graph 구조가 올바른지 확인
2. 고립된 Node가 없는지 확인
3. 실행 가능한 형태로 변환
4. Checkpoint나 Breakpoint 같은 실행 옵션 연결
```

처음 실습에서는 단순히 다음 한 줄로 이해하면 된다.

```text
compile()은 설계한 Graph를 실행 가능한 Workflow로 만드는 단계이다.
```

---

## 15. Graph Invoke란?

Compile된 Graph는 `invoke()`로 실행할 수 있다.

예시는 다음과 같다.

```python
result = graph.invoke(
    {
        "user_input": "Agent 문서를 검색해서 요약해줘",
        "query": "",
        "search_results": [],
        "summary": "",
        "final_answer": "",
    }
)
```

`invoke()`에 전달하는 값은 초기 State이다.

Graph가 실행되면서 각 Node가 State를 갱신하고, 최종 State가 반환된다.

```text
초기 State
   ↓
Node 실행
   ↓
State 갱신
   ↓
다음 Node 실행
   ↓
State 갱신
   ↓
최종 State 반환
```

---

## 16. 가장 단순한 LangGraph 예제

아래는 가장 단순한 LangGraph 예제이다.

```python
from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class SimpleState(TypedDict):
    message: str


def hello_node(state: SimpleState) -> dict:
    return {
        "message": state["message"] + " → hello_node 실행"
    }


graph_builder = StateGraph(SimpleState)

graph_builder.add_node("hello", hello_node)

graph_builder.add_edge(START, "hello")
graph_builder.add_edge("hello", END)

graph = graph_builder.compile()

result = graph.invoke(
    {
        "message": "START"
    }
)

print(result)
```

예상 결과는 다음과 같다.

```text
{
  "message": "START → hello_node 실행"
}
```

이 예제에서 중요한 점은 다음이다.

```text
1. State를 정의한다.
2. Node 함수를 만든다.
3. Node를 Graph에 등록한다.
4. START에서 Node로 Edge를 연결한다.
5. Node에서 END로 Edge를 연결한다.
6. compile 후 invoke로 실행한다.
```

---

## 17. Step3-5 Workflow를 LangGraph로 바꾸기

Step3-5의 문서 검색 Workflow를 다시 보자.

```text
START
  ↓
문서 검색
  ↓
문서 요약
  ↓
최종 답변
  ↓
END
```

이를 LangGraph로 바꾸면 다음과 같다.

```text
START
  ↓
prepare_query
  ↓
search_documents
  ↓
summarize_documents
  ↓
generate_answer
  ↓
END
```

각 Task가 LangGraph에서는 Node가 된다.

| Workflow Task | LangGraph Node |
|---|---|
| 검색어 준비 | `prepare_query` |
| 문서 검색 | `search_documents` |
| 문서 요약 | `summarize_documents` |
| 답변 생성 | `generate_answer` |

이제 중요한 것은 각 Node가 같은 State를 공유한다는 점이다.

```text
prepare_query:
user_input을 query로 변환

search_documents:
query로 문서 검색 후 search_results 저장

summarize_documents:
search_results를 summary로 변환

generate_answer:
summary를 final_answer로 변환
```

---

## 18. 문서 검색 Workflow 예제 코드

아래 코드는 Step3-3에서 만든 검색 Tool을 LangGraph Node 안에서 사용하는 예제이다.

```python
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from tools.search import search_documents


class DocumentWorkflowState(TypedDict):
    user_input: str
    query: str
    search_results: list[dict]
    summary: str
    final_answer: str


def prepare_query_node(state: DocumentWorkflowState) -> dict:
    return {
        "query": state["user_input"]
    }


def search_node(state: DocumentWorkflowState) -> dict:
    results = search_documents(state["query"])

    return {
        "search_results": results
    }


def summarize_node(state: DocumentWorkflowState) -> dict:
    results = state["search_results"]

    if not results:
        return {
            "summary": "검색 결과가 없습니다."
        }

    lines = []

    for index, document in enumerate(results, start=1):
        lines.append(f"{index}. {document['title']} - {document['content']}")

    return {
        "summary": "\n".join(lines)
    }


def final_answer_node(state: DocumentWorkflowState) -> dict:
    return {
        "final_answer": f"문서 검색 결과 요약입니다.\n\n{state['summary']}"
    }


graph_builder = StateGraph(DocumentWorkflowState)

graph_builder.add_node("prepare_query", prepare_query_node)
graph_builder.add_node("search", search_node)
graph_builder.add_node("summarize", summarize_node)
graph_builder.add_node("final_answer", final_answer_node)

graph_builder.add_edge(START, "prepare_query")
graph_builder.add_edge("prepare_query", "search")
graph_builder.add_edge("search", "summarize")
graph_builder.add_edge("summarize", "final_answer")
graph_builder.add_edge("final_answer", END)

graph = graph_builder.compile()

result = graph.invoke(
    {
        "user_input": "Agent",
        "query": "",
        "search_results": [],
        "summary": "",
        "final_answer": "",
    }
)

print(result["final_answer"])
```

이 예제는 단순하지만 LangGraph의 기본 구조를 모두 포함한다.

```text
State 정의
Node 정의
Edge 정의
Compile
Invoke
```

---

## 19. 조건부 Workflow 예제

이번에는 검색 결과가 없으면 검색어를 다시 작성하는 조건부 Workflow를 생각해보자.

```text
START
  ↓
search
  ↓
검색 결과 있음?
  ├─ yes → summarize
  └─ no  → rewrite_query
              ↓
            search
  ↓
END
```

이 구조에는 Conditional Edge가 필요하다.

```python
def route_after_search(state: DocumentWorkflowState) -> str:
    if state["search_results"]:
        return "summarize"

    return "rewrite_query"
```

Graph 연결은 다음과 같다.

```python
graph_builder.add_conditional_edges(
    "search",
    route_after_search,
    {
        "summarize": "summarize",
        "rewrite_query": "rewrite_query",
    }
)
```

검색어 재작성 Node는 다음과 같이 만들 수 있다.

```python
def rewrite_query_node(state: DocumentWorkflowState) -> dict:
    return {
        "query": "Agent"
    }
```

그리고 다시 검색 Node로 연결한다.

```python
graph_builder.add_edge("rewrite_query", "search")
```

이렇게 하면 검색 결과가 없을 때 검색어를 바꿔 다시 검색하는 Loop 구조가 된다.

---

## 20. Loop 구조와 주의사항

LangGraph는 Loop 구조를 표현할 수 있다.

예를 들어 다음과 같은 흐름이 가능하다.

```text
검색
  ↓
결과 없음
  ↓
검색어 수정
  ↓
다시 검색
```

하지만 Loop 구조에는 주의가 필요하다.

잘못 설계하면 무한 반복이 발생할 수 있다.

따라서 Loop에는 반드시 종료 조건이 필요하다.

예를 들어 State에 `retry_count`를 추가할 수 있다.

```python
class DocumentWorkflowState(TypedDict):
    user_input: str
    query: str
    search_results: list[dict]
    summary: str
    final_answer: str
    retry_count: int
```

Router에서 재시도 횟수를 확인한다.

```python
def route_after_search(state: DocumentWorkflowState) -> str:
    if state["search_results"]:
        return "summarize"

    if state["retry_count"] >= 2:
        return "summarize"

    return "rewrite_query"
```

이렇게 하면 최대 2회까지만 재검색하고, 그 이후에는 요약 단계로 넘어간다.

Enterprise 환경에서는 모든 Loop에 제한을 두는 것이 좋다.

```text
1. 최대 반복 횟수
2. 최대 실행 시간
3. 최대 Tool 호출 횟수
4. 실패 시 Human Review
```

---

## 21. LangGraph와 Memory

Step3-4에서 Memory를 학습했다.

LangGraph에서도 Memory는 매우 중요하다.

LangGraph에서 Memory는 크게 두 가지 관점으로 볼 수 있다.

```text
1. Workflow 실행 중 유지되는 State
2. 실행 이후에도 보존되는 Checkpoint 또는 외부 저장소
```

State는 한 번의 Graph 실행 중 유지되는 작업 상태이다.

```text
user_input
query
search_results
summary
final_answer
```

반면 장기 Memory는 여러 실행에 걸쳐 유지되는 정보이다.

```text
대화 이력
사용자 선호
이전 실행 결과
작업 로그
승인 이력
```

LangGraph는 Checkpointer와 함께 사용할 수 있으며, 이를 통해 Workflow 중간 상태를 저장하고 이어서 실행하는 구조로 확장할 수 있다.

이번 Step3-6에서는 우선 State 중심으로 이해하고, 이후 Enterprise 단계에서 Checkpoint와 장기 Memory를 확장하는 것이 좋다.

---

## 22. Human-in-the-Loop 구조

Enterprise Agent에서 중요한 구조 중 하나가 Human-in-the-Loop이다.

예를 들어 Agent가 보고서 초안을 만든 뒤 바로 제출하면 위험할 수 있다.

좋은 Workflow는 다음과 같다.

```text
보고서 초안 작성
   ↓
사용자 검토
   ↓
승인 여부
   ├─ 승인 → 최종 저장
   └─ 수정 요청 → 다시 작성
```

LangGraph에서는 이 구조를 Node와 Conditional Edge로 표현할 수 있다.

```text
draft_report
   ↓
review_required
   ↓
approved?
   ├─ yes → save_report
   └─ no  → revise_report
```

처음 실습에서는 실제 사용자 승인 기능을 구현하지 않아도 된다.

대신 State에 다음 값을 둔다.

```python
approval_status: str
```

예를 들어 다음 값을 사용할 수 있다.

```text
approved
rejected
pending
```

그리고 Conditional Edge에서 이 값을 보고 다음 Node를 결정한다.

---

## 23. LangGraph 기반 Agent와 기존 Agent 비교

기존 Step3-3 Agent는 다음 구조였다.

```text
사용자 입력
   ↓
select_tool
   ↓
execute_tool
   ↓
Final Answer
```

Step3-5 Planning Agent는 다음 구조였다.

```text
사용자 입력
   ↓
create_plan
   ↓
Task List
   ↓
execute_task
   ↓
Final Answer
```

Step3-6 LangGraph Agent는 다음 구조로 확장된다.

```text
사용자 입력
   ↓
Initial State
   ↓
Graph 실행
   ├─ Node
   ├─ Edge
   ├─ Conditional Edge
   └─ State Update
   ↓
Final State
   ↓
Final Answer
```

비교하면 다음과 같다.

| 구분 | Step3-3 기본 Agent | Step3-5 Planning Agent | Step3-6 LangGraph Agent |
|---|---|---|---|
| 실행 단위 | Tool Call | Task | Node |
| 흐름 제어 | if문 | Task List | Edge |
| 조건 분기 | 단순 if문 | Workflow 조건 | Conditional Edge |
| 상태 관리 | 단순 결과 | Workflow State | Graph State |
| 반복 실행 | 제한적 | 직접 구현 | Graph Loop 가능 |
| 확장성 | 낮음 | 중간 | 높음 |

---

## 24. Enterprise Workflow Agent 구조

기업 환경에서 LangGraph 기반 Workflow Agent는 다음 구조로 확장할 수 있다.

```text
사용자 / Open WebUI
        │
        ▼
Agent Gateway
        │
        ▼
LangGraph Workflow Agent
        │
        ├─ State
        ├─ Node
        ├─ Edge
        ├─ Conditional Edge
        ├─ Checkpoint
        └─ Human Review
        │
        ▼
Tool Executor
        │
        ▼
MCP / RAG / DB / API / File
```

이 구조에서 LangGraph는 Agent Runtime의 Workflow 제어 계층 역할을 한다.

```text
LangGraph:
- 어떤 순서로 실행할지 결정
- 상태를 관리
- 조건 분기 처리
- 반복 실행 제어
- 사람 승인 단계 연결

Tool Executor:
- 실제 도구 실행

MCP:
- 외부 시스템 도구 연동 표준화
```

즉, LangGraph와 MCP는 역할이 다르다.

```text
LangGraph:
Agent의 실행 흐름을 제어한다.

MCP:
Agent가 외부 시스템의 도구를 표준 방식으로 사용할 수 있게 한다.
```

---

## 25. 설치 준비

LangGraph를 사용하려면 Python 환경에 패키지를 설치해야 한다.

일반적으로 다음 명령을 사용한다.

```bash
python -m pip install langgraph
```

LangChain과 함께 사용할 경우 다음 패키지도 필요할 수 있다.

```bash
python -m pip install langchain langchain-core langgraph
```

실습 환경에서는 가상환경을 사용하는 것을 권장한다.

```bash
python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install langgraph
```

Windows PowerShell에서는 다음과 같이 활성화한다.

```powershell
.venv\Scripts\Activate.ps1
```

설치 확인은 다음과 같이 할 수 있다.

```bash
python -c "import langgraph; print('langgraph installed')"
```

---

## 26. 권장 실습 디렉터리 구조

이번 Step3-6 실습은 기존 `labs/agent`와 분리하여 `labs/langgraph`로 구성하는 것을 추천한다.

```text
labs
└── langgraph
    ├── README.md
    ├── 01_first_graph.py
    ├── 02_state_graph.py
    ├── 03_conditional_graph.py
    ├── 04_document_workflow_agent.py
    ├── 05_human_review_workflow.py
    └── sample_state.json
```

각 파일의 역할은 다음과 같다.

| 파일 | 역할 |
|---|---|
| `01_first_graph.py` | 가장 단순한 Graph 예제 |
| `02_state_graph.py` | State를 여러 Node가 갱신하는 예제 |
| `03_conditional_graph.py` | Conditional Edge 예제 |
| `04_document_workflow_agent.py` | 문서 검색 Workflow Agent 예제 |
| `05_human_review_workflow.py` | 사용자 승인 흐름 예제 |
| `sample_state.json` | 초기 State 샘플 데이터 |

이번 문서에서는 실습 파일의 방향을 설명하고, 별도 실습 패키지에서 실제 파일을 제공하는 것을 권장한다.

---

## 27. 실습 1: 첫 번째 Graph

첫 번째 실습 목표는 LangGraph의 최소 구조를 실행해보는 것이다.

Workflow는 다음과 같다.

```text
START
  ↓
hello
  ↓
END
```

학습 포인트는 다음이다.

```text
1. State 정의
2. Node 정의
3. StateGraph 생성
4. Node 등록
5. Edge 등록
6. Compile
7. Invoke
```

이 실습을 통해 LangGraph의 기본 실행 흐름을 확인한다.

---

## 28. 실습 2: State를 갱신하는 Graph

두 번째 실습에서는 여러 Node가 같은 State를 갱신한다.

Workflow는 다음과 같다.

```text
START
  ↓
prepare
  ↓
process
  ↓
finish
  ↓
END
```

State 예시는 다음과 같다.

```python
class WorkflowState(TypedDict):
    user_input: str
    prepared_text: str
    processed_text: str
    final_answer: str
```

각 Node는 다음 역할을 수행한다.

```text
prepare:
사용자 입력을 정리한다.

process:
정리된 입력을 처리한다.

finish:
최종 답변을 만든다.
```

이 실습의 목적은 State가 Node 사이에서 어떻게 전달되고 갱신되는지 이해하는 것이다.

---

## 29. 실습 3: Conditional Edge

세 번째 실습에서는 조건에 따라 다른 Node로 이동하는 구조를 만든다.

예시는 다음과 같다.

```text
START
  ↓
classify_request
  ↓
요청 유형
   ├─ search → search_node
   ├─ calculate → calculate_node
   └─ default → default_node
  ↓
END
```

State에 다음 값을 둔다.

```python
request_type: str
```

Router 함수는 이 값을 보고 다음 Node를 결정한다.

```python
def route_by_request_type(state: WorkflowState) -> str:
    return state["request_type"]
```

이 실습은 Agent가 사용자 요청에 따라 다른 Workflow 경로를 선택하는 구조를 보여준다.

---

## 30. 실습 4: 문서 Workflow Agent

네 번째 실습에서는 Step3-3에서 만든 문서 검색 Tool과 연결한다.

Workflow는 다음과 같다.

```text
START
  ↓
prepare_query
  ↓
search_documents
  ↓
has_results?
  ├─ yes → summarize
  └─ no  → no_result_answer
  ↓
END
```

이 실습은 실제 Agent에 가까운 구조이다.

```text
1. 사용자 요청을 State에 저장
2. 검색어 준비
3. 문서 검색 Tool 호출
4. 검색 결과 여부 판단
5. 결과 요약 또는 결과 없음 답변 생성
```

이 구조는 이후 RAG Tool, MCP Tool과 연결하기 좋은 기본 패턴이다.

---

## 31. 실습 5: Human Review Workflow

다섯 번째 실습에서는 사용자의 승인이 필요한 Workflow를 설계한다.

Workflow는 다음과 같다.

```text
START
  ↓
draft_answer
  ↓
review
  ↓
approved?
  ├─ yes → final_answer
  └─ no  → revise_answer
              ↓
            review
```

처음에는 실제 대화형 승인 대신 State 값으로 승인 여부를 처리한다.

```python
approval_status = "approved"
```

이 구조는 이후 다음 작업에 활용할 수 있다.

```text
1. 이메일 발송 전 승인
2. 보고서 저장 전 승인
3. DB 수정 전 승인
4. 티켓 생성 전 승인
```

---

## 32. LangGraph 설계 시 자주 하는 실수

---

### 32.1 State를 너무 크게 만든다

처음부터 모든 데이터를 State에 넣으면 복잡해진다.

좋은 방식은 필요한 값부터 작게 시작하는 것이다.

```text
처음:
user_input, result

이후:
query, search_results, summary, error, retry_count
```

State는 Workflow의 중심이므로 너무 복잡하면 디버깅이 어려워진다.

---

### 32.2 Node가 너무 많은 일을 한다

Node 하나가 검색, 요약, 답변 생성을 모두 하면 Workflow를 나눈 의미가 없다.

좋은 방식은 Node 역할을 작게 나누는 것이다.

```text
나쁜 예:
process_all

좋은 예:
prepare_query
search_documents
summarize_results
generate_answer
```

Node는 하나의 명확한 책임을 가지는 것이 좋다.

---

### 32.3 Conditional Edge의 반환값과 Mapping이 맞지 않는다

Conditional Edge에서 Router 함수가 반환하는 값은 Mapping에 정의된 key와 맞아야 한다.

예를 들어 Router가 `"yes"`를 반환하는데 Mapping에는 `"has_result"`만 있으면 오류가 발생할 수 있다.

좋은 방식은 반환값을 명확히 정하는 것이다.

```python
def route_after_search(state):
    if state["search_results"]:
        return "has_result"

    return "no_result"
```

Mapping도 같은 이름으로 둔다.

```python
{
    "has_result": "summarize",
    "no_result": "no_result_answer"
}
```

---

### 32.4 Loop 종료 조건을 두지 않는다

Loop가 있는 Workflow에는 반드시 종료 조건이 필요하다.

나쁜 예:

```text
검색 실패 → 검색어 수정 → 다시 검색 → 검색 실패 → 검색어 수정 → ...
```

좋은 예:

```text
검색 실패
  ↓
retry_count < 2 ?
  ├─ 예 → 검색어 수정
  └─ 아니오 → 결과 없음 답변
```

---

### 32.5 Graph를 너무 빨리 복잡하게 만든다

처음부터 복잡한 Multi Agent Graph를 만들면 이해하기 어렵다.

추천 순서는 다음과 같다.

```text
1. 단일 Node Graph
2. 순차 Graph
3. Conditional Graph
4. Loop Graph
5. Human Review Graph
6. Tool 연동 Graph
7. Multi Agent Graph
```

---

## 33. Enterprise 관점의 LangGraph 설계 원칙

기업 환경에서 LangGraph를 사용할 때는 다음 원칙이 중요하다.

```text
1. 업무 절차가 명확한 영역부터 적용한다.
2. 읽기 전용 Workflow부터 시작한다.
3. 쓰기 작업은 Human Review Node를 둔다.
4. 모든 Node 실행 결과를 로그로 남긴다.
5. State에 민감정보를 그대로 저장하지 않는다.
6. 실패 처리 정책을 Node별로 정의한다.
7. Loop에는 최대 반복 횟수를 둔다.
8. Tool 실행은 Tool Executor나 MCP Layer를 통해 통제한다.
9. Graph 구조를 문서화한다.
10. 운영 환경에서는 모니터링과 추적 기능을 함께 설계한다.
```

---

## 34. AI DATA Platform에서의 활용 예시

AI DATA Platform 프로젝트에서는 LangGraph를 다음 영역에 활용할 수 있다.

---

### 34.1 RAG 품질 점검 Workflow

```text
START
  ↓
문서 목록 확인
  ↓
Chunk 개수 확인
  ↓
검색 테스트
  ↓
답변 품질 평가
  ↓
개선 포인트 정리
  ↓
END
```

---

### 34.2 Open WebUI / Ollama 점검 Workflow

```text
START
  ↓
Docker 상태 확인
  ↓
Open WebUI 컨테이너 확인
  ↓
Ollama 서버 확인
  ↓
모델 목록 확인
  ↓
문제 여부 판단
  ↓
점검 보고서 작성
  ↓
END
```

---

### 34.3 제안서 작성 보조 Workflow

```text
START
  ↓
RFP 문서 요약
  ↓
요구사항 분류
  ↓
작성 목차 생성
  ↓
초안 작성
  ↓
검토 포인트 정리
  ↓
END
```

---

### 34.4 문서 품질 검토 Workflow

```text
START
  ↓
Markdown 문서 읽기
  ↓
목차 구조 확인
  ↓
누락 항목 확인
  ↓
표현 일관성 점검
  ↓
보완안 작성
  ↓
END
```

---

## 35. Step3-7 MCP와의 연결

Step3-6에서 LangGraph는 Workflow를 제어한다.

하지만 LangGraph만으로 외부 시스템 연동 표준이 해결되는 것은 아니다.

예를 들어 다음 시스템을 연결한다고 하자.

```text
파일 시스템
DB
RAG
Git
Jira
메일
캘린더
업무 API
```

각 시스템을 직접 Python 함수로 연결할 수도 있지만, 시스템이 많아지면 관리가 어려워진다.

이때 Step3-7에서 학습할 MCP가 필요하다.

```text
LangGraph:
어떤 순서로 어떤 Node를 실행할지 제어한다.

MCP:
Node가 사용할 외부 Tool을 표준 방식으로 제공한다.
```

관계를 그림으로 표현하면 다음과 같다.

```text
LangGraph Workflow Agent
        │
        ▼
Node
        │
        ▼
Tool Call
        │
        ▼
MCP Client
        │
        ▼
MCP Server
        │
        ▼
File / DB / RAG / API
```

따라서 Step3-6과 Step3-7은 서로 연결된다.

```text
Step3-6:
Agent의 실행 흐름을 Graph로 제어한다.

Step3-7:
Agent가 외부 시스템의 Tool을 표준 방식으로 사용하도록 만든다.
```

---

## 36. 핵심 정리

이번 문서의 핵심은 다음과 같다.

```text
1. LangGraph는 Agent Workflow를 Graph 구조로 표현하기 위한 도구이다.
2. LangGraph의 핵심 구성 요소는 State, Node, Edge이다.
3. State는 Workflow 전체에서 공유되는 상태 데이터이다.
4. Node는 State를 입력받아 작업을 수행하고 State 일부를 반환하는 함수이다.
5. Edge는 Node와 Node 사이의 실행 흐름을 정의한다.
6. Conditional Edge는 State를 보고 다음 Node를 동적으로 선택한다.
7. START와 END는 Workflow의 시작과 종료 지점이다.
8. Graph는 compile 후 invoke로 실행한다.
9. Step3-5의 Planning Workflow는 LangGraph의 StateGraph로 확장할 수 있다.
10. Enterprise 환경에서는 LangGraph로 Workflow를 제어하고, MCP로 외부 Tool 연동을 표준화할 수 있다.
```

한 문장으로 정리하면 다음과 같다.

> **LangGraph는 복잡한 Agent 업무 흐름을 State, Node, Edge로 구조화하여 제어하는 Workflow Agent 프레임워크이다.**

---

## 37. 다음 단계 예고

다음 문서는 다음과 같다.

```text
Step3-7. MCP 아키텍처 이해
docs/study/step3/step3_7_mcp_architecture_guide.md
```

다음 단계에서는 Agent가 외부 시스템을 도구로 사용할 때 필요한 표준 구조인 MCP를 학습한다.

다음 문서에서 다룰 내용은 다음과 같다.

```text
1. MCP가 필요한 이유
2. Tool Calling의 한계
3. MCP Client / Server 구조
4. MCP Tool
5. MCP Resource
6. MCP Prompt
7. Transport 방식
8. 보안과 권한
9. Enterprise MCP 아키텍처
10. LangGraph와 MCP의 관계
```

---

## 38. 참고 자료

아래 자료는 LangGraph를 이해하기 위한 참고 자료이다.

```text
LangGraph Graph API
https://docs.langchain.com/oss/python/langgraph/graph-api

LangGraph StateGraph Reference
https://reference.langchain.com/python/langgraph/graph/state/StateGraph

LangGraph Graphs Reference
https://reference.langchain.com/python/langgraph/graphs

LangChain Agents Documentation
https://docs.langchain.com/oss/python/langchain/agents
```

---

## 39. 부록: LangGraph 기본 코드 작성 순서

LangGraph 코드를 처음 작성할 때는 아래 순서를 따르면 된다.

```text
1. State 타입을 정의한다.
2. Node 함수를 작성한다.
3. StateGraph를 생성한다.
4. add_node로 Node를 등록한다.
5. add_edge로 실행 흐름을 연결한다.
6. 필요한 경우 add_conditional_edges를 사용한다.
7. START와 END를 연결한다.
8. compile()을 호출한다.
9. invoke()로 실행한다.
10. 최종 State를 확인한다.
```

---

## 40. 부록: Step3-6 실습 패키지 후보

Step3-6 실습 패키지를 만든다면 다음 파일 구성을 추천한다.

```text
labs/langgraph
├── README.md
├── 01_first_graph.py
├── 02_state_graph.py
├── 03_conditional_graph.py
├── 04_document_workflow_agent.py
├── 05_human_review_workflow.py
└── sample_state.json
```

각 파일의 학습 목적은 다음과 같다.

```text
01_first_graph.py:
가장 단순한 LangGraph 실행 구조 확인

02_state_graph.py:
여러 Node가 State를 갱신하는 구조 확인

03_conditional_graph.py:
조건에 따라 다음 Node가 달라지는 구조 확인

04_document_workflow_agent.py:
문서 검색 Tool과 LangGraph Workflow 연결

05_human_review_workflow.py:
승인 단계가 포함된 Workflow 구조 확인
```

---

## 41. 마무리

Step3-6은 AI Agent 학습에서 매우 중요한 단계이다.

Step3-3에서는 Agent가 Tool을 사용할 수 있음을 확인했다.

Step3-4에서는 Agent가 상태를 기억할 수 있음을 학습했다.

Step3-5에서는 복잡한 작업을 Planning과 Workflow로 나누는 방법을 학습했다.

이번 Step3-6에서는 그 Workflow를 LangGraph로 구현할 수 있는 구조를 학습했다.

이제 Agent는 단순한 도구 호출기를 넘어 다음 구조로 발전한다.

```text
목표 이해
   ↓
작업 계획
   ↓
Graph 기반 실행
   ↓
상태 관리
   ↓
조건 분기
   ↓
반복 실행
   ↓
최종 결과 생성
```

이 구조는 이후 MCP, Multi Agent, Enterprise Agent Platform으로 확장되는 기반이 된다.
