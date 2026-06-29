# Step3-1. AI Agent 개요 가이드

> AI DATA Platform 연구 프로젝트  
> Step3. AI Agent  
> Part1. AI Agent 기초  
> 문서 경로: `docs/study/step3/step3_1_ai_agent_overview_guide.md`  
> 작성일: 2026-06-29

---

## 1. 학습 목표

이 문서의 목표는 **AI Agent가 무엇인지**, 그리고 왜 Local LLM과 RAG 다음 단계에서 Agent를 학습해야 하는지 이해하는 것이다.

Step1에서는 Local LLM을 실행했다.  
Step2에서는 RAG를 통해 문서를 검색하고 LLM 답변에 근거를 제공하는 구조를 만들었다.  
Step3에서는 LLM이 단순히 답변만 생성하는 것이 아니라, **목표를 이해하고, 필요한 작업을 판단하고, 도구를 사용하여 실제 업무를 수행하는 구조**를 학습한다.

이 문서를 읽고 나면 다음 질문에 답할 수 있어야 한다.

```text
1. AI Agent란 무엇인가?
2. 일반 Chatbot, RAG, Agent는 무엇이 다른가?
3. LLM만으로는 왜 실제 업무 자동화가 어려운가?
4. Agent는 어떤 구성 요소로 이루어지는가?
5. Agent는 어떤 순서로 동작하는가?
6. Enterprise 환경에서는 Agent를 어떻게 바라봐야 하는가?
7. 앞으로 Step3에서 무엇을 학습하게 되는가?
```

---

## 2. 왜 AI Agent가 필요한가?

LLM은 자연어를 이해하고 답변을 생성하는 데 매우 강력하다.  
하지만 LLM만으로 실제 업무를 처리하기에는 한계가 있다.

예를 들어 사용자가 다음과 같이 요청했다고 하자.

```text
"지난주 장애 내용을 정리해서 보고서 초안을 만들어줘."
```

일반 LLM은 보고서 작성 방법을 설명하거나 예시 문장을 만들어줄 수 있다.  
하지만 실제 장애 이력을 조회하거나, 로그 파일을 읽거나, 관련 Git Commit을 찾거나, 사내 문서를 검색해서 종합 보고서를 만드는 일은 직접 수행하지 못한다.

또 다른 예를 보자.

```text
"프로젝트 폴더에 있는 문서를 읽고 핵심 내용을 요약해줘."
```

LLM은 문서가 대화창에 붙여 넣어져 있으면 요약할 수 있다.  
하지만 로컬 파일 시스템에 직접 접근해서 파일 목록을 보고, 필요한 파일을 선택하고, 내용을 읽고, 요약하는 과정은 별도의 실행 구조가 필요하다.

AI Agent는 바로 이 문제를 해결하기 위해 등장했다.

```text
LLM:
- 질문을 이해한다.
- 답변을 생성한다.

AI Agent:
- 질문을 이해한다.
- 목표를 분석한다.
- 필요한 작업을 나눈다.
- 사용할 도구를 선택한다.
- 도구를 실행한다.
- 실행 결과를 확인한다.
- 필요하면 다시 작업한다.
- 최종 결과를 만든다.
```

즉, Agent는 **LLM의 판단 능력**과 **외부 도구 실행 능력**을 결합한 구조이다.

---

## 3. 기존 방식의 한계

---

### 3.1 일반 Chatbot의 한계

일반 Chatbot 구조는 매우 단순하다.

```text
사용자 질문
   ↓
LLM
   ↓
답변 생성
```

이 구조는 다음과 같은 질문에는 잘 동작한다.

```text
"RAG가 뭐야?"
"Python의 list와 tuple 차이가 뭐야?"
"이 문장을 공손하게 다듬어줘."
```

하지만 다음과 같은 요청에는 한계가 있다.

```text
"내 프로젝트 폴더에 있는 문서를 읽어줘."
"오늘 운영 서버 상태를 점검해줘."
"지난달 매출 데이터를 분석해서 표로 만들어줘."
"이메일을 작성해서 담당자에게 보내줘."
```

이런 요청은 단순 답변이 아니라 **행동**이 필요하다.

---

### 3.2 RAG의 한계

RAG는 LLM의 한계를 많이 보완한다.

RAG 구조는 대략 다음과 같다.

```text
사용자 질문
   ↓
문서 검색
   ↓
관련 문서 Chunk 추출
   ↓
LLM에 참고 문서 전달
   ↓
답변 생성
```

RAG를 사용하면 LLM이 사내 문서나 프로젝트 문서를 근거로 답변할 수 있다.  
즉, RAG는 **문서를 찾아서 답변하는 AI**를 만들 수 있게 해준다.

하지만 RAG도 기본적으로는 검색과 답변 중심이다.

RAG가 잘하는 일은 다음과 같다.

```text
1. 문서에서 관련 내용을 찾는다.
2. 찾은 내용을 근거로 답변한다.
3. 출처를 함께 제공한다.
```

반면 RAG만으로는 다음 작업을 처리하기 어렵다.

```text
1. 여러 단계를 스스로 계획한다.
2. 필요한 도구를 상황에 따라 선택한다.
3. 도구 실행 결과를 보고 다음 행동을 결정한다.
4. 파일을 생성하거나 수정한다.
5. 외부 API를 호출한다.
6. 업무 시스템에 작업을 등록한다.
```

이 지점에서 Agent가 필요해진다.

---

## 4. Chatbot, RAG, Agent 비교

아래 표는 세 가지 구조의 차이를 정리한 것이다.

| 구분 | Chatbot | RAG | AI Agent |
|---|---|---|---|
| 핵심 목적 | 대화와 답변 생성 | 문서 검색 기반 답변 | 목표 달성을 위한 작업 수행 |
| 외부 문서 활용 | 제한적 | 강함 | 필요 시 활용 |
| 도구 사용 | 거의 없음 | 검색 도구 중심 | 다양한 도구 사용 |
| 작업 계획 | 없음 | 제한적 | 가능 |
| 반복 수행 | 없음 | 제한적 | 가능 |
| 상태 관리 | 대화 이력 중심 | 검색 결과 중심 | 작업 상태와 실행 이력 관리 |
| 대표 예시 | FAQ 챗봇 | 사내 문서 Q&A | 보고서 작성, 시스템 점검, 업무 자동화 |
| 한계 | 실제 업무 수행 어려움 | 검색 이후 행동 어려움 | 통제와 보안 설계 필요 |

한 문장으로 정리하면 다음과 같다.

```text
Chatbot은 답변한다.
RAG는 찾아서 답변한다.
Agent는 판단하고 실행한다.
```

---

## 5. AI Agent란 무엇인가?

AI Agent는 사용자의 목표를 달성하기 위해 LLM을 중심으로 여러 구성 요소를 연결한 실행 시스템이다.

Agent를 단순하게 표현하면 다음과 같다.

```text
AI Agent = LLM + Planning + Tool Calling + Memory + Execution Loop
```

각 구성 요소의 의미는 다음과 같다.

```text
LLM:
- 사용자의 요청을 이해한다.
- 어떤 작업이 필요한지 판단한다.
- 도구 결과를 해석한다.
- 최종 답변을 생성한다.

Planning:
- 큰 요청을 작은 작업으로 나눈다.
- 어떤 순서로 처리할지 계획한다.

Tool Calling:
- 필요한 외부 도구를 선택하고 호출한다.
- 예: 검색, 계산, 파일 읽기, DB 조회, API 호출

Memory:
- 이전 대화와 작업 상태를 기억한다.
- 중간 결과와 실행 이력을 보관한다.

Execution Loop:
- 생각, 행동, 관찰을 반복한다.
- 결과가 충분할 때까지 작업을 이어간다.
```

---

## 6. AI Agent의 기본 구성 요소

---

### 6.1 LLM

LLM은 Agent의 판단 중심이다.

LLM은 다음 역할을 담당한다.

```text
1. 사용자 요청 이해
2. 작업 의도 분석
3. 필요한 도구 판단
4. 도구 결과 해석
5. 최종 답변 생성
```

다만 LLM은 실제 시스템 작업을 직접 수행하지 않는다.  
파일을 읽거나, DB를 조회하거나, 메일을 보내는 일은 도구가 수행한다.

---

### 6.2 Prompt

Prompt는 Agent에게 역할과 규칙을 알려주는 지시문이다.

Agent Prompt에는 보통 다음 내용이 포함된다.

```text
1. Agent의 역할
2. 사용할 수 있는 도구 목록
3. 도구 사용 규칙
4. 답변 형식
5. 하지 말아야 할 행동
6. 오류가 발생했을 때의 처리 방식
```

예를 들어 사내 문서 검색 Agent라면 다음과 같은 지시가 들어갈 수 있다.

```text
너는 사내 문서 기반 업무 도우미이다.
답변은 반드시 검색된 문서를 근거로 작성한다.
문서에서 확인되지 않는 내용은 추측하지 않는다.
필요한 경우 search_documents 도구를 사용한다.
답변 마지막에는 참고한 문서를 요약한다.
```

---

### 6.3 Tool

Tool은 Agent가 사용할 수 있는 외부 기능이다.

처음에는 Python 함수 하나도 Tool이 될 수 있다.

```text
calculator:
- 계산이 필요할 때 사용

file_reader:
- 파일 내용을 읽을 때 사용

search_documents:
- 문서를 검색할 때 사용

query_database:
- DB에서 데이터를 조회할 때 사용

send_email:
- 이메일을 보낼 때 사용
```

중요한 점은 **LLM이 직접 실행하는 것이 아니라, LLM은 어떤 도구를 어떤 입력값으로 호출할지 결정하고, 실제 실행은 애플리케이션 코드가 담당한다**는 것이다.

---

### 6.4 Tool Schema

Tool Schema는 도구 사용 설명서이다.

LLM이 도구를 올바르게 사용하려면 다음 정보를 알아야 한다.

```text
1. 도구 이름
2. 도구 설명
3. 입력값
4. 입력값 타입
5. 필수 입력값
6. 반환값 의미
```

예시는 다음과 같다.

```json
{
  "name": "search_documents",
  "description": "사내 문서에서 질문과 관련된 내용을 검색한다.",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "검색할 질문 또는 키워드"
      }
    },
    "required": ["query"]
  }
}
```

Tool Schema가 명확해야 Agent가 도구를 잘못 호출할 가능성이 줄어든다.

---

### 6.5 Memory

Memory는 Agent가 맥락과 상태를 유지하기 위한 구성 요소이다.

Memory는 크게 세 가지로 나눌 수 있다.

```text
Conversation Memory:
- 대화 이력
- 사용자가 이전에 무엇을 요청했는지 저장

Task Memory:
- 현재 진행 중인 작업 상태
- 어떤 파일을 읽었는지, 어떤 검색을 했는지 저장

Long-term Memory:
- 여러 대화에 걸쳐 유지되는 정보
- 프로젝트 설정, 사용자 선호, 자주 사용하는 경로 등
```

Memory가 없으면 Agent는 매 요청을 독립적으로 처리한다.  
Memory가 있으면 Agent는 이전 맥락을 바탕으로 더 자연스럽게 작업을 이어갈 수 있다.

---

### 6.6 Planner

Planner는 큰 작업을 작은 단계로 나누는 역할을 한다.

예를 들어 사용자가 다음과 같이 요청했다고 하자.

```text
"지난주 장애 내용을 정리해서 보고서 초안을 만들어줘."
```

Planner는 이 요청을 다음과 같이 나눌 수 있다.

```text
1. 지난주 기간 계산
2. 장애 이력 조회
3. 장애 유형 분류
4. 주요 원인 정리
5. 조치 내용 정리
6. 보고서 초안 작성
7. 누락 항목 검토
```

간단한 Agent는 Planner 없이 동작할 수 있다.  
하지만 업무가 복잡해질수록 Planning은 매우 중요해진다.

---

### 6.7 Executor

Executor는 실제 도구를 실행하는 구성 요소이다.

LLM이 다음과 같은 도구 호출 요청을 만들었다고 하자.

```json
{
  "tool_name": "calculator",
  "arguments": {
    "expression": "12500 * 17"
  }
}
```

Executor는 이 요청을 받아 실제 계산기 함수를 실행한다.

```text
calculator("12500 * 17")
```

그리고 실행 결과를 다시 LLM에게 전달한다.

```text
212500
```

Executor는 보안 측면에서도 중요하다.  
허용되지 않은 도구 호출을 차단하고, 입력값을 검증하고, 실행 로그를 남기는 역할을 담당한다.

---

## 7. AI Agent의 동작 흐름

Agent는 보통 다음과 같은 흐름으로 동작한다.

```text
1. 사용자 요청 입력
2. LLM이 요청 의도 분석
3. 필요한 작업 판단
4. 필요한 도구 선택
5. 도구 실행
6. 실행 결과 관찰
7. 추가 작업 필요 여부 판단
8. 필요하면 다시 도구 실행
9. 충분하면 최종 답변 생성
```

이를 그림으로 표현하면 다음과 같다.

```text
사용자
  │
  ▼
Agent
  │
  ├─ 요청 이해
  │
  ├─ 계획 수립
  │
  ├─ 도구 선택
  │
  ├─ 도구 실행
  │
  ├─ 결과 관찰
  │
  └─ 최종 답변
```

조금 더 실제 구조에 가깝게 표현하면 다음과 같다.

```text
사용자 요청
   ↓
Prompt + Context + Tool Schema
   ↓
LLM
   ↓
도구 호출 여부 판단
   ↓
Tool Executor
   ↓
Tool Result
   ↓
LLM
   ↓
Final Answer
```

---

## 8. Agent 실행 루프

Agent의 핵심은 한 번에 답변을 끝내지 않고, 필요하면 반복한다는 점이다.

이를 Agent Loop라고 부를 수 있다.

```text
while 작업이 끝나지 않음:
    현재 상태를 LLM에게 전달한다.
    LLM이 다음 행동을 결정한다.

    if 도구 호출이 필요함:
        도구를 실행한다.
        실행 결과를 상태에 추가한다.
    else:
        최종 답변을 생성한다.
        종료한다.
```

Agent Loop는 이후 Step3-2의 ReAct와 연결된다.

ReAct에서는 이 흐름을 다음 세 단계로 표현한다.

```text
Thought:
- 무엇을 해야 하는지 생각한다.

Action:
- 필요한 도구를 사용한다.

Observation:
- 도구 실행 결과를 확인한다.
```

즉, Agent Loop는 다음 패턴을 반복한다.

```text
Thought → Action → Observation → Thought → Action → Observation → Final Answer
```

---

## 9. AI Agent 예시

---

### 9.1 계산 Agent

사용자 요청:

```text
"12,500원 상품을 17개 사면 총액이 얼마야?"
```

Agent 동작:

```text
1. 계산이 필요하다고 판단한다.
2. calculator 도구를 선택한다.
3. 12500 * 17을 계산한다.
4. 결과를 확인한다.
5. "총액은 212,500원입니다."라고 답변한다.
```

---

### 9.2 파일 요약 Agent

사용자 요청:

```text
"docs 폴더의 RAG 가이드를 읽고 요약해줘."
```

Agent 동작:

```text
1. 파일 읽기 또는 문서 검색이 필요하다고 판단한다.
2. file_reader 또는 search_documents 도구를 선택한다.
3. 관련 문서를 읽는다.
4. 핵심 내용을 요약한다.
5. 출처를 함께 답변한다.
```

---

### 9.3 운영 점검 Agent

사용자 요청:

```text
"AI 플랫폼 상태를 점검해줘."
```

Agent 동작:

```text
1. 점검 대상 목록을 만든다.
2. Docker 상태 확인 도구를 호출한다.
3. Ollama 상태 확인 도구를 호출한다.
4. Open WebUI 상태 확인 도구를 호출한다.
5. ChromaDB 경로와 파일 상태를 확인한다.
6. 종합 점검 결과를 정리한다.
```

---

### 9.4 보고서 작성 Agent

사용자 요청:

```text
"지난주 장애 내용을 보고서 초안으로 만들어줘."
```

Agent 동작:

```text
1. 지난주 날짜 범위를 계산한다.
2. 장애 이력 시스템을 조회한다.
3. 관련 로그와 조치 내용을 검색한다.
4. 장애 유형별로 분류한다.
5. 원인과 조치 내용을 요약한다.
6. 보고서 초안을 작성한다.
7. 누락된 항목이 있는지 검토한다.
```

이 예시는 Agent가 단순 답변이 아니라 실제 업무 흐름을 수행하는 구조임을 보여준다.

---

## 10. AI Agent 아키텍처

---

### 10.1 기본 Agent 아키텍처

```text
사용자
  │
  ▼
Agent Application
  │
  ├─ Prompt
  ├─ Memory
  ├─ Tool Schema
  ├─ Planner
  └─ Executor
        │
        ▼
      Tools
        │
        ├─ Search
        ├─ File Reader
        ├─ Calculator
        ├─ Database
        └─ API
```

---

### 10.2 RAG 연동 Agent 아키텍처

Step2에서 만든 RAG는 Agent의 중요한 도구가 될 수 있다.

```text
사용자
  │
  ▼
AI Agent
  │
  ├─ 질문 분석
  ├─ RAG 검색 필요 여부 판단
  │
  ▼
RAG Search Tool
  │
  ├─ Embedding
  ├─ Vector DB
  └─ 유사 문서 검색
  │
  ▼
검색 결과
  │
  ▼
LLM 답변 생성
```

즉, RAG는 Agent와 경쟁하는 구조가 아니라 Agent가 사용하는 도구 중 하나로 볼 수 있다.

```text
RAG = 문서 검색 도구
Agent = 도구를 선택하고 실행하는 주체
```

---

### 10.3 Enterprise Agent 아키텍처

기업 환경에서는 Agent가 단순히 Python 함수 몇 개를 호출하는 수준을 넘어선다.

```text
사용자 / Open WebUI
        │
        ▼
AI Agent Gateway
        │
        ▼
Agent Runtime
        │
        ├─ Planner
        ├─ Memory
        ├─ Tool Registry
        ├─ Tool Executor
        └─ Policy Guard
        │
        ▼
Tool / MCP Layer
        │
        ├─ RAG Search Tool
        ├─ File Tool
        ├─ DB Tool
        ├─ Git Tool
        ├─ Jira Tool
        └─ Mail Tool
        │
        ▼
Enterprise Systems
```

Enterprise 환경에서는 다음 요소가 중요하다.

```text
1. 사용자 인증
2. 권한 관리
3. 도구 실행 통제
4. 감사 로그
5. 민감정보 보호
6. 승인 절차
7. 장애 대응
8. 모니터링
```

---

## 11. Agent 유형

---

### 11.1 단일 Agent

단일 Agent는 하나의 Agent가 전체 작업을 처리하는 구조이다.

```text
사용자 요청
   ↓
Single Agent
   ↓
Tool 실행
   ↓
최종 답변
```

처음 학습할 때는 단일 Agent부터 시작하는 것이 좋다.  
구조가 단순하고 Agent Loop를 이해하기 쉽기 때문이다.

---

### 11.2 Workflow Agent

Workflow Agent는 정해진 흐름에 따라 동작하는 Agent이다.

```text
START
  ↓
질문 분석
  ↓
검색
  ↓
검증
  ↓
답변 생성
  ↓
END
```

업무 절차가 명확한 경우 Workflow Agent가 적합하다.

예를 들어 다음 업무는 Workflow로 만들기 좋다.

```text
1. 보고서 작성
2. 결재 문서 검토
3. 장애 점검
4. 배치 실행 결과 확인
5. 문서 품질 검토
```

---

### 11.3 Planning Agent

Planning Agent는 큰 목표를 작은 작업으로 나누는 Agent이다.

```text
사용자 목표
   ↓
작업 분해
   ↓
실행 순서 결정
   ↓
각 작업 수행
   ↓
결과 통합
```

복잡한 요청일수록 Planning이 중요하다.

---

### 11.4 Multi Agent

Multi Agent는 여러 Agent가 역할을 나누어 협업하는 구조이다.

```text
사용자 요청
   ↓
Supervisor Agent
   ├─ Planner Agent
   ├─ Search Agent
   ├─ Analysis Agent
   ├─ Report Agent
   └─ QA Agent
```

Multi Agent는 강력하지만, 처음부터 사용하면 구조가 복잡해질 수 있다.  
따라서 Step3 후반부에서 학습하는 것이 좋다.

---

## 12. Agent와 MCP의 관계

MCP는 Model Context Protocol의 약자이다.

Agent가 외부 시스템을 사용할 때 각 시스템마다 다른 방식으로 연동하면 구조가 복잡해진다.

```text
파일 시스템 연동 방식
DB 연동 방식
Git 연동 방식
Jira 연동 방식
메일 연동 방식
```

MCP는 이러한 외부 시스템 연결을 표준화하는 역할을 한다.

```text
Agent
  ↓
MCP Client
  ↓
MCP Server
  ↓
외부 시스템
```

즉, MCP는 Agent가 도구를 사용하는 방식을 더 표준화하고 확장하기 위한 구조라고 볼 수 있다.

Step3에서는 먼저 Tool Calling을 이해하고, 이후 MCP를 통해 외부 시스템 연동 구조로 확장한다.

---

## 13. AI Agent의 장점

AI Agent의 장점은 다음과 같다.

```text
1. 단순 답변을 넘어 실제 작업을 수행할 수 있다.
2. 여러 도구를 상황에 맞게 사용할 수 있다.
3. 복잡한 작업을 단계적으로 처리할 수 있다.
4. RAG, DB, API, 파일 시스템을 통합할 수 있다.
5. 반복 작업을 자동화할 수 있다.
6. 업무 흐름을 지능형으로 구성할 수 있다.
```

특히 AI DATA Platform 프로젝트에서는 Agent가 다음 역할을 할 수 있다.

```text
1. 사내 문서 검색 도우미
2. 제안서 작성 보조 Agent
3. RAG 인덱싱 상태 점검 Agent
4. Open WebUI / Ollama 상태 점검 Agent
5. GitHub 문서 변경 요약 Agent
6. 장애 보고서 초안 작성 Agent
7. 프로젝트 문서 품질 검토 Agent
```

---

## 14. AI Agent의 위험과 한계

AI Agent는 강력하지만 위험도 함께 가진다.

---

### 14.1 잘못된 도구 호출

Agent가 잘못된 도구를 선택할 수 있다.

예를 들어 단순히 조회해야 하는 상황에서 삭제 도구를 호출하면 큰 문제가 생길 수 있다.

따라서 도구는 다음과 같이 분리해야 한다.

```text
읽기 도구:
- 검색
- 조회
- 파일 읽기
- 상태 확인

쓰기 도구:
- 파일 생성
- DB 수정
- 메일 발송
- 티켓 생성
- 배포 실행
```

처음에는 읽기 도구만 허용하는 것이 안전하다.

---

### 14.2 권한 문제

Agent가 모든 시스템에 접근할 수 있으면 위험하다.

Enterprise 환경에서는 반드시 사용자 권한을 기준으로 도구 실행 범위를 제한해야 한다.

```text
사용자 권한 확인
   ↓
도구 실행 가능 여부 판단
   ↓
허용된 범위 내에서만 실행
```

---

### 14.3 환각 문제

Agent도 결국 LLM을 사용하므로 잘못된 판단을 할 수 있다.

따라서 다음 원칙이 필요하다.

```text
1. 중요한 정보는 반드시 도구 결과를 근거로 사용한다.
2. 문서에 없는 내용은 추측하지 않는다.
3. 도구 실행 결과와 최종 답변을 분리해서 기록한다.
4. 중요한 작업은 사람 승인 후 실행한다.
```

---

### 14.4 비용과 성능 문제

Agent는 여러 번 LLM을 호출하고 여러 도구를 사용할 수 있다.  
따라서 일반 Chatbot보다 비용과 시간이 더 많이 들 수 있다.

해결 방안은 다음과 같다.

```text
1. 불필요한 도구 호출을 줄인다.
2. 단순 질문은 바로 답변한다.
3. 자주 쓰는 결과는 캐시한다.
4. 긴 작업은 Workflow로 관리한다.
5. 로그를 분석해서 병목을 찾는다.
```

---

## 15. Enterprise AI Agent 설계 원칙

기업 환경에서 Agent를 설계할 때는 다음 원칙이 중요하다.

```text
1. 처음부터 모든 것을 자동화하지 않는다.
2. 읽기 전용 도구부터 시작한다.
3. 쓰기 작업은 승인 절차를 둔다.
4. 도구 실행 로그를 반드시 남긴다.
5. 사용자 권한을 도구 실행 권한과 연결한다.
6. Agent의 판단 결과와 실제 실행 결과를 구분한다.
7. 실패했을 때 복구 가능한 구조로 만든다.
8. RAG를 통해 답변 근거를 강화한다.
9. MCP를 통해 외부 시스템 연동을 표준화한다.
10. Multi Agent는 단일 Agent가 안정화된 후 도입한다.
```

특히 중요한 원칙은 다음이다.

> **Agent는 강력할수록 더 많은 통제가 필요하다.**

---

## 16. Step3 학습 로드맵

Step3는 다음 순서로 진행한다.

```text
Part1. AI Agent 기초

Step3-1. AI Agent 개요
- Agent가 무엇인지 이해한다.
- Chatbot, RAG, Agent 차이를 이해한다.
- Agent 기본 구성 요소를 학습한다.

Step3-2. ReAct와 Tool Calling
- Agent의 생각과 행동 패턴을 이해한다.
- Thought / Action / Observation 구조를 학습한다.
- Tool Calling 개념을 이해한다.

Step3-3. 첫 번째 AI Agent 구현
- Python으로 단일 Agent를 구현한다.
- Tool Registry와 Tool Executor를 만든다.
- 간단한 도구를 호출하는 구조를 만든다.

Step3-4. Agent Memory와 상태 관리
- 대화 이력과 작업 상태를 저장한다.
- Short-term Memory와 Long-term Memory를 구분한다.
```

```text
Part2. AI Agent 심화

Step3-5. Planning Agent와 Workflow
- 복잡한 작업을 단계별로 분해한다.
- 계획 수립과 실행 구조를 학습한다.

Step3-6. LangGraph 기반 Workflow Agent
- Graph 기반으로 Agent 흐름을 제어한다.
- State, Node, Edge 개념을 학습한다.

Step3-7. MCP 아키텍처 이해
- MCP의 Client/Server 구조를 이해한다.
- Agent 도구 연동을 표준화하는 방법을 학습한다.

Step3-8. MCP 기반 외부 시스템 연동
- 파일, RAG, DB, API를 MCP로 연결하는 구조를 실습한다.
```

```text
Part3. Enterprise AI Agent

Step3-9. Multi Agent 협업
- 여러 Agent가 역할을 나누어 협업하는 구조를 학습한다.

Step3-10. Enterprise AI Agent Platform
- Agent Gateway, Tool Registry, MCP Layer, Observability, 보안 구조를 통합 설계한다.
```

---

## 17. 이번 단계에서 실습하지 않는 것

Step3-1은 개요 문서이므로 복잡한 Python 코드를 작성하지 않는다.

이번 문서에서는 다음을 실습하지 않는다.

```text
1. 실제 Tool Calling 코드 구현
2. LangGraph 설치와 실행
3. MCP Server 구현
4. Multi Agent 구현
5. Enterprise Agent Gateway 구현
```

이 내용은 이후 문서에서 순서대로 다룬다.

Step3-1에서는 먼저 큰 그림을 이해하는 것이 중요하다.

---

## 18. 핵심 정리

이번 문서의 핵심은 다음과 같다.

```text
1. Chatbot은 답변 중심이다.
2. RAG는 문서 검색 기반 답변 중심이다.
3. Agent는 목표 달성을 위한 작업 수행 중심이다.
4. Agent는 LLM, Prompt, Tool, Memory, Planner, Executor로 구성된다.
5. Agent는 생각하고, 도구를 사용하고, 결과를 관찰하는 과정을 반복한다.
6. RAG는 Agent와 경쟁하는 구조가 아니라 Agent가 사용할 수 있는 중요한 도구이다.
7. MCP는 Agent의 외부 시스템 연동을 표준화하는 구조이다.
8. Enterprise Agent는 반드시 보안, 권한, 감사 로그, 승인 절차를 함께 설계해야 한다.
```

한 문장으로 정리하면 다음과 같다.

> **AI Agent는 LLM이 단순히 답변하는 수준을 넘어, 도구를 사용해 실제 업무를 수행하도록 만든 실행 구조이다.**

---

## 19. 다음 단계 예고

다음 문서는 다음과 같다.

```text
Step3-2. ReAct와 Tool Calling
docs/study/step3/step3_2_react_and_tool_calling_guide.md
```

Step3-2에서는 Agent가 실제로 어떻게 생각하고 행동하는지 더 자세히 학습한다.

다음 단계의 핵심 개념은 다음과 같다.

```text
1. ReAct
2. Reasoning
3. Acting
4. Thought
5. Action
6. Observation
7. Tool Calling
8. Function Calling
9. Tool Schema
```

Step3-1이 전체 그림을 이해하는 단계라면, Step3-2는 Agent의 핵심 동작 원리를 깊게 이해하는 단계이다.

---

## 20. 참고 자료

아래 자료는 AI Agent 개념과 최신 Agent 설계 관점을 이해하는 데 참고할 수 있는 공식 자료이다.

```text
LangChain Agents Documentation
https://docs.langchain.com/oss/python/langchain/agents

LangChain Overview
https://docs.langchain.com/oss/python/langchain/overview

Anthropic - Building Effective AI Agents
https://www.anthropic.com/research/building-effective-agents

Model Context Protocol 공식 문서
https://modelcontextprotocol.io/docs/getting-started/intro

OpenAI Platform Documentation
https://platform.openai.com/docs/
```

---

## 21. 부록: AI DATA Platform 관점에서의 Agent 위치

AI DATA Platform 연구 로드맵에서 Agent의 위치는 다음과 같다.

```text
Step1. Local LLM
- 로컬에서 LLM을 실행한다.
- Ollama와 Open WebUI를 사용한다.

Step2. RAG
- 문서를 Embedding한다.
- Vector DB에 저장한다.
- 질문과 유사한 문서를 검색한다.
- 검색 결과를 LLM 답변에 활용한다.

Step3. AI Agent
- LLM이 도구를 사용할 수 있게 한다.
- RAG, 파일, DB, API를 도구로 연결한다.
- 업무 수행 구조를 만든다.

Step4. AI Data Platform
- Agent, RAG, MCP, Gateway, 보안, 모니터링을 플랫폼화한다.

Step5. AI Service / Serving
- 실제 사용자 서비스로 배포하고 운영한다.
```

즉, Step3는 단순히 새로운 기능 하나를 배우는 단계가 아니다.  
Step3는 Step1과 Step2에서 만든 기반을 실제 업무 자동화 구조로 확장하는 핵심 전환점이다.

---
