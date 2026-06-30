# Step3 Part2. AI Agent 심화 가이드

> AI DATA Platform 연구 프로젝트  
> Step3. AI Agent  
> Part2. AI Agent 심화  
> 문서 경로: `docs/study/step3/step3_part2_advanced_ai_agent_guide.md`  
> 작성일: 2026-06-30

---

## 1. 문서 목적

이 문서는 `Step3. AI Agent` 과정 중 **Part2. AI Agent 심화**에 해당하는 전체 가이드 문서이다.

Part1에서는 AI Agent의 기본 개념을 학습했다.

```text
Step3-1. AI Agent 개요
Step3-2. ReAct와 Tool Calling
Step3-3. 첫 번째 AI Agent 구현
Step3-4. Agent Memory와 상태 관리
```

Part1의 핵심은 다음과 같다.

```text
1. Agent는 LLM이 단순히 답변하는 구조가 아니다.
2. Agent는 목표를 이해하고, 필요한 도구를 선택하고, 실행 결과를 바탕으로 다음 행동을 판단한다.
3. Python 함수 하나도 Tool이 될 수 있다.
4. Tool Registry와 Tool Executor를 통해 도구 호출 구조를 만들 수 있다.
5. Memory를 통해 대화 이력과 작업 상태를 관리할 수 있다.
```

Part2에서는 여기서 한 단계 더 나아간다.

단순히 하나의 Tool을 호출하는 구조가 아니라, **복잡한 업무를 단계별로 계획하고, Workflow로 제어하고, 외부 시스템을 표준 방식으로 연결하는 구조**를 학습한다.

Part2의 핵심 주제는 다음과 같다.

```text
Step3-5. Planning Agent와 Workflow
Step3-6. LangGraph 기반 Workflow Agent
Step3-7. MCP 아키텍처 이해
Step3-8. MCP 기반 외부 시스템 연동
```

---

## 2. Part2 전체 학습 목표

Part2를 마치면 다음 내용을 이해하고 설명할 수 있어야 한다.

```text
1. 복잡한 사용자 요청을 작은 작업 단위로 분해할 수 있다.
2. Agent가 계획을 세우고 실행하는 구조를 이해할 수 있다.
3. 단순 Agent Loop와 Workflow Agent의 차이를 설명할 수 있다.
4. LangGraph의 State, Node, Edge 개념을 설명할 수 있다.
5. Graph 기반 Agent가 왜 Enterprise 업무에 적합한지 이해할 수 있다.
6. MCP가 왜 등장했는지 설명할 수 있다.
7. MCP의 Host, Client, Server 구조를 이해할 수 있다.
8. MCP의 Tools, Resources, Prompts 개념을 설명할 수 있다.
9. 파일, RAG, DB, API를 MCP Server로 노출하는 구조를 설계할 수 있다.
10. AI DATA Platform 관점에서 Agent Runtime, Workflow, MCP Layer의 위치를 이해할 수 있다.
```

---

## 3. Part2의 위치

전체 Step3에서 Part2의 위치는 다음과 같다.

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
│   ├─ Step3-6. LangGraph 기반 Workflow Agent
│   ├─ Step3-7. MCP 아키텍처 이해
│   └─ Step3-8. MCP 기반 외부 시스템 연동
│
└─ Part3. Enterprise AI Agent
    ├─ Step3-9. Multi Agent 협업
    └─ Step3-10. Enterprise AI Agent Platform
```

Part2는 Part1과 Part3 사이의 연결 구간이다.

```text
Part1:
단일 Agent의 기본 구조를 이해한다.

Part2:
Agent 실행 흐름을 계획, Workflow, Graph, MCP로 확장한다.

Part3:
여러 Agent와 Enterprise Platform 구조로 확장한다.
```

즉, Part2는 AI Agent를 단순 실습 수준에서 **업무 자동화 구조**로 발전시키는 단계이다.

---

## 4. 왜 Part2가 필요한가?

Part1에서 만든 Agent는 다음과 같은 구조였다.

```text
사용자 질문
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

이 구조는 간단한 작업에는 충분하다.

예를 들어 다음 작업은 단순 Agent로 처리할 수 있다.

```text
1. 계산하기
2. 문서 검색하기
3. 파일 하나 읽기
4. 직원 샘플 데이터 검색하기
5. 간단한 답변 생성하기
```

하지만 실제 업무 요청은 더 복잡하다.

예를 들어 사용자가 다음과 같이 요청했다고 하자.

```text
"AI DATA Platform 프로젝트 문서를 검토해서,
Step2와 Step3의 핵심 내용을 비교하고,
부족한 실습 파일을 찾아서,
추가해야 할 실습 목록을 정리해줘."
```

이 요청은 단순한 Tool 호출 하나로 끝나지 않는다.

필요한 작업은 다음처럼 나뉜다.

```text
1. 프로젝트 문서 목록 확인
2. Step2 문서 검색
3. Step3 문서 검색
4. 각 문서의 학습 목표 추출
5. 실습 파일이 있는지 확인
6. 부족한 실습 데이터 판단
7. 추가 실습 목록 작성
8. 최종 보고서 정리
```

이런 요청을 안정적으로 처리하려면 Agent에게 다음 능력이 필요하다.

```text
1. 작업 분해
2. 실행 순서 결정
3. 각 단계별 도구 선택
4. 중간 결과 저장
5. 실패 시 재시도 또는 우회
6. 최종 결과 통합
```

이것이 Part2에서 다루는 핵심이다.

---

## 5. Part2 전체 아키텍처 개요

Part2에서 학습할 구조를 전체적으로 표현하면 다음과 같다.

```text
사용자 요청
   ↓
Planning Agent
   ↓
작업 계획 생성
   ↓
Workflow Controller
   ↓
단계별 Node 실행
   ↓
Tool / MCP 호출
   ↓
State 업데이트
   ↓
최종 결과 생성
```

조금 더 상세하게 표현하면 다음과 같다.

```text
사용자
  │
  ▼
Agent Application
  │
  ├─ Planner
  │   └─ 작업 분해 / 실행 순서 결정
  │
  ├─ Workflow Runtime
  │   ├─ State
  │   ├─ Node
  │   └─ Edge
  │
  ├─ Tool Registry
  │   └─ 사용 가능한 도구 목록
  │
  ├─ MCP Client
  │   └─ 외부 MCP Server 연결
  │
  ▼
MCP Server / Local Tools
  │
  ├─ File Tool
  ├─ RAG Tool
  ├─ DB Tool
  └─ API Tool
```

---

# Step3-5. Planning Agent와 Workflow

---

## 6. Step3-5 학습 목표

`Step3-5. Planning Agent와 Workflow`에서는 Agent가 복잡한 작업을 어떻게 단계별로 나누고 실행하는지 학습한다.

학습 목표는 다음과 같다.

```text
1. Planning Agent가 필요한 이유를 이해한다.
2. 작업 분해(Task Decomposition)를 이해한다.
3. Plan과 Workflow의 차이를 설명할 수 있다.
4. 계획 수립 → 실행 → 검증 → 재계획 구조를 이해한다.
5. 단순 순차 실행과 조건 분기 Workflow의 차이를 이해한다.
6. AI DATA Platform 업무에 적용 가능한 Workflow 예시를 설계할 수 있다.
```

---

## 7. Planning Agent란 무엇인가?

Planning Agent는 사용자의 큰 목표를 작은 작업 단위로 나누고, 어떤 순서로 수행할지 결정하는 Agent이다.

단순 Agent는 보통 다음처럼 동작한다.

```text
사용자 질문
   ↓
도구 하나 선택
   ↓
도구 실행
   ↓
답변
```

반면 Planning Agent는 다음처럼 동작한다.

```text
사용자 목표
   ↓
작업 분해
   ↓
실행 계획 생성
   ↓
단계별 실행
   ↓
중간 결과 검토
   ↓
필요 시 계획 수정
   ↓
최종 결과 생성
```

즉, Planning Agent의 핵심은 **바로 실행하지 않고 먼저 계획을 세운다**는 점이다.

---

## 8. Plan과 Workflow의 차이

Plan과 Workflow는 비슷해 보이지만 역할이 다르다.

| 구분 | Plan | Workflow |
|---|---|---|
| 의미 | 해야 할 일의 목록과 순서 | 실제 실행 흐름 |
| 생성 주체 | Planner 또는 LLM | 애플리케이션 또는 Workflow Engine |
| 성격 | 비교적 유연함 | 비교적 명확함 |
| 예시 | 1. 문서 검색 2. 요약 3. 검토 | START → search_node → summarize_node → review_node → END |
| 변경 가능성 | 실행 중 변경 가능 | 설계에 따라 제한적으로 변경 |

쉽게 정리하면 다음과 같다.

```text
Plan:
무엇을 할지 정리한 계획표

Workflow:
그 계획을 실제로 실행하는 흐름
```

---

## 9. 작업 분해 예시

사용자 요청:

```text
"AI Agent Part2 문서를 만들고, 각 단계별 실습 파일도 설계해줘."
```

Planning Agent는 이 요청을 다음처럼 분해할 수 있다.

```text
1. Part2 전체 범위 확인
2. Step3-5의 학습 목표 정의
3. Step3-6의 학습 목표 정의
4. Step3-7의 학습 목표 정의
5. Step3-8의 학습 목표 정의
6. 각 단계별 실습 파일 구조 설계
7. 실습 데이터 설계
8. 최종 가이드 문서 작성
9. 누락 항목 검토
```

이렇게 분해하면 Agent는 큰 요청을 한 번에 처리하려고 하지 않고, 작은 작업을 순서대로 처리할 수 있다.

---

## 10. Planning Agent 실행 구조

Planning Agent의 기본 구조는 다음과 같다.

```text
사용자 요청
   ↓
create_plan()
   ↓
plan = [task1, task2, task3, ...]
   ↓
for task in plan:
    execute_task(task)
    save_result(task_result)
   ↓
review_results()
   ↓
final_answer()
```

Python 구조로 단순화하면 다음과 같다.

```python
def create_plan(user_request: str) -> list[dict]:
    return [
        {"step": 1, "task": "문서 검색", "tool": "search_documents"},
        {"step": 2, "task": "요약 작성", "tool": "summarizer"},
        {"step": 3, "task": "결과 검토", "tool": "reviewer"},
    ]


def execute_plan(plan: list[dict]) -> list[dict]:
    results = []

    for item in plan:
        result = execute_task(item)
        results.append(result)

    return results
```

---

## 11. Planning Agent에서 중요한 상태 정보

Planning Agent는 작업 중간 상태를 반드시 관리해야 한다.

필요한 상태 정보는 다음과 같다.

```text
1. 사용자 원본 요청
2. 생성된 계획
3. 현재 실행 중인 단계
4. 완료된 단계 목록
5. 실패한 단계 목록
6. 각 단계의 실행 결과
7. 최종 답변 생성 여부
```

예시 State는 다음과 같다.

```json
{
  "user_request": "Step3 Part2 문서를 만들어줘.",
  "plan": [
    {"step": 1, "task": "목차 설계", "status": "done"},
    {"step": 2, "task": "본문 작성", "status": "running"},
    {"step": 3, "task": "검토", "status": "pending"}
  ],
  "current_step": 2,
  "results": [],
  "errors": []
}
```

---

## 12. Workflow 유형

Workflow는 크게 세 가지 형태로 볼 수 있다.

---

### 12.1 순차 Workflow

가장 단순한 Workflow이다.

```text
START
  ↓
Step 1
  ↓
Step 2
  ↓
Step 3
  ↓
END
```

예시:

```text
문서 읽기 → 요약하기 → 검토하기 → 결과 출력
```

---

### 12.2 조건 분기 Workflow

실행 결과에 따라 다음 단계가 달라지는 Workflow이다.

```text
START
  ↓
검색
  ↓
검색 결과 있음?
  ├─ Yes → 요약
  └─ No  → 추가 질문
  ↓
END
```

예시:

```text
검색 결과가 충분하면 답변 생성
검색 결과가 부족하면 추가 검색 또는 사용자 확인
```

---

### 12.3 반복 Workflow

조건이 만족될 때까지 반복하는 Workflow이다.

```text
START
  ↓
계획 수립
  ↓
실행
  ↓
검토
  ↓
충분한가?
  ├─ No  → 계획 수정 후 재실행
  └─ Yes → 최종 답변
```

예시:

```text
보고서 초안 작성 → 품질 검토 → 부족하면 보완 → 최종본 생성
```

---

## 13. Step3-5 추천 실습 구조

`Step3-5`에서는 아래 실습 파일을 만드는 것을 추천한다.

```text
labs/agent_planning
├── README.md
├── 01_task_decomposition.py
├── 02_sequential_workflow.py
├── 03_conditional_workflow.py
├── 04_plan_execute_review.py
│
├── common
│   ├── __init__.py
│   ├── planner.py
│   ├── workflow_state.py
│   └── task_executor.py
│
└── sample_tasks
    ├── report_request.txt
    └── platform_check_request.txt
```

각 파일의 역할은 다음과 같다.

| 파일 | 역할 |
|---|---|
| `01_task_decomposition.py` | 사용자 요청을 작은 작업으로 나누는 실습 |
| `02_sequential_workflow.py` | 순차 Workflow 실행 실습 |
| `03_conditional_workflow.py` | 조건 분기 Workflow 실습 |
| `04_plan_execute_review.py` | 계획, 실행, 검토 흐름 통합 실습 |
| `planner.py` | 작업 계획 생성 함수 |
| `workflow_state.py` | Workflow 상태 구조 정의 |
| `task_executor.py` | 각 작업 실행 함수 |
| `sample_tasks/*.txt` | 실습용 사용자 요청 데이터 |

---

## 14. Step3-5 핵심 정리

```text
1. Planning Agent는 큰 요청을 작은 작업으로 나눈다.
2. Plan은 해야 할 일의 목록이다.
3. Workflow는 실제 실행 흐름이다.
4. 복잡한 업무는 순차, 조건 분기, 반복 Workflow로 표현할 수 있다.
5. Planning Agent는 중간 상태를 관리해야 한다.
6. Enterprise 업무 자동화에서는 계획, 실행, 검토가 분리되어야 한다.
```

한 문장으로 정리하면 다음과 같다.

> **Planning Agent는 복잡한 요청을 실행 가능한 작은 작업으로 나누고, 그 작업을 순서대로 수행하도록 만드는 구조이다.**

---

# Step3-6. LangGraph 기반 Workflow Agent

---

## 15. Step3-6 학습 목표

`Step3-6. LangGraph 기반 Workflow Agent`에서는 Workflow Agent를 직접 Graph 구조로 표현하는 방법을 학습한다.

학습 목표는 다음과 같다.

```text
1. LangGraph가 필요한 이유를 이해한다.
2. StateGraph의 개념을 이해한다.
3. State, Node, Edge의 역할을 설명할 수 있다.
4. 조건 분기 Edge를 이해한다.
5. Graph 기반 Agent 실행 흐름을 설계할 수 있다.
6. Memory, Persistence, Human-in-the-loop와 LangGraph의 관계를 이해한다.
```

---

## 16. LangGraph란 무엇인가?

LangGraph는 Agent와 Workflow를 Graph 기반으로 구성하기 위한 프레임워크이다.

LangGraph에서는 Agent 실행 흐름을 다음 구성 요소로 표현한다.

```text
State:
현재 Workflow의 상태

Node:
상태를 입력받아 작업을 수행하고 상태를 업데이트하는 함수

Edge:
어떤 Node 다음에 어떤 Node를 실행할지 결정하는 연결

Graph:
State, Node, Edge로 구성된 전체 실행 흐름
```

LangGraph 공식 문서에서도 Graph API의 핵심 개념을 State, Nodes, Edges로 설명한다.

---

## 17. 왜 LangGraph가 필요한가?

단순 Agent Loop는 아래처럼 작성할 수 있다.

```python
while not done:
    action = llm_decide_next_action(state)
    result = execute_tool(action)
    state = update_state(state, result)
```

이 구조는 처음에는 간단하지만, 업무가 복잡해질수록 관리가 어려워진다.

문제는 다음과 같다.

```text
1. 단계가 많아지면 코드가 복잡해진다.
2. 조건 분기가 많아지면 흐름을 파악하기 어렵다.
3. 중간 상태 저장이 어렵다.
4. 실패한 지점부터 재시작하기 어렵다.
5. 사람 승인 절차를 넣기 어렵다.
6. 여러 Node의 실행 이력을 추적하기 어렵다.
```

LangGraph는 이런 문제를 Graph 구조로 해결한다.

```text
복잡한 Agent 흐름을 Node와 Edge로 분리한다.
각 Node는 하나의 책임만 가진다.
State는 전체 흐름에서 공유된다.
조건에 따라 다음 Node를 선택할 수 있다.
중간 상태 저장과 재개 구조를 만들 수 있다.
```

---

## 18. State란 무엇인가?

State는 Graph 실행 중 공유되는 상태 데이터이다.

예를 들어 보고서 작성 Workflow의 State는 다음과 같을 수 있다.

```python
from typing import TypedDict


class ReportState(TypedDict):
    user_request: str
    plan: list[str]
    search_results: list[str]
    draft: str
    review_result: str
    final_answer: str
```

각 Node는 이 State를 입력으로 받고, 필요한 값을 추가하거나 수정한다.

```text
planner_node:
State에 plan 추가

search_node:
State에 search_results 추가

draft_node:
State에 draft 추가

review_node:
State에 review_result 추가
```

State는 Agent의 작업 메모리이자 Workflow의 실행 컨텍스트이다.

---

## 19. Node란 무엇인가?

Node는 실제 작업을 수행하는 함수이다.

LangGraph에서 Node는 일반적으로 다음처럼 동작한다.

```text
입력:
현재 State

처리:
특정 작업 수행

출력:
업데이트할 State 일부
```

예시:

```python
def planner_node(state: ReportState) -> dict:
    user_request = state["user_request"]

    plan = [
        "관련 문서 검색",
        "핵심 내용 요약",
        "보고서 초안 작성",
        "초안 검토",
    ]

    return {"plan": plan}
```

중요한 점은 Node가 전체 State를 모두 새로 만들 필요는 없다는 것이다.  
Node는 보통 변경할 값만 반환한다.

---

## 20. Edge란 무엇인가?

Edge는 Node와 Node를 연결하는 흐름이다.

가장 단순한 Edge는 고정 연결이다.

```text
planner_node → search_node
search_node → draft_node
draft_node → review_node
review_node → final_node
```

조건 분기 Edge는 State 값에 따라 다음 Node가 달라진다.

```text
review_node
  ├─ 통과 → final_node
  └─ 보완 필요 → draft_node
```

예시 조건 함수:

```python
def route_after_review(state: ReportState) -> str:
    if state["review_result"] == "pass":
        return "final"
    return "rewrite"
```

---

## 21. LangGraph 기반 Workflow 예시

보고서 작성 Workflow를 Graph로 표현하면 다음과 같다.

```text
START
  ↓
planner
  ↓
search
  ↓
draft
  ↓
review
  ↓
review 결과?
  ├─ pass    → final
  └─ rewrite → draft
  ↓
END
```

이 구조는 기존 Python 코드보다 흐름을 명확하게 보여준다.

---

## 22. LangGraph와 Memory / Persistence

Agent Workflow는 중간 상태를 저장할 수 있어야 한다.

예를 들어 보고서 작성 중 다음 상황이 발생할 수 있다.

```text
1. 중간에 오류가 발생했다.
2. 사용자 승인이 필요하다.
3. 시간이 오래 걸려 나중에 이어서 실행해야 한다.
4. 실행 이력을 확인해야 한다.
```

LangGraph는 Persistence를 통해 Graph 상태를 저장하고 다시 이어서 실행할 수 있는 구조를 제공한다.

이 개념은 Step3-4에서 다룬 Memory와 연결된다.

```text
Step3-4 Memory:
대화 이력과 작업 상태 저장

Step3-6 LangGraph Persistence:
Graph 실행 상태 저장과 재개
```

---

## 23. LangGraph와 Human-in-the-loop

Enterprise 환경에서는 Agent가 모든 작업을 자동 실행하면 위험하다.

특히 다음 작업은 사람의 승인 절차가 필요하다.

```text
1. 이메일 발송
2. DB 수정
3. 파일 삭제
4. 티켓 생성
5. 운영 배포
6. 외부 시스템 반영
```

LangGraph는 사람 승인 단계를 Workflow 중간에 넣는 구조를 만들기 좋다.

예시:

```text
draft_email
  ↓
approval_node
  ↓
승인 여부?
  ├─ approve → send_email
  ├─ edit    → revise_email
  └─ reject  → end
```

이 구조는 실제 기업 Agent에서 매우 중요하다.

---

## 24. Step3-6 추천 실습 구조

`Step3-6`에서는 아래 실습 파일을 추천한다.

```text
labs/langgraph_agent
├── README.md
├── 01_simple_graph.py
├── 02_conditional_graph.py
├── 03_report_workflow_agent.py
├── 04_human_approval_mock.py
│
├── nodes
│   ├── __init__.py
│   ├── planner_node.py
│   ├── search_node.py
│   ├── draft_node.py
│   ├── review_node.py
│   └── final_node.py
│
├── common
│   ├── __init__.py
│   └── state.py
│
└── sample_docs
    ├── incident_log.md
    └── rag_status.md
```

각 파일의 역할은 다음과 같다.

| 파일 | 역할 |
|---|---|
| `01_simple_graph.py` | 가장 단순한 StateGraph 실행 실습 |
| `02_conditional_graph.py` | 조건 분기 Edge 실습 |
| `03_report_workflow_agent.py` | 보고서 작성 Workflow Agent 실습 |
| `04_human_approval_mock.py` | 승인 절차 Mock 실습 |
| `nodes/*.py` | 각 Node 함수 분리 |
| `common/state.py` | Graph State 타입 정의 |

---

## 25. Step3-6 핵심 정리

```text
1. LangGraph는 Agent Workflow를 Graph로 표현하는 프레임워크이다.
2. State는 Workflow의 현재 상태이다.
3. Node는 State를 입력받아 작업을 수행하는 함수이다.
4. Edge는 다음에 실행할 Node를 결정한다.
5. 조건 분기를 통해 복잡한 업무 흐름을 표현할 수 있다.
6. Persistence는 중간 상태 저장과 재개에 필요하다.
7. Human-in-the-loop는 Enterprise Agent에서 중요한 통제 장치이다.
```

한 문장으로 정리하면 다음과 같다.

> **LangGraph는 복잡한 Agent 실행 흐름을 State, Node, Edge로 나누어 안정적으로 제어하기 위한 Graph 기반 Workflow 구조이다.**

---

# Step3-7. MCP 아키텍처 이해

---

## 26. Step3-7 학습 목표

`Step3-7. MCP 아키텍처 이해`에서는 Agent가 외부 시스템을 표준 방식으로 연결하는 MCP 구조를 학습한다.

학습 목표는 다음과 같다.

```text
1. MCP가 등장한 배경을 이해한다.
2. Tool Calling과 MCP의 관계를 설명할 수 있다.
3. MCP의 Host, Client, Server 구조를 이해한다.
4. MCP Server가 제공하는 Tools, Resources, Prompts 개념을 이해한다.
5. MCP가 Enterprise Agent 구조에서 어떤 위치를 가지는지 설명할 수 있다.
6. MCP 적용 시 보안과 권한 통제가 왜 중요한지 이해한다.
```

---

## 27. MCP란 무엇인가?

MCP는 Model Context Protocol의 약자이다.

MCP는 LLM 애플리케이션과 외부 데이터, 도구, 시스템을 연결하기 위한 표준 프로토콜이다.

Agent는 다양한 외부 시스템을 사용해야 한다.

```text
1. 파일 시스템
2. RAG 검색 시스템
3. 데이터베이스
4. 업무 API
5. Git
6. Jira
7. Slack
8. Mail
9. Calendar
10. 운영 로그
```

각 시스템을 매번 서로 다른 방식으로 연결하면 구조가 복잡해진다.

MCP는 이 연결 방식을 표준화한다.

```text
Agent Application
   ↓
MCP Client
   ↓
MCP Server
   ↓
External System
```

---

## 28. Tool Calling과 MCP의 관계

Tool Calling은 LLM이 외부 도구를 호출하는 개념이다.

```json
{
  "tool_name": "search_documents",
  "arguments": {
    "query": "AI Agent"
  }
}
```

MCP는 이런 도구들을 외부 시스템과 연결하는 표준 계층이다.

관계는 다음과 같다.

```text
Tool Calling:
도구를 호출하는 개념

MCP:
도구를 표준 방식으로 노출하고 연결하는 프로토콜
```

즉, MCP는 Tool Calling을 대체하는 것이 아니다.  
MCP는 Tool Calling을 더 확장 가능하고 표준화된 방식으로 구현하게 해준다.

---

## 29. MCP 기본 구조

MCP의 기본 구조는 다음과 같다.

```text
MCP Host
  │
  ├─ MCP Client
  │    │
  │    ▼
  │  MCP Server A
  │    └─ File Tools
  │
  ├─ MCP Client
  │    │
  │    ▼
  │  MCP Server B
  │    └─ DB Tools
  │
  └─ MCP Client
       │
       ▼
     MCP Server C
       └─ RAG Tools
```

각 구성 요소의 역할은 다음과 같다.

| 구성 요소 | 설명 |
|---|---|
| MCP Host | AI 애플리케이션 또는 Agent Runtime |
| MCP Client | Host 내부에서 MCP Server와 통신하는 클라이언트 |
| MCP Server | 외부 시스템의 기능을 표준 방식으로 제공하는 서버 |
| Tool | LLM/Agent가 호출할 수 있는 실행 기능 |
| Resource | 파일, DB 레코드, API 응답 등 참조 가능한 데이터 |
| Prompt | 재사용 가능한 프롬프트 템플릿 |

---

## 30. MCP Host

MCP Host는 사용자가 실제로 접하는 AI 애플리케이션이다.

예시는 다음과 같다.

```text
1. ChatGPT
2. Claude Desktop
3. Cursor
4. VS Code 기반 AI 도구
5. 사내 Agent Portal
6. Open WebUI 확장 Agent
7. AI DATA Platform Agent Gateway
```

Host는 사용자의 요청을 받고, 필요한 경우 MCP Client를 통해 MCP Server와 통신한다.

---

## 31. MCP Client

MCP Client는 Host 안에서 MCP Server와 연결되는 구성 요소이다.

역할은 다음과 같다.

```text
1. MCP Server와 연결한다.
2. Server가 제공하는 기능을 조회한다.
3. Tool 목록을 가져온다.
4. Resource 목록을 가져온다.
5. Tool 실행 요청을 보낸다.
6. 실행 결과를 Host 또는 Agent Runtime에 전달한다.
```

Agent 관점에서는 MCP Client가 외부 도구를 가져오는 통로 역할을 한다.

---

## 32. MCP Server

MCP Server는 특정 외부 시스템을 MCP 방식으로 노출하는 서버이다.

예를 들어 파일 시스템 MCP Server는 다음 기능을 제공할 수 있다.

```text
1. 파일 목록 조회
2. 파일 읽기
3. 파일 검색
4. 허용된 경로 내 파일 생성
5. 허용된 경로 내 파일 수정
```

DB MCP Server는 다음 기능을 제공할 수 있다.

```text
1. 테이블 목록 조회
2. SELECT 쿼리 실행
3. 사전에 정의된 업무 조회 실행
4. 데이터 Dictionary 조회
```

RAG MCP Server는 다음 기능을 제공할 수 있다.

```text
1. 문서 검색
2. Chunk 조회
3. Collection 목록 조회
4. 인덱싱 상태 확인
```

---

## 33. MCP Tools

MCP Tool은 Agent가 호출할 수 있는 실행 기능이다.

예시:

```text
read_file
search_documents
query_database
get_api_status
create_ticket
send_message
```

Tool은 실행을 동반하므로 가장 주의가 필요하다.

특히 쓰기 Tool은 반드시 통제해야 한다.

```text
1. 파일 수정
2. DB 변경
3. 메일 발송
4. 티켓 생성
5. 배포 실행
```

---

## 34. MCP Resources

Resource는 Agent가 참조할 수 있는 데이터이다.

예시는 다음과 같다.

```text
1. 파일 내용
2. DB 레코드
3. API 응답
4. 로그 파일
5. 이미지
6. 운영 상태 데이터
```

Tool과 Resource의 차이는 다음과 같다.

| 구분 | Tool | Resource |
|---|---|---|
| 성격 | 실행 기능 | 참조 데이터 |
| 예시 | search_documents 실행 | 특정 문서 내용 |
| 위험도 | 상대적으로 높음 | 상대적으로 낮음 |
| 권한 통제 | 매우 중요 | 중요 |

---

## 35. MCP Prompts

Prompt는 MCP Server가 제공할 수 있는 재사용 가능한 프롬프트 템플릿이다.

예시:

```text
1. 장애 보고서 작성 Prompt
2. 문서 요약 Prompt
3. 코드 리뷰 Prompt
4. RFP 요구사항 분석 Prompt
5. 회의록 정리 Prompt
```

Prompt를 MCP Server에서 관리하면 여러 Agent가 동일한 업무 프롬프트를 재사용할 수 있다.

---

## 36. MCP 아키텍처와 AI DATA Platform

AI DATA Platform에서 MCP는 다음 위치에 놓을 수 있다.

```text
사용자 / Open WebUI
        │
        ▼
AI Agent Gateway
        │
        ▼
Agent Runtime / LangGraph Workflow
        │
        ▼
MCP Client Layer
        │
        ▼
MCP Server Layer
        │
        ├─ File MCP Server
        ├─ RAG MCP Server
        ├─ DB MCP Server
        ├─ Git MCP Server
        └─ API MCP Server
        │
        ▼
Enterprise Systems
```

MCP를 도입하면 다음 장점이 있다.

```text
1. 외부 시스템 연결 방식이 표준화된다.
2. Agent마다 도구 연동 코드를 중복 작성하지 않아도 된다.
3. 도구 목록을 동적으로 조회할 수 있다.
4. 시스템별 Tool을 독립적으로 개발하고 배포할 수 있다.
5. Enterprise Agent Platform 구조로 확장하기 쉽다.
```

---

## 37. MCP 보안 관점

MCP는 강력하지만 보안 설계가 반드시 필요하다.

주의해야 할 점은 다음과 같다.

```text
1. MCP Server가 어떤 도구를 노출하는지 명확히 관리해야 한다.
2. 파일 시스템 접근 경로를 제한해야 한다.
3. DB는 SELECT 중심으로 시작해야 한다.
4. 쓰기 작업은 승인 절차를 둬야 한다.
5. Tool 입력값을 검증해야 한다.
6. 사용자 권한과 Tool 실행 권한을 연결해야 한다.
7. 실행 로그를 남겨야 한다.
8. 민감정보를 응답과 로그에 그대로 노출하지 않아야 한다.
```

처음 MCP를 실습할 때는 다음 원칙을 추천한다.

```text
1. 읽기 전용 Tool부터 만든다.
2. 로컬 샘플 데이터로 시작한다.
3. 파일 접근 범위를 프로젝트 디렉터리 내부로 제한한다.
4. DB는 SQLite 샘플 DB로 시작한다.
5. 외부 API는 Mock API 또는 공개 테스트 API로 시작한다.
```

---

## 38. Step3-7 추천 실습 구조

`Step3-7`은 개념 중심 문서이므로 복잡한 코드를 만들기보다 MCP 구조를 이해하는 실습을 추천한다.

```text
labs/mcp_architecture
├── README.md
├── 01_mcp_concept_map.md
├── 02_tool_resource_prompt_example.md
├── 03_mcp_message_flow.md
│
└── diagrams
    ├── mcp_basic_architecture.md
    └── ai_data_platform_mcp_layer.md
```

추천 산출물은 다음과 같다.

```text
1. MCP 구성 요소 설명 표
2. Host / Client / Server 흐름도
3. Tool / Resource / Prompt 비교표
4. AI DATA Platform MCP Layer 설계도
5. 보안 체크리스트
```

---

## 39. Step3-7 핵심 정리

```text
1. MCP는 LLM 애플리케이션과 외부 시스템을 연결하는 표준 프로토콜이다.
2. MCP는 Host, Client, Server 구조를 가진다.
3. MCP Server는 Tools, Resources, Prompts를 제공할 수 있다.
4. Tool Calling은 도구 호출 개념이고, MCP는 도구 연결을 표준화하는 계층이다.
5. Enterprise 환경에서는 MCP 도입 시 권한, 로그, 승인, 경로 제한이 중요하다.
```

한 문장으로 정리하면 다음과 같다.

> **MCP는 Agent가 외부 시스템의 도구와 데이터를 표준 방식으로 사용할 수 있게 해주는 연결 계층이다.**

---

# Step3-8. MCP 기반 외부 시스템 연동

---

## 40. Step3-8 학습 목표

`Step3-8. MCP 기반 외부 시스템 연동`에서는 파일, RAG, DB, API를 MCP 구조로 연결하는 방법을 실습한다.

학습 목표는 다음과 같다.

```text
1. MCP Server를 외부 시스템별로 분리하는 이유를 이해한다.
2. File MCP Server 구조를 설계할 수 있다.
3. RAG MCP Server 구조를 설계할 수 있다.
4. DB MCP Server 구조를 설계할 수 있다.
5. API MCP Server 구조를 설계할 수 있다.
6. Agent Runtime에서 MCP Client를 통해 Tool을 사용하는 흐름을 이해한다.
7. 읽기 도구와 쓰기 도구를 분리하여 안전하게 설계할 수 있다.
```

---

## 41. 외부 시스템 연동 대상

Step3-8에서 다룰 외부 시스템은 다음 네 가지로 잡는 것이 좋다.

```text
1. File
2. RAG
3. DB
4. API
```

이 네 가지는 Enterprise Agent에서 가장 기본적인 연동 대상이다.

| 연동 대상 | 목적 | 예시 Tool |
|---|---|---|
| File | 프로젝트 문서 읽기 | `list_files`, `read_file`, `search_files` |
| RAG | 문서 검색 | `search_rag_documents`, `get_chunk` |
| DB | 정형 데이터 조회 | `list_tables`, `query_readonly` |
| API | 외부 서비스 조회 | `get_status`, `search_ticket`, `get_weather_mock` |

---

## 42. File MCP Server 설계

File MCP Server는 프로젝트 내부 파일을 안전하게 읽기 위한 MCP Server이다.

초기 실습에서는 읽기 기능만 제공하는 것이 좋다.

추천 Tool:

```text
list_files
read_file
search_files
```

각 Tool의 역할은 다음과 같다.

| Tool | 설명 |
|---|---|
| `list_files` | 허용된 디렉터리 내부 파일 목록 조회 |
| `read_file` | 허용된 디렉터리 내부 텍스트 파일 읽기 |
| `search_files` | 파일명 또는 파일 내용 키워드 검색 |

보안 원칙:

```text
1. 프로젝트 루트 밖의 파일 접근 금지
2. 상대 경로만 허용
3. `../` 경로 차단
4. 대용량 파일 읽기 제한
5. 바이너리 파일 읽기 제한
```

---

## 43. RAG MCP Server 설계

RAG MCP Server는 Step2에서 만든 RAG 검색 기능을 MCP Tool로 노출하는 구조이다.

추천 Tool:

```text
search_rag_documents
get_rag_chunk
list_collections
check_index_status
```

각 Tool의 역할은 다음과 같다.

| Tool | 설명 |
|---|---|
| `search_rag_documents` | 질문과 유사한 문서 Chunk 검색 |
| `get_rag_chunk` | 특정 Chunk 원문 조회 |
| `list_collections` | Vector DB Collection 목록 조회 |
| `check_index_status` | 인덱싱 상태 확인 |

RAG MCP Server 흐름:

```text
Agent
  ↓
MCP Client
  ↓
RAG MCP Server
  ↓
Embedding Model
  ↓
Vector DB
  ↓
검색 결과 반환
```

AI DATA Platform에서는 기존 `labs/rag` 실습과 연결하면 좋다.

---

## 44. DB MCP Server 설계

DB MCP Server는 데이터베이스를 조회하기 위한 MCP Server이다.

초기 실습에서는 SQLite를 사용하는 것을 추천한다.

추천 Tool:

```text
list_tables
describe_table
query_readonly
```

주의할 점은 DB Tool은 매우 위험할 수 있다는 것이다.

초기에는 반드시 읽기 전용으로 제한한다.

```text
허용:
SELECT

금지:
INSERT
UPDATE
DELETE
DROP
ALTER
TRUNCATE
CREATE
```

보안 원칙:

```text
1. SELECT만 허용
2. 쿼리 길이 제한
3. 결과 건수 제한
4. 민감 컬럼 마스킹
5. 실행 로그 저장
6. 사용자 권한별 테이블 접근 제한
```

---

## 45. API MCP Server 설계

API MCP Server는 외부 또는 내부 API를 호출하는 MCP Server이다.

초기 실습에서는 Mock API 방식으로 시작하는 것이 좋다.

추천 Tool:

```text
get_platform_status
get_ticket_status
search_api_catalog
```

예시:

```text
get_platform_status:
- Ollama, Open WebUI, ChromaDB 상태를 Mock 데이터로 반환

get_ticket_status:
- 장애 티켓 상태를 Mock 데이터로 반환

search_api_catalog:
- 연동 가능한 API 목록 검색
```

운영 환경에서는 API Key, 인증 토큰, Rate Limit, Timeout 관리가 필수이다.

---

## 46. Step3-8 전체 연동 아키텍처

Step3-8의 최종 구조는 다음과 같다.

```text
사용자
  │
  ▼
Agent Application
  │
  ▼
MCP Client
  │
  ├───────────────┬───────────────┬───────────────┐
  ▼               ▼               ▼               ▼
File MCP       RAG MCP          DB MCP          API MCP
Server         Server           Server          Server
  │               │               │               │
  ▼               ▼               ▼               ▼
sample_docs     ChromaDB        SQLite          Mock API
```

---

## 47. Step3-8 추천 실습 구조

`Step3-8`에서는 다음 실습 패키지를 추천한다.

```text
labs/mcp_integration
├── README.md
├── 01_file_mcp_server.py
├── 02_rag_mcp_server.py
├── 03_db_mcp_server.py
├── 04_api_mcp_server.py
├── 05_agent_mcp_client.py
│
├── servers
│   ├── __init__.py
│   ├── file_server.py
│   ├── rag_server.py
│   ├── db_server.py
│   └── api_server.py
│
├── client
│   ├── __init__.py
│   └── mcp_client.py
│
├── sample_docs
│   ├── agent_guide.md
│   └── rag_guide.md
│
├── sample_db
│   └── platform.db
│
└── sample_api
    └── platform_status.json
```

각 파일의 역할은 다음과 같다.

| 파일 | 역할 |
|---|---|
| `01_file_mcp_server.py` | File MCP Server 단독 실행 실습 |
| `02_rag_mcp_server.py` | RAG MCP Server 단독 실행 실습 |
| `03_db_mcp_server.py` | DB MCP Server 단독 실행 실습 |
| `04_api_mcp_server.py` | API MCP Server 단독 실행 실습 |
| `05_agent_mcp_client.py` | Agent가 MCP Client를 통해 각 Server Tool을 호출하는 통합 실습 |
| `servers/*.py` | 외부 시스템별 MCP Server 역할 |
| `client/mcp_client.py` | MCP Client Mock 구현 |
| `sample_docs` | 파일/RAG 실습용 문서 |
| `sample_db` | DB 실습용 SQLite 데이터 |
| `sample_api` | API 실습용 Mock 응답 데이터 |

---

## 48. Step3-8 실습 순서

추천 실습 순서는 다음과 같다.

```text
1. File MCP Server Mock 구현
2. File Tool 실행 확인
3. API MCP Server Mock 구현
4. API Tool 실행 확인
5. SQLite 샘플 DB 생성
6. DB MCP Server 읽기 전용 조회 구현
7. RAG MCP Server 구조 설계
8. Agent MCP Client에서 각 MCP Server 호출
9. Tool 실행 로그 출력
10. 보안 체크리스트 적용
```

처음부터 실제 MCP SDK를 깊게 사용하기보다, 먼저 MCP의 구조를 Mock으로 이해한 뒤 실제 SDK로 확장하는 방식이 좋다.

---

## 49. MCP 연동과 LangGraph의 결합

Step3-8에서 만든 MCP Tool들은 Step3-6의 LangGraph Workflow와 결합할 수 있다.

예를 들어 플랫폼 점검 Workflow는 다음과 같이 구성할 수 있다.

```text
START
  ↓
check_file_config_node
  ↓
check_rag_index_node
  ↓
check_db_status_node
  ↓
check_api_status_node
  ↓
generate_report_node
  ↓
END
```

각 Node는 MCP Tool을 호출한다.

```text
check_file_config_node:
File MCP Server 호출

check_rag_index_node:
RAG MCP Server 호출

check_db_status_node:
DB MCP Server 호출

check_api_status_node:
API MCP Server 호출
```

이렇게 하면 Workflow 제어는 LangGraph가 담당하고, 외부 시스템 연결은 MCP가 담당하게 된다.

```text
LangGraph:
업무 흐름 제어

MCP:
외부 시스템 연결 표준화
```

---

## 50. Step3-8 핵심 정리

```text
1. MCP는 외부 시스템을 Agent Tool로 연결하기 위한 표준 계층이다.
2. File, RAG, DB, API는 Enterprise Agent의 기본 연동 대상이다.
3. 처음에는 읽기 전용 Tool부터 시작하는 것이 안전하다.
4. DB Tool은 반드시 SELECT 중심으로 제한해야 한다.
5. File Tool은 프로젝트 경로 밖 접근을 차단해야 한다.
6. API Tool은 인증, Timeout, Rate Limit을 고려해야 한다.
7. LangGraph와 MCP를 결합하면 업무 흐름 제어와 시스템 연동을 분리할 수 있다.
```

한 문장으로 정리하면 다음과 같다.

> **Step3-8의 핵심은 Agent가 파일, RAG, DB, API를 직접 제각각 연결하지 않고 MCP Layer를 통해 표준화된 Tool로 사용하는 구조를 만드는 것이다.**

---

# Part2 통합 정리

---

## 51. Part2 전체 흐름 다시 보기

Part2 전체 흐름은 다음과 같다.

```text
Step3-5:
복잡한 요청을 작은 작업으로 나누는 Planning을 학습한다.

Step3-6:
Planning된 작업 흐름을 LangGraph 기반 Workflow로 제어한다.

Step3-7:
외부 시스템 연동을 표준화하는 MCP 아키텍처를 이해한다.

Step3-8:
File, RAG, DB, API를 MCP로 연결하는 구조를 실습한다.
```

Part2를 하나의 그림으로 정리하면 다음과 같다.

```text
사용자 요청
   ↓
Planning Agent
   ↓
작업 계획
   ↓
LangGraph Workflow
   ↓
State / Node / Edge
   ↓
MCP Client
   ↓
MCP Server
   ↓
File / RAG / DB / API
   ↓
결과 통합
   ↓
최종 답변
```

---

## 52. Part2와 Part3의 연결

Part2를 마치면 다음 구조를 이해하게 된다.

```text
1. Agent가 복잡한 작업을 계획한다.
2. Workflow로 실행 흐름을 통제한다.
3. LangGraph로 State 기반 Graph 실행을 구성한다.
4. MCP로 외부 시스템 Tool을 표준화한다.
```

이 구조는 Part3의 기반이 된다.

Part3에서는 다음으로 확장한다.

```text
Step3-9. Multi Agent 협업
- Planner Agent, Research Agent, Writer Agent, QA Agent처럼 역할을 나눈다.

Step3-10. Enterprise AI Agent Platform
- Agent Gateway, Tool Registry, MCP Layer, Observability, Security, Approval 구조를 통합한다.
```

즉, Part2는 단일 Agent를 Enterprise Agent Platform으로 확장하기 위한 중간 단계이다.

---

## 53. AI DATA Platform 관점의 최종 구조

AI DATA Platform에서 Part2까지 학습한 구조는 다음과 같이 연결된다.

```text
Step1. Local LLM
  ↓
LLM 실행 기반 확보

Step2. RAG
  ↓
문서 검색 기반 확보

Step3 Part1. Agent 기초
  ↓
Tool Calling / Memory / Executor 이해

Step3 Part2. Agent 심화
  ↓
Planning / Workflow / LangGraph / MCP 이해

Step3 Part3. Enterprise Agent
  ↓
Multi Agent / Agent Platform / 운영 통제 구조
```

아키텍처로 표현하면 다음과 같다.

```text
사용자 / Open WebUI / Agent Portal
        │
        ▼
AI Agent Gateway
        │
        ▼
Agent Runtime
        │
        ├─ Planner
        ├─ Memory
        ├─ LangGraph Workflow
        ├─ Tool Registry
        ├─ Policy Guard
        └─ Execution Log
        │
        ▼
MCP Layer
        │
        ├─ File MCP Server
        ├─ RAG MCP Server
        ├─ DB MCP Server
        ├─ API MCP Server
        └─ Git/Jira/Mail MCP Server
        │
        ▼
Enterprise Systems
```

---

## 54. Part2에서 반드시 기억해야 할 문장

```text
1. Planning은 복잡한 요청을 작은 작업으로 나누는 것이다.
2. Workflow는 그 작업을 실제 실행 흐름으로 만드는 것이다.
3. LangGraph는 Workflow를 State, Node, Edge로 표현하는 구조이다.
4. MCP는 Agent와 외부 시스템을 표준 방식으로 연결하는 계층이다.
5. Enterprise Agent는 실행 능력보다 통제 능력이 더 중요하다.
```

한 문장으로 최종 정리하면 다음과 같다.

> **Part2의 핵심은 Agent가 복잡한 업무를 계획하고, Workflow로 제어하며, MCP를 통해 외부 시스템을 표준화된 도구로 사용하는 구조를 이해하는 것이다.**

---

## 55. 추천 실습 패키지 목록

Part2 전체에 대응하는 실습 패키지는 다음 네 개로 나누는 것을 추천한다.

```text
labs/agent_planning
- Step3-5 Planning Agent와 Workflow 실습

labs/langgraph_agent
- Step3-6 LangGraph 기반 Workflow Agent 실습

labs/mcp_architecture
- Step3-7 MCP 아키텍처 이해 자료

labs/mcp_integration
- Step3-8 MCP 기반 외부 시스템 연동 실습
```

전체 구조는 다음과 같다.

```text
labs
├── agent_planning
├── langgraph_agent
├── mcp_architecture
└── mcp_integration
```

---

## 56. 다음 단계 예고

다음 문서는 다음과 같다.

```text
Step3-5. Planning Agent와 Workflow
docs/study/step3/step3_5_planning_and_workflow_agent_guide.md
```

다음 문서에서는 Part2의 첫 번째 단계로, Planning Agent를 실제 코드와 함께 학습한다.

다음 단계에서 다룰 내용은 다음과 같다.

```text
1. Planning Agent 개념
2. Task Decomposition
3. 순차 Workflow
4. 조건 분기 Workflow
5. Plan → Execute → Review 구조
6. 실습 디렉터리 생성
7. Python 기반 Planning Agent 구현
8. 실습 데이터 구성
```

---

## 57. 참고 자료

아래 자료는 Part2 내용을 이해하기 위한 참고 자료이다.

```text
LangGraph Graph API
https://docs.langchain.com/oss/python/langgraph/graph-api

LangGraph Overview
https://docs.langchain.com/oss/python/langgraph/overview

LangGraph Persistence
https://docs.langchain.com/oss/python/langgraph/persistence

LangChain Human-in-the-loop
https://docs.langchain.com/oss/python/langchain/human-in-the-loop

Model Context Protocol 공식 문서
https://modelcontextprotocol.io/docs/getting-started/intro

Model Context Protocol Specification
https://modelcontextprotocol.io/specification/2025-06-18

Anthropic - Introducing the Model Context Protocol
https://www.anthropic.com/news/model-context-protocol
```

---
