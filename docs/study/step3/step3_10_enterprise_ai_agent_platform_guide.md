# Step3-10. Enterprise AI Agent Platform 가이드

> AI DATA Platform 연구 프로젝트  
> Step3. AI Agent  
> Part3. Enterprise AI Agent  
> 문서 경로: `docs/study/step3/step3_10_enterprise_ai_agent_platform_guide.md`  
> 작성일: 2026-06-30

---

## 1. 문서 목적

이 문서는 Step3의 마지막 문서로, 지금까지 학습한 RAG, Tool Calling, Memory, Planning, LangGraph, MCP, Multi Agent 개념을 하나의 **Enterprise AI Agent Platform** 아키텍처로 통합하기 위한 가이드 문서이다.

앞 단계까지의 학습 흐름은 다음과 같다.

```text
Step3-1:
AI Agent 개요

Step3-2:
ReAct와 Tool Calling

Step3-3:
첫 번째 AI Agent 구현

Step3-4:
Agent Memory와 상태 관리

Step3-5:
Planning Agent와 Workflow

Step3-6:
LangGraph 기반 Workflow Agent

Step3-7:
MCP 아키텍처 이해

Step3-8:
MCP 기반 외부 시스템 연동

Step3-9:
Multi Agent 협업
```

이번 Step3-10에서는 위 내용을 모두 묶어 실제 기업 환경에서 운영 가능한 AI Agent Platform을 설계한다.

이번 문서의 핵심은 다음 한 문장으로 요약할 수 있다.

> **Enterprise AI Agent Platform은 여러 Agent, Workflow, Tool, MCP, Memory, 권한, 승인, 로그, 모니터링을 통합하여 기업 업무에 안전하게 적용할 수 있도록 만든 Agent 운영 플랫폼이다.**

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
│   ├─ Step3-6. LangGraph 기반 Workflow Agent
│   ├─ Step3-7. MCP 아키텍처 이해
│   └─ Step3-8. MCP 기반 외부 시스템 연동
│
└─ Part3. Enterprise AI Agent
    ├─ Step3-9. Multi Agent 협업
    └─ Step3-10. Enterprise AI Agent Platform   ← 현재 문서
```

Step3-10은 Step3 전체의 마무리 단계이다.

이 문서를 통해 단순 Agent 실습을 넘어, 실제 기업 시스템에 적용할 수 있는 플랫폼 구조를 이해한다.

---

## 3. 학습 목표

이 문서를 마치면 다음 내용을 설명할 수 있어야 한다.

```text
1. Enterprise AI Agent Platform이 왜 필요한지 설명할 수 있다.
2. 단일 Agent와 Agent Platform의 차이를 설명할 수 있다.
3. Agent Gateway의 역할을 이해할 수 있다.
4. Agent Registry와 Tool Registry의 필요성을 설명할 수 있다.
5. Workflow Runtime의 역할을 설명할 수 있다.
6. MCP Client Layer와 MCP Server Layer의 역할을 구분할 수 있다.
7. Memory Store와 Persistence 구조를 설명할 수 있다.
8. Policy Guard와 Human Approval 구조를 이해할 수 있다.
9. Observability와 Audit Log의 필요성을 설명할 수 있다.
10. AI DATA Platform 프로젝트 기준의 Enterprise Agent 아키텍처를 설계할 수 있다.
```

---

## 4. 왜 Enterprise AI Agent Platform이 필요한가?

Step3 초반에는 간단한 Agent를 만들었다.

```text
사용자 질문
   ↓
Agent
   ↓
Tool
   ↓
답변
```

이 구조는 학습에는 좋다.

하지만 기업 환경에서는 다음 요구사항이 생긴다.

```text
1. 여러 사용자가 동시에 사용해야 한다.
2. 사용자별 권한을 제어해야 한다.
3. 여러 Agent를 등록하고 관리해야 한다.
4. 여러 Tool과 외부 시스템을 연결해야 한다.
5. Tool 실행 이력을 남겨야 한다.
6. 위험한 작업은 승인 후 실행해야 한다.
7. 장애 발생 시 원인을 추적해야 한다.
8. 비용과 사용량을 관리해야 한다.
9. 문서, DB, API 접근 권한을 통제해야 한다.
10. 보안 감사와 운영 모니터링이 필요하다.
```

즉, 단순한 Agent 코드만으로는 부족하다.

기업 환경에서는 Agent를 운영하기 위한 플랫폼이 필요하다.

```text
Agent 코드
   ↓
Agent Runtime
   ↓
Agent Platform
   ↓
Enterprise AI Service
```

---

## 5. 단일 Agent와 Enterprise Agent Platform 비교

| 구분 | 단일 Agent | Enterprise Agent Platform |
|---|---|---|
| 목적 | 하나의 작업 처리 | 여러 Agent와 업무 흐름 운영 |
| 사용자 | 개인 또는 개발자 | 조직, 팀, 부서, 현업 사용자 |
| 권한 관리 | 거의 없음 | 사용자/역할/문서/Tool별 통제 |
| Tool 관리 | 코드 내부 등록 | Registry와 MCP Layer로 관리 |
| Workflow | 단순 if문 또는 루프 | LangGraph 등 Runtime 기반 |
| Memory | 로컬 변수 또는 파일 | Session/Long-term/Audit Store |
| 승인 | 수동 처리 | Human Approval Workflow |
| 로그 | print 또는 단순 로그 | Trace, Audit, Observability |
| 운영 | 로컬 실행 | 서버, API, UI, 모니터링 |
| 보안 | 개발자 책임 | 정책 기반 통제 |

한 문장으로 정리하면 다음과 같다.

```text
단일 Agent는 기능이고, Enterprise Agent Platform은 운영 체계이다.
```

---

## 6. Enterprise AI Agent Platform 전체 구조

AI DATA Platform 프로젝트 기준으로 Enterprise AI Agent Platform은 다음 구조로 설계할 수 있다.

```text
사용자 / 현업 / 개발자
        │
        ▼
Agent UI / Open WebUI / Custom Portal
        │
        ▼
Agent Gateway
        │
        ▼
Agent Runtime
        │
        ├─ Agent Registry
        ├─ Workflow Runtime
        ├─ Planner
        ├─ Multi Agent Orchestrator
        ├─ Memory Manager
        ├─ Policy Guard
        └─ Human Approval
        │
        ▼
Tool Access Layer
        │
        ├─ Tool Registry
        ├─ MCP Client Layer
        └─ Tool Executor
        │
        ▼
MCP Server Layer
        │
        ├─ File MCP Server
        ├─ RAG MCP Server
        ├─ DB MCP Server
        ├─ API MCP Server
        └─ 업무시스템 MCP Server
        │
        ▼
Enterprise Systems
        │
        ├─ 문서 저장소
        ├─ Vector DB
        ├─ Database
        ├─ 사내 API
        ├─ Git / Jira
        └─ 운영 로그
```

이 구조에서 중요한 점은 다음이다.

```text
1. 사용자 요청은 Gateway를 통과한다.
2. Agent Runtime은 어떤 Agent와 Workflow를 실행할지 결정한다.
3. Tool 호출은 Registry와 Policy Guard를 거친다.
4. 외부 시스템은 MCP Server를 통해 표준화한다.
5. 모든 실행 과정은 Trace와 Audit Log로 남긴다.
```

---

## 7. 주요 구성요소

Enterprise AI Agent Platform은 다음 구성요소로 나눌 수 있다.

```text
1. Agent UI
2. Agent Gateway
3. Agent Registry
4. Agent Runtime
5. Workflow Runtime
6. Multi Agent Orchestrator
7. Tool Registry
8. MCP Client Layer
9. MCP Server Layer
10. Memory Store
11. Policy Guard
12. Human Approval
13. Observability
14. Audit Log
15. Evaluation
```

각 구성요소를 하나씩 살펴본다.

---

## 8. Agent UI

Agent UI는 사용자가 Agent를 사용하는 화면이다.

예시는 다음과 같다.

```text
Open WebUI
사내 Agent Portal
Slack / Teams Bot
업무시스템 내 Agent 패널
개발자 CLI
관리자 콘솔
```

Agent UI의 역할은 다음과 같다.

```text
1. 사용자 질문 입력
2. Agent 선택
3. 파일 첨부
4. Knowledge 선택
5. 실행 결과 확인
6. 출처 확인
7. 승인 요청 처리
8. 실행 이력 조회
```

AI DATA Platform 초기 단계에서는 Open WebUI를 Agent UI로 사용할 수 있다.

이후 Enterprise 단계에서는 별도 Agent Portal을 만들 수 있다.

---

## 9. Agent Gateway

Agent Gateway는 사용자 요청이 Agent Runtime으로 들어가기 전에 거치는 진입점이다.

역할은 다음과 같다.

```text
1. 사용자 인증
2. 사용자 권한 확인
3. 요청 라우팅
4. 사용 가능한 Agent 목록 제공
5. 요청 크기 제한
6. 민감정보 사전 검사
7. Rate Limit
8. 실행 로그 시작
9. 세션 생성
```

Agent Gateway는 API Gateway와 비슷한 역할을 한다.

다만 일반 API Gateway보다 Agent 특화 기능이 추가된다.

```text
1. Agent 선택
2. Tool 권한 확인
3. Knowledge 접근 권한 확인
4. Prompt Injection 위험 탐지
5. Human Approval 요청 연결
```

---

## 10. Agent Registry

Agent Registry는 플랫폼에서 사용할 수 있는 Agent 목록과 설정을 관리한다.

예시는 다음과 같다.

```json
{
  "agent_id": "proposal_writer",
  "name": "제안서 작성 Agent",
  "description": "RFP 분석과 제안서 초안 작성을 지원한다.",
  "version": "1.0.0",
  "owner": "AI플랫폼팀",
  "allowed_tools": [
    "rag_search",
    "file_read",
    "template_read"
  ],
  "workflow": "proposal_workflow",
  "approval_required": false
}
```

Agent Registry가 필요한 이유는 다음과 같다.

```text
1. Agent를 체계적으로 등록하고 관리한다.
2. Agent별 권한과 Tool을 제한한다.
3. Agent 버전을 관리한다.
4. Agent 소유자와 책임자를 명확히 한다.
5. 사용 가능한 Agent를 UI에서 보여줄 수 있다.
6. 운영 중 Agent를 비활성화할 수 있다.
```

Enterprise 환경에서는 Agent를 코드만으로 관리하지 않고 Registry로 관리하는 것이 좋다.

---

## 11. Agent Runtime

Agent Runtime은 실제 Agent를 실행하는 핵심 엔진이다.

역할은 다음과 같다.

```text
1. 사용자 요청을 Agent에 전달한다.
2. Agent Prompt를 구성한다.
3. LLM을 호출한다.
4. Tool Call을 처리한다.
5. Workflow Runtime과 연동한다.
6. Memory를 읽고 쓴다.
7. 실행 결과를 반환한다.
```

Agent Runtime은 단순 LLM 호출기가 아니다.

Agent Runtime은 다음을 함께 처리해야 한다.

```text
1. 상태
2. 도구
3. 권한
4. 오류
5. 재시도
6. 승인
7. 로그
8. 추적
```

---

## 12. Workflow Runtime

Workflow Runtime은 Agent 실행 흐름을 제어한다.

Step3-6에서 LangGraph를 학습했다.

LangGraph 공식 문서에서는 LangGraph를 durable execution, streaming, human-in-the-loop, persistence를 제공하는 orchestration runtime으로 설명한다.

Enterprise AI Agent Platform에서 Workflow Runtime은 다음 역할을 한다.

```text
1. Workflow State 관리
2. Node 실행
3. Edge 흐름 제어
4. Conditional Edge 분기
5. 실패 시 재시도
6. 중간 상태 저장
7. Human Approval 지점 처리
8. 중단 후 재개
```

구조는 다음과 같다.

```text
Initial State
   ↓
Workflow Runtime
   ↓
Node 실행
   ↓
State 갱신
   ↓
다음 Node 결정
   ↓
Final State
```

Workflow Runtime이 없으면 복잡한 Agent 업무 흐름은 if문과 for문으로 뒤엉키기 쉽다.

---

## 13. Multi Agent Orchestrator

Step3-9에서는 Multi Agent 협업을 학습했다.

Enterprise Platform에서는 여러 Agent를 조율하는 Orchestrator가 필요하다.

역할은 다음과 같다.

```text
1. Supervisor Agent 실행
2. Worker Agent 호출
3. Agent 간 메시지 전달
4. Shared State 관리
5. Agent 결과 취합
6. Agent 간 충돌 조정
7. 최종 답변 생성
```

구조는 다음과 같다.

```text
Supervisor
  ├─ Planner Agent
  ├─ Research Agent
  ├─ Writer Agent
  ├─ Reviewer Agent
  └─ Security Agent
```

Multi Agent Orchestrator는 Workflow Runtime 위에서 동작할 수도 있다.

```text
LangGraph Node = Agent 실행 단위
```

---

## 14. Tool Registry

Tool Registry는 Agent가 사용할 수 있는 Tool 목록과 정책을 관리한다.

예시는 다음과 같다.

```json
{
  "tool_id": "db_select",
  "name": "DB 조회 Tool",
  "type": "mcp",
  "server": "db_mcp_server",
  "operation": "read",
  "risk_level": "medium",
  "approval_required": false,
  "allowed_roles": [
    "developer",
    "architect"
  ]
}
```

Tool Registry가 필요한 이유는 다음과 같다.

```text
1. Tool 목록을 중앙에서 관리한다.
2. Tool별 위험도를 관리한다.
3. Tool별 사용 권한을 관리한다.
4. Tool별 승인 필요 여부를 관리한다.
5. Tool 실행 로그와 연결한다.
6. MCP Server의 Tool과 Agent Runtime을 연결한다.
```

Tool Registry는 MCP와 함께 사용할 수 있다.

```text
Tool Registry:
Tool의 정책과 메타데이터 관리

MCP Server:
Tool의 실제 실행 기능 제공
```

---

## 15. MCP Client Layer

Step3-7과 Step3-8에서 MCP를 학습했다.

MCP 공식 문서에서는 MCP를 AI 애플리케이션이 외부 시스템에 연결하기 위한 표준 방식으로 설명한다. MCP Server는 데이터, 도구, 프롬프트를 제공할 수 있다.

Enterprise Platform에서는 MCP Client Layer가 다음 역할을 한다.

```text
1. MCP Server 연결 관리
2. MCP Tool 목록 조회
3. MCP Tool 호출
4. MCP Resource 조회
5. MCP Prompt 조회
6. 연결 상태 확인
7. Timeout과 Retry 처리
8. Tool 결과 표준화
```

구조는 다음과 같다.

```text
Agent Runtime
   ↓
MCP Client Layer
   ├─ File MCP Client
   ├─ RAG MCP Client
   ├─ DB MCP Client
   └─ API MCP Client
```

MCP Client Layer가 있으면 Agent Runtime은 외부 시스템별 세부 API를 직접 알 필요가 줄어든다.

---

## 16. MCP Server Layer

MCP Server Layer는 외부 시스템 기능을 MCP 방식으로 제공한다.

예시는 다음과 같다.

```text
File MCP Server:
파일 목록, 파일 읽기, 파일 검색

RAG MCP Server:
문서 검색, Chunk 조회, Collection 상태 확인

DB MCP Server:
테이블 목록, 스키마 조회, SELECT 실행

API MCP Server:
사내 API 조회, 상태 확인

Git MCP Server:
소스 조회, 변경 내역 조회

Jira MCP Server:
이슈 조회, 티켓 생성
```

MCP Server Layer의 핵심 원칙은 다음이다.

```text
1. 시스템별로 Server를 분리한다.
2. 읽기 Tool과 쓰기 Tool을 분리한다.
3. 입력값을 검증한다.
4. 권한을 확인한다.
5. 실행 로그를 남긴다.
6. 위험한 작업은 승인 후 실행한다.
```

MCP는 강력하지만 외부 시스템 실행 권한을 열어주는 구조이므로 보안 설계가 반드시 필요하다.

---

## 17. Memory Store

Agent Platform에는 Memory가 필요하다.

Memory는 크게 세 가지로 나눌 수 있다.

```text
1. Session Memory
2. Long-term Memory
3. Audit Memory
```

### 17.1 Session Memory

현재 대화 또는 현재 Workflow 실행 중에 필요한 상태를 저장한다.

```text
사용자 요청
현재 단계
중간 결과
검색 결과
Tool 결과
오류 상태
```

### 17.2 Long-term Memory

여러 세션에 걸쳐 재사용할 수 있는 정보를 저장한다.

```text
사용자 선호
프로젝트 정보
반복되는 업무 규칙
문서 작성 스타일
자주 사용하는 템플릿
```

### 17.3 Audit Memory

감사와 추적을 위해 실행 이력을 저장한다.

```text
누가
언제
어떤 Agent를
어떤 Tool로
어떤 입력값으로
어떤 결과를 만들었는가
```

LangGraph의 Persistence 문서에서는 checkpointer를 통한 short-term memory와 store를 통한 long-term memory 개념을 설명한다.

Enterprise 환경에서는 이 개념을 확장하여 Session Memory, Long-term Memory, Audit Memory로 나누는 것이 좋다.

---

## 18. Policy Guard

Policy Guard는 Agent가 위험한 행동을 하지 않도록 통제하는 정책 계층이다.

역할은 다음과 같다.

```text
1. 사용자 입력 검사
2. Prompt Injection 탐지
3. Tool 호출 허용 여부 판단
4. 민감정보 포함 여부 확인
5. 문서 접근 권한 확인
6. DB Query 제한
7. 파일 경로 제한
8. 외부 API 호출 제한
9. 승인 필요 여부 판단
10. 결과 응답 필터링
```

OpenAI Agents SDK도 Guardrails와 human review를 복잡한 workflow에서 고려해야 할 요소로 설명한다.

Enterprise Agent Platform에서는 Guardrail을 단순 안전 필터가 아니라 운영 정책 엔진으로 봐야 한다.

---

## 19. Human Approval

Human Approval은 Agent가 위험한 작업을 실행하기 전에 사람의 승인을 받는 구조이다.

승인이 필요한 작업 예시는 다음과 같다.

```text
1. 메일 발송
2. DB 수정
3. 파일 삭제
4. 외부 시스템 티켓 생성
5. 운영 배포
6. 고객사 문서 제출
7. 보안 정책 변경
```

Workflow 구조는 다음과 같다.

```text
Agent 작업 생성
   ↓
Preview 생성
   ↓
Human Approval 요청
   ↓
승인 여부
   ├─ 승인 → 실제 실행
   └─ 반려 → 수정 또는 중단
```

Human Approval은 Enterprise Agent의 핵심 통제 지점이다.

AI Agent가 단순히 추천하는 수준을 넘어 실제 업무 시스템을 변경하려면 반드시 승인 구조가 필요하다.

---

## 20. Observability

Observability는 Agent가 어떻게 동작했는지 관찰하고 분석하는 기능이다.

필요한 정보는 다음과 같다.

```text
1. 사용자 요청
2. 선택된 Agent
3. 실행된 Workflow
4. 호출된 LLM
5. Token 사용량
6. Tool Call 목록
7. MCP Server 호출
8. 실행 시간
9. 오류 메시지
10. 최종 답변
```

OpenAI Agents SDK의 Tracing 문서는 Agent run 동안 LLM generation, tool calls, handoffs, guardrails, custom events까지 추적할 수 있다고 설명한다.

Enterprise Platform에서는 Observability가 없으면 운영이 어렵다.

```text
왜 이런 답변이 나왔는가?
어떤 문서를 검색했는가?
어떤 Tool을 호출했는가?
어느 단계에서 실패했는가?
비용이 어디서 많이 발생했는가?
```

이 질문에 답하려면 Trace가 필요하다.

---

## 21. Audit Log

Audit Log는 보안 감사와 책임 추적을 위한 로그이다.

Observability가 개발과 운영 모니터링에 가깝다면, Audit Log는 보안과 감사 목적에 가깝다.

Audit Log에는 다음 정보가 포함되어야 한다.

```text
1. 사용자 ID
2. 사용자 역할
3. 요청 시간
4. Agent ID
5. Workflow ID
6. Tool ID
7. MCP Server ID
8. 입력 파라미터
9. 실행 결과
10. 승인자
11. 승인 시간
12. 실패 사유
```

예시는 다음과 같다.

```json
{
  "timestamp": "2026-06-30T15:30:00+09:00",
  "user_id": "user001",
  "role": "architect",
  "agent_id": "proposal_writer",
  "workflow_id": "proposal_workflow_v1",
  "tool_id": "rag_search",
  "mcp_server": "rag_mcp_server",
  "action": "tool_call",
  "status": "success",
  "approval_required": false
}
```

Enterprise Agent에서는 Audit Log가 선택이 아니라 필수에 가깝다.

---

## 22. Evaluation

Evaluation은 Agent 품질을 측정하는 구조이다.

평가 기준은 다음과 같다.

```text
1. 답변 정확성
2. 출처 적합성
3. 누락 여부
4. 환각 여부
5. 보안 정책 위반 여부
6. Tool 사용 적절성
7. 문서 작성 품질
8. 사용자 만족도
9. 실행 비용
10. 처리 시간
```

RAG 기반 Agent라면 다음 평가가 중요하다.

```text
검색된 문서가 질문과 관련 있는가?
답변이 검색 문서에 근거하고 있는가?
출처가 명확한가?
문서에 없는 내용을 추측하지 않았는가?
```

Multi Agent라면 다음 평가도 필요하다.

```text
Agent별 역할이 잘 수행되었는가?
중간 결과가 최종 답변에 반영되었는가?
Reviewer Agent가 오류를 잘 잡았는가?
Supervisor가 결과를 잘 통합했는가?
```

---

## 23. Enterprise AI Agent Platform 기준 아키텍처

AI DATA Platform 프로젝트에서 권장하는 Enterprise AI Agent Platform 구조는 다음과 같다.

```text
[User]
   │
   ▼
[Agent UI]
   │
   ▼
[Agent Gateway]
   │
   ├─ Auth
   ├─ Rate Limit
   ├─ Request Validation
   └─ Session Create
   │
   ▼
[Agent Runtime]
   │
   ├─ Agent Registry
   ├─ Prompt Manager
   ├─ Workflow Runtime
   ├─ Multi Agent Orchestrator
   ├─ Memory Manager
   ├─ Policy Guard
   └─ Human Approval
   │
   ▼
[Tool Access Layer]
   │
   ├─ Tool Registry
   ├─ MCP Client Layer
   └─ Tool Executor
   │
   ▼
[MCP Server Layer]
   │
   ├─ File MCP Server
   ├─ RAG MCP Server
   ├─ DB MCP Server
   ├─ API MCP Server
   └─ 업무시스템 MCP Server
   │
   ▼
[Enterprise Systems]
   │
   ├─ Document Store
   ├─ Vector DB
   ├─ Database
   ├─ Business API
   ├─ Git / Jira
   └─ Logs
```

횡단 관심사는 다음과 같다.

```text
Observability
Audit Log
Security
Evaluation
Cost Management
Monitoring
```

---

## 24. 플랫폼 계층별 책임

| 계층 | 책임 |
|---|---|
| Agent UI | 사용자 입력과 결과 표시 |
| Agent Gateway | 인증, 권한, 요청 통제 |
| Agent Runtime | Agent 실행과 LLM 호출 |
| Workflow Runtime | 실행 흐름과 상태 관리 |
| Multi Agent Orchestrator | 여러 Agent 협업 조율 |
| Memory Manager | 세션, 장기 기억, 감사 메모리 관리 |
| Policy Guard | 정책 검증과 위험 작업 차단 |
| Tool Registry | Tool 메타데이터와 권한 관리 |
| MCP Client Layer | MCP Server 연결과 Tool 호출 |
| MCP Server Layer | 외부 시스템 기능 제공 |
| Enterprise Systems | 실제 업무 데이터와 기능 제공 |
| Observability | 실행 추적과 모니터링 |
| Audit Log | 보안 감사와 책임 추적 |
| Evaluation | Agent 품질 평가 |

---

## 25. AI DATA Platform 적용 로드맵

AI DATA Platform 프로젝트에서는 Enterprise Agent Platform을 한 번에 만들지 않는다.

다음 단계로 확장하는 것이 현실적이다.

---

### 25.1 1단계: 단일 Agent 안정화

```text
1. Tool Calling 구조 정리
2. Tool Registry 정리
3. RAG Tool 연결
4. File Tool 연결
5. 기본 로그 추가
```

목표:

```text
하나의 Agent가 안전하게 Tool을 호출할 수 있다.
```

---

### 25.2 2단계: Workflow Runtime 도입

```text
1. Planning Agent 구현
2. LangGraph Workflow 적용
3. State 관리
4. 조건 분기
5. 실패 처리
```

목표:

```text
단순 Tool 호출이 아니라 업무 흐름을 제어할 수 있다.
```

---

### 25.3 3단계: MCP Layer 도입

```text
1. File MCP Server
2. RAG MCP Server
3. DB MCP Server
4. API MCP Server
5. MCP Client Layer
```

목표:

```text
외부 시스템 연동을 표준화한다.
```

---

### 25.4 4단계: Multi Agent 도입

```text
1. Supervisor Agent
2. Research Agent
3. Writer Agent
4. Reviewer Agent
5. Security Agent
```

목표:

```text
복잡한 업무를 역할별 Agent가 협업하도록 만든다.
```

---

### 25.5 5단계: Enterprise 통제 기능 추가

```text
1. Agent Gateway
2. User / Role 권한
3. Policy Guard
4. Human Approval
5. Audit Log
6. Observability
7. Evaluation
```

목표:

```text
기업 환경에서 안전하게 운영 가능한 Agent Platform을 만든다.
```

---

## 26. 권한 설계

Enterprise Agent Platform에서는 권한 설계가 중요하다.

권한은 최소한 다음 단위로 나눌 수 있다.

```text
1. 사용자 권한
2. Agent 사용 권한
3. Tool 사용 권한
4. 문서 접근 권한
5. DB 접근 권한
6. API 호출 권한
7. 승인 권한
```

예시는 다음과 같다.

| 역할 | 가능한 작업 |
|---|---|
| 일반 사용자 | 문서 검색, 요약 |
| 개발자 | RAG 검색, DB 조회, 로그 조회 |
| 아키텍트 | Agent 실행, Workflow 실행, 문서 분석 |
| 관리자 | Agent 등록, Tool 등록, 권한 설정 |
| 승인자 | 위험 작업 승인 |

권한 설계의 핵심은 다음이다.

```text
Agent가 할 수 있는 일은 사용자의 권한을 넘으면 안 된다.
```

---

## 27. Tool Risk Level

Tool은 위험도에 따라 분류해야 한다.

| 위험도 | 예시 | 처리 방식 |
|---|---|---|
| Low | 문서 검색, 파일 목록 조회 | 즉시 실행 |
| Medium | DB SELECT, 로그 조회 | 권한 확인 후 실행 |
| High | 파일 생성, 티켓 생성 | 승인 후 실행 |
| Critical | DB 수정, 파일 삭제, 배포 실행 | 강한 승인과 감사 필요 |

Tool Registry에는 위험도를 포함하는 것이 좋다.

```json
{
  "tool_id": "send_email",
  "risk_level": "high",
  "approval_required": true
}
```

---

## 28. Prompt와 Policy 관리

Enterprise 환경에서는 Prompt도 관리 대상이다.

관리해야 할 Prompt는 다음과 같다.

```text
1. System Prompt
2. Agent Role Prompt
3. Tool 사용 Prompt
4. RAG 답변 Prompt
5. Reviewer Prompt
6. 보안 정책 Prompt
7. 보고서 작성 Prompt
```

Prompt 관리 기준은 다음과 같다.

```text
1. Prompt 버전 관리
2. 변경 이력 관리
3. 승인 후 운영 반영
4. Agent별 Prompt 분리
5. 보안 정책 Prompt 고정
6. 테스트 후 배포
```

Prompt를 코드 안에 흩어놓으면 유지보수가 어렵다.

Prompt Registry 또는 Prompt Manager로 관리하는 것이 좋다.

---

## 29. 실패 처리 설계

Enterprise Agent는 실패를 전제로 설계해야 한다.

실패 유형은 다음과 같다.

```text
1. LLM 응답 실패
2. Tool 호출 실패
3. MCP Server 연결 실패
4. DB Timeout
5. 파일 없음
6. 권한 없음
7. 승인 반려
8. JSON 파싱 실패
9. Workflow 중간 실패
10. Agent 간 결과 충돌
```

대응 방식은 다음과 같다.

```text
Retry:
일시적 오류에 재시도

Fallback:
대체 Tool 또는 대체 Agent 사용

Human Review:
사람에게 판단 요청

Fail Fast:
위험한 작업은 즉시 중단

Resume:
Checkpoint에서 재개
```

Workflow Runtime과 Persistence가 있으면 실패 지점부터 재개하기 쉽다.

---

## 30. 데이터 저장소 설계

Enterprise Agent Platform에는 여러 저장소가 필요하다.

| 저장소 | 역할 |
|---|---|
| Agent Registry DB | Agent 목록과 설정 저장 |
| Tool Registry DB | Tool 목록과 권한 저장 |
| Workflow DB | Workflow 정의와 버전 저장 |
| Session Store | 대화와 실행 상태 저장 |
| Memory Store | 장기 기억 저장 |
| Vector DB | 문서 Chunk와 Embedding 저장 |
| Audit Log Store | 감사 로그 저장 |
| Trace Store | 실행 추적 정보 저장 |
| Evaluation Store | 평가 결과 저장 |

처음에는 SQLite나 JSON 파일로 시작할 수 있다.

운영 환경에서는 PostgreSQL, Redis, Object Storage, Vector DB 등을 조합할 수 있다.

---

## 31. 배포 구조

로컬 실습 구조는 다음과 같다.

```text
Python Script
  ↓
Local Ollama
  ↓
Local ChromaDB
  ↓
Local MCP Server
```

Enterprise 배포 구조는 다음과 같이 확장된다.

```text
User Browser
  ↓
Agent UI
  ↓
Agent Gateway API
  ↓
Agent Runtime Service
  ↓
Workflow Runtime
  ↓
MCP Client Layer
  ↓
MCP Server Services
  ↓
Enterprise Systems
```

컨테이너 기반으로 표현하면 다음과 같다.

```text
docker-compose
  ├─ agent-ui
  ├─ agent-gateway
  ├─ agent-runtime
  ├─ workflow-runtime
  ├─ rag-mcp-server
  ├─ db-mcp-server
  ├─ file-mcp-server
  ├─ vector-db
  └─ observability
```

---

## 32. 운영 모니터링 지표

운영 시 확인할 지표는 다음과 같다.

```text
1. 요청 수
2. Agent별 사용량
3. Tool 호출 수
4. MCP Server별 호출 수
5. 오류율
6. 평균 응답 시간
7. Token 사용량
8. 비용
9. 승인 요청 수
10. 승인 반려 수
11. RAG 검색 성공률
12. 사용자 만족도
```

이 지표가 있어야 운영 개선이 가능하다.

---

## 33. 보안 체크리스트

Enterprise Agent Platform 보안 체크리스트는 다음과 같다.

```text
1. 사용자 인증이 적용되었는가?
2. 사용자별 Agent 권한이 있는가?
3. 사용자별 Tool 권한이 있는가?
4. 문서 접근 권한이 적용되었는가?
5. DB 조회 권한이 제한되었는가?
6. 쓰기 Tool은 승인 절차가 있는가?
7. 파일 경로 접근 제한이 있는가?
8. Prompt Injection 방어가 있는가?
9. 민감정보 마스킹이 있는가?
10. 실행 로그와 감사 로그가 남는가?
11. 외부 LLM 사용 정책이 정의되었는가?
12. MCP Server 실행 권한이 제한되었는가?
13. Secret이 코드에 저장되지 않았는가?
14. 운영 장애 대응 절차가 있는가?
```

---

## 34. AI DATA Platform 기준 최소 구현 범위

처음부터 모든 기능을 구현할 필요는 없다.

AI DATA Platform 프로젝트에서 Step3 이후 최소 구현 범위는 다음 정도가 적합하다.

```text
1. Agent Gateway 역할의 FastAPI 서버
2. Agent Registry JSON 또는 SQLite
3. Tool Registry JSON 또는 SQLite
4. LangGraph 기반 Workflow Runtime
5. File / RAG / DB / API MCP Server
6. MCP Client 호출 모듈
7. Session Memory
8. 실행 로그
9. 간단한 Human Approval Mock
10. Open WebUI 또는 간단한 웹 UI 연동
```

이 정도만 구현해도 Enterprise Agent Platform의 핵심 구조를 확인할 수 있다.

---

## 35. 권장 실습 디렉터리 구조

Step3-10 실습 패키지를 만든다면 다음 구조를 추천한다.

```text
labs
└── enterprise_agent_platform
    ├── README.md
    ├── requirements.txt
    │
    ├── gateway
    │   └── app.py
    │
    ├── runtime
    │   ├── agent_runtime.py
    │   ├── workflow_runtime.py
    │   ├── policy_guard.py
    │   └── memory_manager.py
    │
    ├── registry
    │   ├── agents.json
    │   ├── tools.json
    │   └── workflows.json
    │
    ├── mcp_clients
    │   └── mcp_client_manager.py
    │
    ├── logs
    │   └── audit_log.jsonl
    │
    ├── examples
    │   ├── 01_run_agent.py
    │   ├── 02_run_workflow.py
    │   ├── 03_tool_policy_check.py
    │   └── 04_human_approval_demo.py
    │
    └── docs
        └── architecture.md
```

---

## 36. 실습 파일 역할

| 파일 | 역할 |
|---|---|
| `gateway/app.py` | Agent Gateway API 예제 |
| `agent_runtime.py` | Agent 실행 엔진 |
| `workflow_runtime.py` | Workflow 실행 엔진 |
| `policy_guard.py` | Tool 권한과 위험도 확인 |
| `memory_manager.py` | Session Memory 관리 |
| `agents.json` | Agent Registry |
| `tools.json` | Tool Registry |
| `workflows.json` | Workflow 정의 |
| `mcp_client_manager.py` | MCP Client 호출 관리 |
| `audit_log.jsonl` | 감사 로그 예제 |
| `01_run_agent.py` | Agent 실행 예제 |
| `02_run_workflow.py` | Workflow 실행 예제 |
| `03_tool_policy_check.py` | 정책 검증 예제 |
| `04_human_approval_demo.py` | 승인 흐름 예제 |

---

## 37. Enterprise Agent Platform 구현 순서

권장 구현 순서는 다음과 같다.

```text
1. Agent Registry JSON 작성
2. Tool Registry JSON 작성
3. Policy Guard 구현
4. Agent Runtime 구현
5. Workflow Runtime 구현
6. Memory Manager 구현
7. Audit Logger 구현
8. MCP Client Manager 구현
9. Gateway API 구현
10. Human Approval Mock 구현
```

처음에는 LLM을 붙이지 않아도 된다.

규칙 기반 Mock Agent로 구조를 먼저 만든 뒤 LLM을 연결하는 것이 좋다.

---

## 38. 예시: Agent Registry

```json
[
  {
    "agent_id": "rag_assistant",
    "name": "RAG 문서 검색 Agent",
    "description": "사내 문서를 검색하고 근거 기반 답변을 생성한다.",
    "allowed_tools": [
      "rag_search",
      "file_read"
    ],
    "risk_level": "low"
  },
  {
    "agent_id": "proposal_writer",
    "name": "제안서 작성 Agent",
    "description": "RFP 분석과 제안서 초안 작성을 지원한다.",
    "allowed_tools": [
      "rag_search",
      "file_read",
      "template_read"
    ],
    "risk_level": "medium"
  }
]
```

---

## 39. 예시: Tool Registry

```json
[
  {
    "tool_id": "rag_search",
    "name": "RAG 검색",
    "type": "mcp",
    "mcp_server": "rag_mcp_server",
    "operation": "read",
    "risk_level": "low",
    "approval_required": false
  },
  {
    "tool_id": "db_select",
    "name": "DB 조회",
    "type": "mcp",
    "mcp_server": "db_mcp_server",
    "operation": "read",
    "risk_level": "medium",
    "approval_required": false
  },
  {
    "tool_id": "send_email",
    "name": "메일 발송",
    "type": "mcp",
    "mcp_server": "email_mcp_server",
    "operation": "write",
    "risk_level": "high",
    "approval_required": true
  }
]
```

---

## 40. 예시: Policy Guard 로직

```python
def check_tool_permission(user_role: str, tool: dict) -> dict:
    risk_level = tool["risk_level"]
    approval_required = tool["approval_required"]

    if risk_level == "critical":
        return {
            "allowed": False,
            "reason": "Critical Tool은 현재 허용되지 않습니다."
        }

    if approval_required:
        return {
            "allowed": True,
            "approval_required": True,
            "reason": "사용자 승인 후 실행 가능합니다."
        }

    return {
        "allowed": True,
        "approval_required": False,
        "reason": "실행 가능합니다."
    }
```

이 로직은 매우 단순하지만 Policy Guard의 기본 개념을 보여준다.

---

## 41. 예시: Audit Log

```json
{
  "timestamp": "2026-06-30T16:00:00+09:00",
  "user_id": "architect001",
  "agent_id": "rag_assistant",
  "tool_id": "rag_search",
  "action": "tool_call",
  "status": "success",
  "input_summary": "query=LangGraph",
  "approval_required": false
}
```

---

## 42. Enterprise 적용 예시 1: 사내 문서 QA Agent

구조:

```text
User
  ↓
Agent Gateway
  ↓
RAG Assistant Agent
  ↓
RAG MCP Server
  ↓
Vector DB
  ↓
출처 포함 답변
```

필요 구성요소:

```text
1. RAG Assistant Agent
2. RAG MCP Server
3. Vector DB
4. 문서 접근 권한
5. 답변 출처 표시
6. 질문/답변 로그
```

---

## 43. Enterprise 적용 예시 2: 제안서 작성 Agent

구조:

```text
User
  ↓
Proposal Supervisor Agent
  ├─ Research Agent
  ├─ Analysis Agent
  ├─ Writer Agent
  └─ Reviewer Agent
  ↓
Human Review
  ↓
최종 초안
```

필요 구성요소:

```text
1. Multi Agent Orchestrator
2. RAG MCP Server
3. File MCP Server
4. Template Store
5. Review Checklist
6. Human Approval
7. Audit Log
```

---

## 44. Enterprise 적용 예시 3: 운영 점검 Agent

구조:

```text
User
  ↓
Operation Check Agent
  ├─ Docker 상태 확인
  ├─ Ollama 상태 확인
  ├─ Open WebUI 상태 확인
  ├─ ChromaDB 상태 확인
  └─ 로그 분석
  ↓
점검 보고서
```

필요 구성요소:

```text
1. API MCP Server
2. Log MCP Server
3. Workflow Runtime
4. 실패 처리
5. 알림 연동
6. 보고서 생성
```

---

## 45. Enterprise 적용 예시 4: 보안 요구사항 검토 Agent

구조:

```text
User
  ↓
Security Review Agent
  ↓
보안 정책 RAG 검색
  ↓
요구사항 분석
  ↓
위험 항목 분류
  ↓
대응 방안 작성
```

필요 구성요소:

```text
1. Security Agent
2. Policy RAG MCP Server
3. 보안 기준 문서
4. 위험도 분류 기준
5. Reviewer Agent
6. 감사 로그
```

---

## 46. 운영 전환 기준

PoC 수준의 Agent를 운영 서비스로 전환하려면 다음 조건이 필요하다.

```text
1. 사용자 인증이 적용되었다.
2. Agent별 권한이 정의되었다.
3. Tool별 권한이 정의되었다.
4. 위험 Tool 승인 절차가 있다.
5. 실행 로그가 남는다.
6. 장애 추적이 가능하다.
7. 비용과 사용량을 볼 수 있다.
8. 보안 정책이 정의되었다.
9. 문서 접근 권한이 적용되었다.
10. 관리자 화면 또는 설정 파일로 Agent를 관리할 수 있다.
```

---

## 47. 운영 조직 관점

Enterprise Agent Platform은 기술만으로 운영되지 않는다.

운영 조직과 책임도 필요하다.

| 역할 | 책임 |
|---|---|
| Platform Owner | 전체 플랫폼 방향과 운영 책임 |
| Agent Owner | 개별 Agent 품질과 변경 책임 |
| Tool Owner | Tool 기능과 보안 책임 |
| Data Owner | 문서와 데이터 접근 권한 책임 |
| Security Reviewer | 보안 정책 검토 |
| Operation Manager | 장애 대응과 모니터링 |
| Business Owner | 업무 적용 효과 검증 |

Agent가 많아질수록 소유자와 변경 절차가 중요해진다.

---

## 48. 변경 관리

Enterprise Agent는 계속 변경된다.

변경 대상은 다음과 같다.

```text
1. Prompt
2. Agent 설정
3. Tool Schema
4. MCP Server
5. Workflow
6. 정책
7. Memory
8. 모델
```

변경 관리 원칙은 다음과 같다.

```text
1. 변경 이력을 남긴다.
2. 운영 반영 전 테스트한다.
3. 위험 Tool 변경은 승인받는다.
4. Agent별 버전을 관리한다.
5. 문제가 생기면 이전 버전으로 되돌릴 수 있어야 한다.
```

---

## 49. 비용 관리

Agent는 비용이 발생한다.

비용 요소는 다음과 같다.

```text
1. LLM Token
2. Embedding
3. Vector DB
4. MCP Server 운영
5. 외부 API 호출
6. 로그 저장
7. 모니터링
8. 인프라
```

비용 관리를 위해 다음을 측정한다.

```text
Agent별 요청 수
사용자별 요청 수
Tool별 호출 수
Token 사용량
평균 응답 시간
실패 재시도 횟수
```

---

## 50. 플랫폼 성숙도 모델

Enterprise AI Agent Platform의 성숙도는 다음 단계로 볼 수 있다.

| 단계 | 설명 |
|---|---|
| Level 1 | 단일 Agent 로컬 실습 |
| Level 2 | Tool Calling과 RAG 연동 |
| Level 3 | Workflow Agent와 MCP 연동 |
| Level 4 | Multi Agent 협업 |
| Level 5 | 권한, 승인, 로그가 있는 운영 플랫폼 |
| Level 6 | 평가, 모니터링, 비용 최적화까지 포함한 Enterprise Platform |

AI DATA Platform 프로젝트는 Step3 종료 시점에 Level 3~4의 구조를 이해하고, 이후 Step4에서 Level 5~6을 목표로 확장할 수 있다.

---

## 51. Step4로 이어지는 방향

Step3은 AI Agent를 학습하는 단계이다.

Step4에서는 이를 AI Data Platform 구조로 확장할 수 있다.

예상 흐름은 다음과 같다.

```text
Step3:
Agent 구조 학습

Step4:
AI Data Platform 아키텍처 설계

Step5:
Serving / API / 운영 환경 구성

Step6:
Enterprise 적용 PoC
```

Step3-10은 Step4로 넘어가기 전 기준 아키텍처 역할을 한다.

---

## 52. 핵심 정리

이번 문서의 핵심은 다음과 같다.

```text
1. Enterprise AI Agent Platform은 Agent를 운영하기 위한 전체 체계이다.
2. 단일 Agent는 기능이고, Agent Platform은 운영 구조이다.
3. Agent Gateway는 인증, 권한, 요청 통제의 진입점이다.
4. Agent Registry는 Agent 목록과 권한을 관리한다.
5. Workflow Runtime은 Agent 실행 흐름과 상태를 제어한다.
6. MCP Layer는 외부 시스템 연동을 표준화한다.
7. Memory Store는 세션 상태, 장기 기억, 감사 이력을 관리한다.
8. Policy Guard는 위험한 Tool 실행을 통제한다.
9. Human Approval은 쓰기 작업과 고위험 작업의 안전장치이다.
10. Observability와 Audit Log는 운영과 보안 감사의 핵심이다.
```

한 문장으로 정리하면 다음과 같다.

> **Enterprise AI Agent Platform은 Agent, Workflow, Tool, MCP, Memory, 권한, 승인, 로그를 통합하여 기업 업무에서 AI Agent를 안전하게 운영하기 위한 기반 구조이다.**

---

## 53. 참고 자료

아래 자료는 Enterprise AI Agent Platform 구조를 이해하기 위한 참고 자료이다.

```text
LangGraph Overview
https://docs.langchain.com/oss/python/langgraph/overview

LangGraph Persistence
https://docs.langchain.com/oss/python/langgraph/persistence

Model Context Protocol Introduction
https://modelcontextprotocol.io/docs/getting-started/intro

Model Context Protocol Resources
https://modelcontextprotocol.io/specification/2025-06-18/server/resources

OpenAI Agents SDK
https://developers.openai.com/api/docs/guides/agents

OpenAI Agents SDK Guardrails
https://openai.github.io/openai-agents-python/guardrails/

OpenAI Agents SDK Tracing
https://openai.github.io/openai-agents-python/tracing/
```

---

## 54. 마무리

Step3-10은 Step3 전체를 Enterprise 관점으로 정리하는 문서이다.

지금까지 학습한 내용은 각각 하나의 기술 요소였다.

```text
RAG
Tool Calling
Memory
Planning
LangGraph
MCP
Multi Agent
```

하지만 실제 기업 환경에서는 이 기술 요소들이 따로 존재하지 않는다.

모든 요소가 하나의 플랫폼 안에서 연결되어야 한다.

```text
사용자 요청
   ↓
Agent Gateway
   ↓
Agent Runtime
   ↓
Workflow Runtime
   ↓
MCP Tool
   ↓
Enterprise System
   ↓
Trace / Audit / Evaluation
```

이 구조를 이해하면 이후 AI DATA Platform 프로젝트는 단순한 학습 저장소를 넘어, 실제 기업형 AI Agent 플랫폼 설계 역량을 축적하는 프로젝트로 발전할 수 있다.
