# Step3-5. Planning Agent와 Workflow 가이드

> AI DATA Platform 연구 프로젝트  
> Step3. AI Agent  
> Part2. AI Agent 심화  
> 문서 경로: `docs/study/step3/step3_5_planning_and_workflow_agent_guide.md`  
> 작성일: 2026-06-30

---

## 1. 문서 목적

이 문서는 `Step3-3. 첫 번째 AI Agent 구현`과 `Step3-4. Agent Memory와 상태 관리`에서 학습한 내용을 바탕으로, **Planning Agent**와 **Workflow Agent**의 기본 개념을 이해하기 위한 가이드 문서이다.

앞 단계에서는 Agent가 다음과 같은 방식으로 동작하는 것을 학습했다.

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

이 구조는 단순한 작업에는 충분하다.

예를 들어 다음과 같은 요청은 하나의 도구로 처리할 수 있다.

```text
"12500 * 17 계산해줘"
"Agent 문서를 검색해줘"
"sample_docs/agent_sample.md 파일을 읽어줘"
```

하지만 실제 업무 요청은 대부분 하나의 도구 호출로 끝나지 않는다.

예를 들어 다음과 같은 요청을 생각해보자.

```text
"AI 플랫폼 상태를 점검하고, 문제가 있으면 원인을 정리해서 보고서 초안으로 만들어줘."
```

이 요청을 처리하려면 Agent는 다음을 수행해야 한다.

```text
1. 점검 대상 식별
2. Docker 상태 확인
3. Ollama 상태 확인
4. Open WebUI 상태 확인
5. ChromaDB 또는 RAG 데이터 상태 확인
6. 문제 여부 판단
7. 원인 정리
8. 보고서 초안 작성
```

즉, 복잡한 요청은 먼저 **작업을 나누고**, **순서를 정하고**, **각 작업을 실행하고**, **결과를 종합**해야 한다.

이번 문서에서는 이 구조를 **Planning Agent**와 **Workflow** 관점에서 학습한다.

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
│   ├─ Step3-5. Planning Agent와 Workflow   ← 현재 문서
│   ├─ Step3-6. LangGraph 기반 Workflow Agent
│   ├─ Step3-7. MCP 아키텍처 이해
│   └─ Step3-8. MCP 기반 외부 시스템 연동
│
└─ Part3. Enterprise AI Agent
    ├─ Step3-9. Multi Agent 협업
    └─ Step3-10. Enterprise AI Agent Platform
```

Step3-5는 Part1에서 만든 단일 Agent 구조를 **업무 흐름 기반 Agent**로 확장하는 첫 단계이다.

```text
Step3-3:
하나의 요청을 하나의 도구로 처리하는 Agent 구조 이해

Step3-4:
대화 이력과 작업 상태를 저장하는 Memory 구조 이해

Step3-5:
복잡한 요청을 여러 단계로 나누고 실행하는 Planning / Workflow 구조 이해

Step3-6:
LangGraph를 사용하여 Workflow를 코드로 제어
```

따라서 이번 문서는 Step3-6의 LangGraph 학습을 위한 사전 준비 단계이다.

---

## 3. 학습 목표

이 문서를 마치면 다음 내용을 설명할 수 있어야 한다.

```text
1. Planning Agent가 왜 필요한지 설명할 수 있다.
2. Task Decomposition이 무엇인지 설명할 수 있다.
3. Plan, Task, Step, Workflow의 차이를 설명할 수 있다.
4. Planner와 Executor의 역할을 구분할 수 있다.
5. 순차 Workflow와 조건부 Workflow를 설명할 수 있다.
6. Planning Agent 실행 흐름을 설계할 수 있다.
7. ReAct 기반 Agent와 Planning Agent의 차이를 설명할 수 있다.
8. Enterprise 업무 자동화에서 Workflow 통제가 왜 중요한지 설명할 수 있다.
9. Step3-6에서 LangGraph가 왜 필요한지 이해할 수 있다.
```

---

## 4. 왜 Planning Agent가 필요한가?

기본 Agent는 사용자의 요청을 보고 바로 도구를 선택한다.

```text
사용자:
"Agent 검색해줘"

Agent:
검색 도구를 사용해야겠다.

Tool Call:
search(query="Agent")

Observation:
검색 결과

Final Answer:
검색 결과 정리
```

이 구조는 단순하고 이해하기 쉽다.

하지만 다음 요청은 다르다.

```text
"프로젝트 문서를 검토해서 누락된 내용을 찾고, 보완할 목차를 추천해줘."
```

이 요청은 바로 답변하기 어렵다.

Agent는 먼저 다음과 같은 판단을 해야 한다.

```text
1. 어떤 프로젝트 문서를 볼 것인가?
2. 문서 목록을 먼저 확인해야 하는가?
3. 각 문서를 읽어야 하는가?
4. 목차 구조를 추출해야 하는가?
5. 누락 여부를 어떤 기준으로 판단할 것인가?
6. 보완 목차를 어떤 형식으로 제안할 것인가?
```

즉, 복잡한 요청은 다음 구조가 필요하다.

```text
큰 목표
   ↓
작업 분해
   ↓
실행 순서 결정
   ↓
각 작업 실행
   ↓
중간 결과 저장
   ↓
최종 결과 통합
```

이 역할을 수행하는 Agent가 Planning Agent이다.

---

## 5. Planning Agent란 무엇인가?

Planning Agent는 사용자의 목표를 달성하기 위해 필요한 작업을 먼저 계획하고, 그 계획에 따라 실행하는 Agent이다.

간단히 표현하면 다음과 같다.

```text
Planning Agent = Planner + Executor + Memory + Tools
```

각 구성 요소의 역할은 다음과 같다.

```text
Planner:
- 사용자의 목표를 작은 작업으로 나눈다.
- 작업 순서를 정한다.
- 어떤 도구가 필요한지 판단한다.

Executor:
- Planner가 만든 작업을 실제로 실행한다.
- Tool Call을 수행한다.
- 실행 결과를 반환한다.

Memory:
- 계획, 중간 결과, 실행 상태를 저장한다.
- 실패한 작업이나 완료된 작업을 기록한다.

Tools:
- 검색, 파일 읽기, 계산, DB 조회, API 호출 등 실제 작업을 수행한다.
```

Planning Agent의 기본 흐름은 다음과 같다.

```text
사용자 목표
   ↓
계획 수립
   ↓
작업 목록 생성
   ↓
작업 실행
   ↓
결과 확인
   ↓
필요 시 계획 수정
   ↓
최종 답변
```

---

## 6. Planning과 ReAct의 차이

Step3-2에서 ReAct를 학습했다.

ReAct는 다음 흐름을 가진다.

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

ReAct는 매 순간 다음 행동을 판단하는 구조에 가깝다.

반면 Planning Agent는 먼저 전체 계획을 세우는 구조에 가깝다.

```text
Plan
   ↓
Step 1
   ↓
Step 2
   ↓
Step 3
   ↓
Final Answer
```

둘의 차이를 비교하면 다음과 같다.

| 구분 | ReAct Agent | Planning Agent |
|---|---|---|
| 중심 개념 | 생각과 행동의 반복 | 계획 수립과 실행 |
| 실행 방식 | 매 단계에서 다음 행동 판단 | 전체 또는 일부 계획을 먼저 생성 |
| 적합한 작업 | 단순 질의, 도구 사용, 검색 | 보고서 작성, 점검, 분석, 업무 자동화 |
| 장점 | 유연하고 단순하다 | 복잡한 작업을 체계적으로 처리한다 |
| 단점 | 긴 작업에서는 흐름이 흔들릴 수 있다 | 계획이 잘못되면 전체 실행이 영향을 받는다 |

실제 Agent 시스템에서는 ReAct와 Planning이 함께 사용될 수 있다.

```text
Planning:
전체 작업 계획을 세운다.

ReAct:
각 작업을 실행하면서 필요한 도구를 선택하고 결과를 확인한다.
```

즉, Planning은 큰 흐름을 잡고, ReAct는 각 단계의 실행 판단을 담당할 수 있다.

---

## 7. Task Decomposition이란?

Task Decomposition은 큰 목표를 작은 작업으로 나누는 것이다.

예를 들어 다음 요청이 있다고 하자.

```text
"Step2 RAG 문서를 검토해서 팀원 교육용 요약 자료를 만들어줘."
```

이 요청은 다음과 같이 분해할 수 있다.

```text
1. Step2 RAG 문서 목록 확인
2. 주요 문서 읽기
3. 핵심 개념 추출
4. 실습 흐름 정리
5. 팀원이 어려워할 부분 정리
6. 교육용 요약 자료 작성
7. 최종 검토
```

Task Decomposition의 목적은 다음과 같다.

```text
1. 복잡한 작업을 이해하기 쉽게 만든다.
2. 실행 순서를 명확히 한다.
3. 중간 결과를 관리할 수 있다.
4. 실패한 작업만 다시 실행할 수 있다.
5. 사람이 검토하기 쉬워진다.
```

---

## 8. Plan, Task, Step, Workflow의 차이

Planning Agent를 이해하려면 용어를 구분해야 한다.

| 용어 | 의미 |
|---|---|
| Goal | 사용자가 달성하고 싶은 최종 목표 |
| Plan | 목표를 달성하기 위한 전체 계획 |
| Task | 계획을 구성하는 개별 작업 |
| Step | Task를 실행하는 구체적인 단계 |
| Workflow | Task 또는 Step의 실행 흐름 |
| State | 현재까지의 작업 상태와 중간 결과 |

예를 들어 다음 요청이 있다고 하자.

```text
"AI 플랫폼 상태 점검 보고서를 만들어줘."
```

이를 구조화하면 다음과 같다.

```text
Goal:
AI 플랫폼 상태 점검 보고서 작성

Plan:
1. 점검 대상 식별
2. 상태 정보 수집
3. 이상 여부 판단
4. 보고서 작성

Task:
- Docker 상태 확인
- Ollama 상태 확인
- Open WebUI 상태 확인
- ChromaDB 상태 확인

Step:
- docker ps 실행
- ollama list 실행
- HTTP 응답 확인
- 경로 존재 여부 확인

Workflow:
점검 대상 식별 → 상태 확인 → 결과 분석 → 보고서 작성

State:
현재까지 확인된 상태 정보와 오류 목록
```

---

## 9. Workflow란 무엇인가?

Workflow는 작업이 어떤 순서와 조건으로 실행되는지를 정의한 흐름이다.

단순한 Workflow는 다음과 같다.

```text
START
  ↓
문서 검색
  ↓
문서 요약
  ↓
답변 생성
  ↓
END
```

업무 시스템에서 Workflow는 매우 중요하다.

왜냐하면 실제 업무는 대부분 절차를 가지고 있기 때문이다.

```text
제안서 작성:
자료 수집 → 요구사항 분석 → 목차 작성 → 본문 작성 → 검토 → 제출

장애 보고:
장애 감지 → 로그 확인 → 영향도 분석 → 조치 내용 정리 → 보고서 작성

문서 검토:
문서 읽기 → 기준 확인 → 누락 항목 확인 → 개선안 작성 → 최종 검토
```

Agent가 Workflow를 이해하면 단순 답변이 아니라 실제 업무 흐름을 수행할 수 있다.

---

## 10. Workflow의 기본 유형

---

### 10.1 Sequential Workflow

Sequential Workflow는 작업을 순서대로 실행하는 방식이다.

```text
Task A
  ↓
Task B
  ↓
Task C
  ↓
Task D
```

예시는 다음과 같다.

```text
문서 읽기
  ↓
핵심 내용 추출
  ↓
요약 작성
  ↓
최종 답변 생성
```

가장 단순하고 이해하기 쉬운 Workflow이다.

처음 Planning Agent를 구현할 때는 Sequential Workflow부터 시작하는 것이 좋다.

---

### 10.2 Conditional Workflow

Conditional Workflow는 조건에 따라 다음 작업이 달라지는 방식이다.

```text
상태 확인
   ↓
문제 있음?
   ├─ 예 → 원인 분석
   └─ 아니오 → 정상 보고
```

예시는 다음과 같다.

```text
Ollama 상태 확인
   ↓
실행 중인가?
   ├─ 예 → 모델 목록 확인
   └─ 아니오 → 실행 가이드 출력
```

조건부 Workflow는 실제 운영 점검 Agent에서 자주 필요하다.

---

### 10.3 Parallel Workflow

Parallel Workflow는 여러 작업을 동시에 또는 독립적으로 수행하는 방식이다.

```text
        START
          ↓
   ┌──────┼──────┐
   ↓      ↓      ↓
Docker  Ollama  ChromaDB
   ↓      ↓      ↓
   └──────┼──────┘
          ↓
       결과 종합
```

예시는 다음과 같다.

```text
1. Docker 상태 확인
2. Ollama 상태 확인
3. Open WebUI 상태 확인
4. ChromaDB 상태 확인
5. 결과 종합
```

여러 점검 작업이 서로 의존하지 않는 경우 병렬 구조로 설계할 수 있다.

단, 처음 구현할 때는 병렬 실행을 실제로 구현하지 않고, 논리적으로만 병렬 작업으로 분리해도 충분하다.

---

### 10.4 Human-in-the-Loop Workflow

Human-in-the-Loop은 중간에 사람의 확인이나 승인을 받는 Workflow이다.

```text
Agent 초안 작성
   ↓
사용자 검토
   ↓
승인 여부
   ├─ 승인 → 최종 생성
   └─ 수정 요청 → 다시 작성
```

Enterprise 환경에서는 매우 중요하다.

특히 다음 작업은 바로 실행하면 위험하다.

```text
1. 메일 발송
2. DB 수정
3. 파일 삭제
4. 배포 실행
5. 티켓 등록
6. 외부 시스템 전송
```

따라서 쓰기 작업은 다음 구조를 권장한다.

```text
계획 수립
  ↓
Preview 생성
  ↓
사용자 승인
  ↓
실제 실행
  ↓
실행 로그 기록
```

---

## 11. Planner와 Executor 구조

Planning Agent는 보통 Planner와 Executor를 분리한다.

```text
사용자 요청
   ↓
Planner
   ↓
Task List
   ↓
Executor
   ↓
Tool Result
   ↓
Final Answer
```

Planner의 역할은 다음과 같다.

```text
1. 사용자 요청 분석
2. 목표 정의
3. 필요한 작업 분해
4. 작업 순서 결정
5. 필요한 도구 후보 지정
```

Executor의 역할은 다음과 같다.

```text
1. Task를 하나씩 실행
2. 필요한 Tool 호출
3. 실행 결과 저장
4. 실패 여부 확인
5. 다음 Task로 이동
```

이 구조를 분리하면 장점이 있다.

```text
1. 계획과 실행을 따로 검토할 수 있다.
2. 잘못된 계획을 실행 전에 수정할 수 있다.
3. 실패한 Task만 재실행할 수 있다.
4. 실행 로그를 체계적으로 남길 수 있다.
5. 나중에 LangGraph로 확장하기 쉽다.
```

---

## 12. Planning Agent의 실행 흐름

Planning Agent의 기본 실행 흐름은 다음과 같다.

```text
1. 사용자 요청 입력
2. Planner가 Plan 생성
3. Plan을 Task 목록으로 변환
4. Executor가 Task를 순서대로 실행
5. 각 Task 결과를 State에 저장
6. 모든 Task 완료 여부 확인
7. 결과를 종합하여 Final Answer 생성
```

이를 의사코드로 표현하면 다음과 같다.

```python
user_goal = input("요청을 입력하세요: ")

plan = planner.create_plan(user_goal)

state = {
    "goal": user_goal,
    "plan": plan,
    "task_results": []
}

for task in plan["tasks"]:
    result = executor.run(task)
    state["task_results"].append(result)

final_answer = summarize(state)
print(final_answer)
```

이 구조는 Step3-6에서 LangGraph의 StateGraph 구조로 확장된다.

---

## 13. Plan 데이터 구조 설계

Planning Agent를 구현하려면 Plan을 데이터로 표현해야 한다.

가장 단순한 Plan 구조는 다음과 같다.

```json
{
  "goal": "AI 플랫폼 상태를 점검한다.",
  "tasks": [
    {
      "id": "task_1",
      "name": "Docker 상태 확인",
      "tool": "check_docker_status",
      "status": "pending"
    },
    {
      "id": "task_2",
      "name": "Ollama 상태 확인",
      "tool": "check_ollama_status",
      "status": "pending"
    },
    {
      "id": "task_3",
      "name": "결과 요약",
      "tool": "summarizer",
      "status": "pending"
    }
  ]
}
```

처음에는 이 정도로 충분하다.

이후에는 다음 정보를 추가할 수 있다.

```text
1. Task 설명
2. 입력 파라미터
3. 예상 결과
4. 의존 Task
5. 실패 시 처리 방식
6. 승인 필요 여부
7. 실행 시간
8. 실행 결과
```

확장된 구조는 다음과 같다.

```json
{
  "id": "task_1",
  "name": "문서 검색",
  "description": "Step2 RAG 관련 문서를 검색한다.",
  "tool": "search_documents",
  "arguments": {
    "query": "Step2 RAG ChromaDB"
  },
  "depends_on": [],
  "status": "pending",
  "approval_required": false,
  "result": null
}
```

---

## 14. Task 상태 관리

Workflow에서 각 Task는 상태를 가진다.

대표적인 상태는 다음과 같다.

| 상태 | 의미 |
|---|---|
| pending | 아직 실행 전 |
| running | 실행 중 |
| success | 성공 |
| failed | 실패 |
| skipped | 조건에 의해 건너뜀 |
| waiting_approval | 사용자 승인 대기 |

Task 상태를 관리하면 다음을 할 수 있다.

```text
1. 어떤 작업이 완료되었는지 확인
2. 어디서 실패했는지 확인
3. 실패한 작업만 다시 실행
4. 승인 대기 작업을 분리
5. 실행 이력을 로그로 남김
```

단순 Agent와 Workflow Agent의 가장 큰 차이 중 하나가 바로 상태 관리이다.

---

## 15. Workflow State란?

State는 현재 Workflow의 전체 상태이다.

예를 들어 상태 점검 Agent의 State는 다음과 같이 표현할 수 있다.

```json
{
  "goal": "AI 플랫폼 상태 점검",
  "current_task_id": "task_2",
  "results": {
    "docker": "running",
    "ollama": "not_running",
    "open_webui": "running"
  },
  "errors": [
    "Ollama 서버가 실행 중이 아닙니다."
  ],
  "final_report": null
}
```

State는 Agent가 다음 행동을 결정하는 기준이 된다.

```text
State를 보고 다음 Task를 실행한다.
State를 보고 조건 분기를 수행한다.
State를 보고 최종 답변을 만든다.
```

Step3-6에서 LangGraph를 학습할 때 가장 중요한 개념이 바로 State이다.

---

## 16. Planning Agent 예시 1: 문서 요약 Workflow

사용자 요청:

```text
"Agent 관련 문서를 찾아서 교육용 요약을 만들어줘."
```

Planning 결과:

```text
1. Agent 관련 문서 검색
2. 검색 결과에서 주요 문서 선택
3. 문서 내용 요약
4. 교육용 핵심 포인트 정리
5. 최종 답변 작성
```

Workflow:

```text
START
  ↓
search_documents
  ↓
read_text_file
  ↓
summarize
  ↓
format_answer
  ↓
END
```

이 예시는 문서 기반 RAG와 Agent Workflow가 결합되는 형태이다.

---

## 17. Planning Agent 예시 2: 운영 점검 Workflow

사용자 요청:

```text
"AI 플랫폼 상태를 점검해줘."
```

Planning 결과:

```text
1. Docker 상태 확인
2. Ollama 상태 확인
3. Open WebUI 상태 확인
4. ChromaDB 상태 확인
5. 이상 여부 판단
6. 점검 결과 보고
```

Workflow:

```text
START
  ↓
check_docker_status
  ↓
check_ollama_status
  ↓
check_open_webui_status
  ↓
check_chroma_status
  ↓
analyze_health
  ↓
generate_report
  ↓
END
```

조건부 Workflow로 표현하면 다음과 같다.

```text
check_ollama_status
   ↓
Ollama 실행 중?
   ├─ 예 → 모델 목록 확인
   └─ 아니오 → 실행 가이드 생성
```

---

## 18. Planning Agent 예시 3: 제안서 작성 Workflow

사용자 요청:

```text
"KB증권 자산성장 프로젝트 제안서 작성 방향을 정리해줘."
```

Planning 결과:

```text
1. RFP 또는 요구사항 문서 확인
2. 자산성장 관련 키워드 추출
3. 경쟁사 벤치마킹 관점 정리
4. 웹표준/웹접근성 항목 정리
5. 보안 요구사항 대응 항목 정리
6. 작성 목차 추천
7. 초안 작성
8. 검토 포인트 정리
```

이 예시는 실제 제안 업무에서 Planning Agent가 어떻게 활용될 수 있는지 보여준다.

Enterprise 업무에서는 계획 자체가 매우 중요하다.

왜냐하면 사용자가 원하는 것은 단순 답변이 아니라 다음과 같은 결과물이기 때문이다.

```text
1. 어떤 순서로 작업할지
2. 누가 어떤 자료를 봐야 하는지
3. 어떤 산출물이 나와야 하는지
4. 어떤 검토 포인트가 있는지
5. 최종 문서가 어떤 구조여야 하는지
```

---

## 19. Planning Agent 구현 방식

Planning Agent를 구현하는 방식은 크게 세 가지가 있다.

```text
1. 규칙 기반 Planning
2. LLM 기반 Planning
3. Hybrid Planning
```

---

### 19.1 규칙 기반 Planning

규칙 기반 Planning은 미리 정한 규칙에 따라 계획을 만든다.

예를 들어 다음과 같다.

```text
입력에 "점검"이 있으면:
1. Docker 상태 확인
2. Ollama 상태 확인
3. Open WebUI 상태 확인
4. 결과 요약
```

장점은 다음과 같다.

```text
1. 예측 가능하다.
2. 디버깅이 쉽다.
3. 보안 통제가 쉽다.
4. 처음 실습하기 좋다.
```

단점은 다음과 같다.

```text
1. 유연성이 낮다.
2. 새로운 요청에 약하다.
3. 규칙이 많아지면 관리가 어렵다.
```

Step3-5 실습에서는 먼저 규칙 기반 Planning을 권장한다.

---

### 19.2 LLM 기반 Planning

LLM 기반 Planning은 LLM이 사용자의 요청을 분석해서 계획을 생성한다.

예를 들어 LLM에게 다음과 같이 요청할 수 있다.

```text
사용자 요청을 처리하기 위한 작업 계획을 JSON 형식으로 작성하라.
각 작업에는 id, name, tool, arguments를 포함하라.
```

LLM 출력 예시는 다음과 같다.

```json
{
  "goal": "Agent 문서를 교육용으로 요약한다.",
  "tasks": [
    {
      "id": "task_1",
      "name": "Agent 문서 검색",
      "tool": "search_documents",
      "arguments": {
        "query": "AI Agent"
      }
    },
    {
      "id": "task_2",
      "name": "요약 작성",
      "tool": "summarize",
      "arguments": {}
    }
  ]
}
```

장점은 다음과 같다.

```text
1. 유연하다.
2. 다양한 요청에 대응할 수 있다.
3. 사람이 직접 규칙을 모두 만들 필요가 없다.
```

단점은 다음과 같다.

```text
1. 잘못된 계획을 만들 수 있다.
2. 허용되지 않은 도구를 제안할 수 있다.
3. JSON 형식이 깨질 수 있다.
4. 보안 검증이 반드시 필요하다.
```

---

### 19.3 Hybrid Planning

Hybrid Planning은 규칙 기반과 LLM 기반을 함께 사용하는 방식이다.

```text
LLM:
계획 초안을 만든다.

Application:
계획을 검증한다.
허용된 도구인지 확인한다.
위험한 작업은 승인 대상으로 분리한다.

Executor:
검증된 계획만 실행한다.
```

Enterprise 환경에서는 Hybrid 방식을 권장한다.

```text
LLM은 계획을 제안한다.
Application은 계획을 검증한다.
사용자는 중요한 작업을 승인한다.
Executor는 승인된 작업만 실행한다.
```

---

## 20. Planning Agent 보안 원칙

Planning Agent는 단일 Tool Calling Agent보다 더 강력하다.

따라서 더 많은 통제가 필요하다.

중요한 보안 원칙은 다음과 같다.

```text
1. Plan에 포함된 도구가 허용된 도구인지 검증한다.
2. 쓰기 작업은 실행 전 사용자 승인을 받는다.
3. 파일 경로는 허용된 디렉터리 안으로 제한한다.
4. DB 수정, 메일 발송, 배포 실행은 별도 권한을 요구한다.
5. Plan과 실행 결과를 모두 로그로 남긴다.
6. 실패한 작업은 안전하게 중단한다.
7. 민감정보는 로그에 그대로 저장하지 않는다.
8. Agent가 만든 계획을 사람이 검토할 수 있어야 한다.
```

Planning Agent에서 가장 중요한 원칙은 다음이다.

> **LLM이 만든 계획을 그대로 믿고 실행하면 안 된다.**

---

## 21. Planning Agent 로그 설계

Planning Agent는 실행 과정이 길기 때문에 로그가 중요하다.

로그에는 다음 정보가 포함되는 것이 좋다.

```text
1. 사용자 요청
2. 생성된 Plan
3. 각 Task의 시작 시간
4. 각 Task의 종료 시간
5. 실행한 Tool
6. 입력 Arguments
7. 실행 결과 상태
8. 오류 메시지
9. 승인 여부
10. 최종 답변
```

예시는 다음과 같다.

```json
{
  "session_id": "session-20260630-001",
  "goal": "AI 플랫폼 상태 점검",
  "plan_id": "plan-001",
  "tasks": [
    {
      "task_id": "task_1",
      "name": "Docker 상태 확인",
      "tool": "check_docker_status",
      "status": "success",
      "elapsed_ms": 120
    },
    {
      "task_id": "task_2",
      "name": "Ollama 상태 확인",
      "tool": "check_ollama_status",
      "status": "failed",
      "error": "Ollama 서버 응답 없음"
    }
  ]
}
```

이 로그는 다음 목적에 사용된다.

```text
1. 장애 분석
2. 보안 감사
3. 실행 흐름 재현
4. Agent 품질 개선
5. 비용 분석
6. 실패 지점 파악
```

---

## 22. Workflow 실패 처리

실제 Workflow에서는 실패가 자주 발생한다.

예를 들어 다음 문제가 생길 수 있다.

```text
1. 파일이 존재하지 않는다.
2. 검색 결과가 없다.
3. API 응답이 실패한다.
4. DB 연결이 되지 않는다.
5. 권한이 없다.
6. LLM 응답 형식이 깨진다.
```

실패 처리 방식은 다음과 같이 설계할 수 있다.

```text
Fail Fast:
- 오류가 발생하면 즉시 중단한다.
- 위험한 작업에 적합하다.

Retry:
- 일정 횟수 다시 시도한다.
- 네트워크 오류나 일시적 API 오류에 적합하다.

Skip:
- 실패한 작업을 건너뛰고 다음 작업으로 진행한다.
- 선택 작업에 적합하다.

Fallback:
- 대체 도구나 대체 경로를 사용한다.
- 검색 실패 시 다른 키워드로 재검색하는 방식이다.

Human Review:
- 사람이 판단하도록 중단한다.
- 중요한 업무나 위험한 작업에 적합하다.
```

처음 실습에서는 Fail Fast 방식으로 시작해도 충분하다.

---

## 23. 실습 목표

이번 Step3-5 실습에서는 완성형 Planning Agent를 만드는 것이 아니라, Planning 구조를 이해하기 위한 최소 예제를 만든다.

실습 목표는 다음과 같다.

```text
1. 사용자 요청을 기반으로 Plan을 만든다.
2. Plan을 Task 목록으로 표현한다.
3. Task를 순서대로 실행한다.
4. 실행 결과를 State에 저장한다.
5. 최종 결과를 요약한다.
```

실습에서는 실제 LLM을 연결하지 않고 규칙 기반 Planner를 사용한다.

이유는 다음과 같다.

```text
1. Planning 구조를 먼저 이해하기 위해서이다.
2. LLM 응답 오류와 Agent 구조 오류를 분리하기 위해서이다.
3. 디버깅이 쉽다.
4. Step3-6에서 LangGraph로 확장하기 쉽다.
```

---

## 24. 권장 실습 디렉터리 구조

이번 실습은 기존 `labs/agent` 아래에 `workflow` 디렉터리를 추가하는 방식으로 진행한다.

```text
labs
└── agent
    ├── workflow
    │   ├── README.md
    │   ├── 01_simple_planner.py
    │   ├── 02_task_executor.py
    │   ├── 03_workflow_demo.py
    │   └── sample_tasks.json
    │
    ├── tools
    │   ├── calculator.py
    │   ├── search.py
    │   └── file_reader.py
    │
    └── common
        ├── tool_registry.py
        └── tool_executor.py
```

이번 문서에서는 구조를 설명하고, 실제 실습 파일은 별도 실습 패키지로 제공하는 것을 권장한다.

---

## 25. 실습 파일 1: sample_tasks.json

파일 경로:

```text
labs/agent/workflow/sample_tasks.json
```

예시 내용:

```json
{
  "goal": "AI Agent 문서를 검색하고 요약한다.",
  "tasks": [
    {
      "id": "task_1",
      "name": "Agent 문서 검색",
      "tool": "search",
      "arguments": {
        "query": "Agent"
      },
      "status": "pending"
    },
    {
      "id": "task_2",
      "name": "샘플 문서 읽기",
      "tool": "file_reader",
      "arguments": {
        "relative_path": "sample_docs/agent_sample.md"
      },
      "status": "pending"
    }
  ]
}
```

이 파일은 Plan을 JSON 데이터로 표현하는 예제이다.

---

## 26. 실습 파일 2: 01_simple_planner.py

이 파일은 사용자 요청을 보고 간단한 Plan을 생성한다.

예시 흐름은 다음과 같다.

```text
사용자 요청에 "점검" 포함
→ 상태 점검 Plan 생성

사용자 요청에 "문서" 또는 "검색" 포함
→ 문서 검색 Plan 생성

사용자 요청에 "계산" 포함
→ 계산 Plan 생성
```

의사코드는 다음과 같다.

```python
def create_plan(user_input: str) -> dict:
    if "점검" in user_input:
        return health_check_plan()

    if "문서" in user_input or "검색" in user_input:
        return document_search_plan()

    if "계산" in user_input:
        return calculation_plan()

    return default_plan()
```

처음에는 이처럼 규칙 기반으로 계획을 생성한다.

---

## 27. 실습 파일 3: 02_task_executor.py

이 파일은 Plan에 포함된 Task를 실행한다.

의사코드는 다음과 같다.

```python
def execute_task(task: dict) -> dict:
    tool_name = task["tool"]
    arguments = task.get("arguments", {})

    result = execute_tool(tool_name, arguments)

    return {
        "task_id": task["id"],
        "status": "success",
        "result": result
    }
```

Task Executor는 기존 Step3-3에서 만든 `execute_tool()` 구조를 재사용할 수 있다.

이 점이 중요하다.

```text
Step3-3:
Tool Executor 구현

Step3-5:
Tool Executor를 Task Executor에서 재사용
```

---

## 28. 실습 파일 4: 03_workflow_demo.py

이 파일은 전체 Workflow를 실행한다.

흐름은 다음과 같다.

```text
1. 사용자 요청 입력
2. create_plan() 호출
3. Plan 출력
4. Task 목록 순회
5. 각 Task 실행
6. State에 결과 저장
7. 최종 결과 출력
```

의사코드는 다음과 같다.

```python
def run_workflow(user_input: str) -> dict:
    plan = create_plan(user_input)

    state = {
        "goal": plan["goal"],
        "tasks": plan["tasks"],
        "results": []
    }

    for task in plan["tasks"]:
        task_result = execute_task(task)
        state["results"].append(task_result)

    return state
```

---

## 29. 실행 예시

사용자 입력:

```text
Agent 문서 검색하고 요약해줘
```

생성된 Plan:

```json
{
  "goal": "Agent 관련 문서를 검색하고 내용을 확인한다.",
  "tasks": [
    {
      "id": "task_1",
      "name": "Agent 문서 검색",
      "tool": "search",
      "arguments": {
        "query": "Agent"
      },
      "status": "pending"
    },
    {
      "id": "task_2",
      "name": "샘플 Agent 문서 읽기",
      "tool": "file_reader",
      "arguments": {
        "relative_path": "sample_docs/agent_sample.md"
      },
      "status": "pending"
    }
  ]
}
```

실행 결과:

```text
task_1 성공
- Agent 관련 문서 검색 결과 확인

task_2 성공
- agent_sample.md 파일 내용 읽기 완료

최종 답변:
Agent 관련 문서를 검색하고 샘플 문서를 읽었습니다...
```

---

## 30. Step3-3 코드와의 연결

Step3-5는 Step3-3의 코드를 버리는 것이 아니라 확장한다.

Step3-3 구조:

```text
사용자 입력
   ↓
select_tool
   ↓
execute_tool
   ↓
Final Answer
```

Step3-5 구조:

```text
사용자 입력
   ↓
create_plan
   ↓
Task List
   ↓
execute_task
   ↓
execute_tool
   ↓
State 저장
   ↓
Final Answer
```

즉, Step3-5에서 새로 추가되는 것은 다음이다.

```text
1. Plan
2. Task
3. Workflow
4. State
```

기존 Tool Registry와 Tool Executor는 그대로 재사용할 수 있다.

---

## 31. Step3-6 LangGraph로 이어지는 이유

Step3-5에서는 Workflow를 Python for문과 if문으로 단순하게 표현한다.

```python
for task in tasks:
    execute_task(task)
```

하지만 Workflow가 복잡해지면 문제가 생긴다.

```text
1. 조건 분기가 많아진다.
2. 중간 상태 관리가 어려워진다.
3. 실패 처리 로직이 복잡해진다.
4. 재시작과 재실행이 어렵다.
5. Human-in-the-Loop을 넣기 어렵다.
6. 그래프 형태의 업무 흐름을 표현하기 어렵다.
```

이 문제를 해결하기 위해 Step3-6에서 LangGraph를 학습한다.

LangGraph는 Workflow를 다음 개념으로 표현한다.

```text
State:
현재 작업 상태

Node:
실행 단위

Edge:
다음 실행 흐름

Conditional Edge:
조건에 따른 분기

Graph:
전체 Workflow 구조
```

즉, Step3-5에서 개념적으로 배운 Workflow가 Step3-6에서는 LangGraph 코드로 구현된다.

---

## 32. Enterprise 관점에서 Planning Agent 보기

Enterprise 환경에서 Planning Agent는 단순한 자동화 도구가 아니다.

업무 절차를 AI가 이해하고 실행할 수 있도록 만드는 구조이다.

예시는 다음과 같다.

```text
제안서 작성 Agent:
요구사항 분석 → 경쟁사 조사 → 목차 작성 → 초안 작성 → 품질 검토

운영 점검 Agent:
시스템 상태 확인 → 오류 탐지 → 원인 분석 → 조치 가이드 작성

문서 관리 Agent:
문서 목록 확인 → 변경사항 요약 → 누락 항목 검토 → 개선안 작성

RAG 품질 점검 Agent:
문서 수집 → Chunk 품질 확인 → 검색 테스트 → 답변 품질 평가
```

이런 업무는 단순 Tool Calling으로는 어렵고, Planning과 Workflow가 필요하다.

---

## 33. Planning Agent 도입 시 주의사항

Planning Agent를 도입할 때는 다음을 주의해야 한다.

```text
1. 처음부터 너무 복잡한 Planner를 만들지 않는다.
2. 읽기 전용 Workflow부터 시작한다.
3. 쓰기 작업은 반드시 승인 단계를 둔다.
4. Plan을 사람이 볼 수 있는 형태로 출력한다.
5. 실패한 Task를 확인할 수 있게 한다.
6. Plan과 실행 결과를 로그로 남긴다.
7. 허용된 Tool만 실행되도록 검증한다.
8. Workflow가 길어질수록 State를 명확히 관리한다.
```

처음에는 다음 정도의 Workflow부터 시작하는 것이 좋다.

```text
문서 검색
  ↓
파일 읽기
  ↓
요약
  ↓
답변
```

이 구조가 안정화된 후 운영 점검, 보고서 작성, 외부 시스템 연동으로 확장한다.

---

## 34. 핵심 정리

이번 문서의 핵심은 다음과 같다.

```text
1. Planning Agent는 복잡한 요청을 여러 작업으로 분해한다.
2. Task Decomposition은 큰 목표를 작은 작업으로 나누는 과정이다.
3. Workflow는 Task의 실행 순서와 조건을 정의한다.
4. Planner는 계획을 만들고, Executor는 계획을 실행한다.
5. Workflow에는 순차, 조건부, 병렬, Human-in-the-Loop 구조가 있다.
6. Task는 pending, running, success, failed 같은 상태를 가진다.
7. State는 Workflow 전체의 현재 상태와 중간 결과를 저장한다.
8. Step3-3의 Tool Executor는 Step3-5의 Task Executor에서 재사용된다.
9. Enterprise 환경에서는 Plan 검증, 권한, 승인, 로그가 중요하다.
10. Step3-6에서는 이 Workflow를 LangGraph로 구현한다.
```

한 문장으로 정리하면 다음과 같다.

> **Planning Agent는 복잡한 업무 요청을 계획 가능한 작업 목록으로 분해하고, Workflow에 따라 실행하는 Agent 구조이다.**

---

## 35. 다음 단계 예고

다음 문서는 다음과 같다.

```text
Step3-6. LangGraph 기반 Workflow Agent
docs/study/step3/step3_6_langgraph_workflow_agent_guide.md
```

다음 단계에서는 이번 문서에서 학습한 Planning과 Workflow 개념을 LangGraph로 구현한다.

다음 문서에서 다룰 내용은 다음과 같다.

```text
1. LangGraph가 필요한 이유
2. StateGraph 개념
3. State 정의
4. Node 정의
5. Edge 정의
6. Conditional Edge 정의
7. START와 END
8. Workflow 실행
9. Agent State 관리
10. LangGraph 기반 Workflow Agent 구현
```

---

## 36. 참고: 이번 단계에서 만들 실습 패키지 후보

Step3-5 실습 패키지를 만든다면 다음 파일 구성을 추천한다.

```text
labs/agent/workflow
├── README.md
├── 01_simple_planner.py
├── 02_task_executor.py
├── 03_workflow_demo.py
├── 04_conditional_workflow.py
└── sample_tasks.json
```

각 파일의 역할은 다음과 같다.

| 파일 | 역할 |
|---|---|
| `01_simple_planner.py` | 사용자 요청을 기반으로 Plan 생성 |
| `02_task_executor.py` | Task를 실행하고 결과 반환 |
| `03_workflow_demo.py` | 전체 Workflow 실행 |
| `04_conditional_workflow.py` | 조건부 Workflow 예제 |
| `sample_tasks.json` | Plan 데이터 예제 |

---

## 37. 부록: Planning Agent와 기존 Agent 비교

| 구분 | 기본 Tool Agent | Planning Agent |
|---|---|---|
| 입력 처리 | 요청 즉시 도구 선택 | 먼저 계획 수립 |
| 실행 단위 | Tool Call | Task |
| 상태 관리 | 단순 결과 | Workflow State |
| 복잡한 작업 | 어려움 | 가능 |
| 실패 처리 | 단순 예외 처리 | Task 단위 처리 |
| 로그 | Tool 실행 로그 | Plan + Task + Tool 로그 |
| 확장 방향 | Tool 추가 | Workflow / LangGraph 확장 |

---

## 38. 부록: Planning Agent 설계 체크리스트

Planning Agent를 설계할 때 다음 항목을 확인한다.

```text
1. 사용자의 Goal이 명확한가?
2. Goal을 Task로 분해할 수 있는가?
3. 각 Task에 적절한 Tool이 지정되어 있는가?
4. Task 실행 순서가 명확한가?
5. Task 간 의존 관계가 있는가?
6. 실패 시 중단할 것인가, 재시도할 것인가?
7. 사용자 승인이 필요한 Task가 있는가?
8. 실행 결과를 State에 저장하는가?
9. Plan과 실행 로그를 남기는가?
10. 최종 답변에서 실행 결과를 명확히 요약하는가?
```

---

## 39. 부록: 추천 학습 순서

이번 문서는 다음 순서로 학습하는 것을 추천한다.

```text
1. Planning Agent가 왜 필요한지 이해한다.
2. Task Decomposition 예시를 직접 만들어본다.
3. Sequential Workflow를 그려본다.
4. Conditional Workflow를 그려본다.
5. Plan을 JSON으로 표현해본다.
6. Task 상태값을 정의해본다.
7. Step3-3의 Tool Executor와 연결하는 구조를 이해한다.
8. Step3-6의 LangGraph가 왜 필요한지 이해한다.
```

---

## 40. 마무리

Step3-5는 Agent 학습에서 중요한 전환점이다.

Step3-3까지는 Agent가 도구를 사용할 수 있다는 것을 확인했다.

Step3-4에서는 Agent가 작업 상태를 기억할 수 있다는 것을 확인했다.

Step3-5에서는 Agent가 이제 단순히 도구를 호출하는 수준을 넘어, **업무를 계획하고 순서대로 실행하는 구조**로 확장된다.

이 구조가 안정화되면 이후 다음 단계로 자연스럽게 이어질 수 있다.

```text
Planning Agent
   ↓
LangGraph Workflow Agent
   ↓
MCP 기반 외부 시스템 연동
   ↓
Multi Agent 협업
   ↓
Enterprise AI Agent Platform
```

따라서 Step3-5는 단순한 개념 문서가 아니라, AI DATA Platform의 Agent 구조를 실무형 Workflow로 확장하기 위한 핵심 기반 문서이다.
