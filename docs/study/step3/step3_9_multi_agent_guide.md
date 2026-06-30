# Step3-9. Multi Agent 협업 가이드

> AI DATA Platform 연구 프로젝트  
> Step3. AI Agent  
> Part3. Enterprise AI Agent  
> 문서 경로: `docs/study/step3/step3_9_multi_agent_guide.md`  
> 작성일: 2026-06-30

---

## 1. 문서 목적

이 문서는 `Step3-8. MCP 기반 외부 시스템 연동` 이후, AI Agent를 단일 Agent 구조에서 **Multi Agent 협업 구조**로 확장하기 위한 가이드 문서이다.

앞 단계까지의 흐름은 다음과 같다.

```text
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
```

지금까지는 하나의 Agent가 사용자 요청을 받고, 필요한 Tool을 선택하고, 결과를 정리하는 구조를 중심으로 학습했다.

하지만 실제 Enterprise 업무는 하나의 Agent가 모든 일을 처리하기 어렵다.

예를 들어 다음 요청을 생각해보자.

```text
KB증권 자산성장 프로젝트 제안서 작성 방향을 검토하고,
경쟁사 벤치마킹 관점과 보안 요구사항 대응 방향을 정리해서
초안과 검토 의견을 함께 만들어줘.
```

이 요청에는 여러 역할이 필요하다.

```text
1. 요구사항 분석 담당
2. 벤치마킹 조사 담당
3. 보안 요구사항 검토 담당
4. 문서 작성 담당
5. 품질 검토 담당
6. 최종 요약 담당
```

이런 경우 하나의 Agent가 모든 역할을 수행하는 것보다, 역할별 Agent가 협업하는 구조가 더 자연스럽다.

이번 문서의 핵심은 다음 한 문장으로 요약할 수 있다.

> **Multi Agent는 복잡한 업무를 여러 전문 Agent가 역할을 나누어 처리하고, Supervisor 또는 Workflow가 전체 협업 흐름을 조율하는 구조이다.**

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
    ├─ Step3-9. Multi Agent 협업   ← 현재 문서
    └─ Step3-10. Enterprise AI Agent Platform
```

Step3-9는 Part3의 시작 문서이다.

Part2까지는 Agent의 구성요소를 개별적으로 학습했다.

```text
Planning
Workflow
LangGraph
MCP
Tool
Memory
```

Part3에서는 이 구성요소들을 묶어서 실제 기업형 Agent 구조로 확장한다.

---

## 3. 학습 목표

이 문서를 마치면 다음 내용을 설명할 수 있어야 한다.

```text
1. Multi Agent가 필요한 이유를 설명할 수 있다.
2. Single Agent와 Multi Agent의 차이를 설명할 수 있다.
3. Supervisor Agent 구조를 이해할 수 있다.
4. Router Agent 구조를 이해할 수 있다.
5. Agents-as-Tools 패턴을 이해할 수 있다.
6. Handoff 패턴을 이해할 수 있다.
7. Planner, Researcher, Writer, Reviewer Agent의 역할을 구분할 수 있다.
8. LangGraph로 Multi Agent Workflow를 설계하는 방향을 이해할 수 있다.
9. MCP Tool을 여러 Agent가 공유하는 구조를 설명할 수 있다.
10. Enterprise 환경에서 Multi Agent를 운영할 때 필요한 통제 요소를 설명할 수 있다.
```

---

## 4. Multi Agent가 필요한 이유

Single Agent는 다음 구조를 가진다.

```text
사용자 요청
   ↓
Agent
   ↓
Tool
   ↓
답변
```

이 구조는 단순한 업무에 적합하다.

예를 들어 다음 요청은 Single Agent로 충분할 수 있다.

```text
Agent 문서를 검색해줘.
12500 * 17 계산해줘.
Open WebUI 설치 절차를 요약해줘.
```

하지만 실제 업무 요청은 복잡하다.

```text
RFP를 분석하고, 요구사항을 분류하고, 제안 전략을 세우고,
초안을 작성하고, 보안 관점에서 검토하고, 최종 보고용으로 정리해줘.
```

이런 요청은 다음과 같은 이유로 Single Agent에 부담이 크다.

```text
1. 처리해야 할 업무 범위가 넓다.
2. 필요한 전문성이 다르다.
3. 중간 결과가 많다.
4. 검토와 작성이 동시에 필요하다.
5. 오류 발생 시 원인 추적이 어렵다.
6. 프롬프트가 길어지고 역할이 불명확해진다.
7. 하나의 Agent가 너무 많은 Tool을 갖게 된다.
```

Multi Agent는 이 문제를 역할 분리로 해결한다.

```text
Planner Agent:
전체 작업을 계획한다.

Research Agent:
문서와 자료를 검색한다.

Analysis Agent:
요구사항과 쟁점을 분석한다.

Writer Agent:
문서 초안을 작성한다.

Reviewer Agent:
품질과 오류를 검토한다.

Supervisor Agent:
전체 흐름을 조율한다.
```

---

## 5. Single Agent와 Multi Agent 비교

| 구분 | Single Agent | Multi Agent |
|---|---|---|
| 구조 | 하나의 Agent가 모든 역할 수행 | 여러 Agent가 역할 분담 |
| 장점 | 단순하고 구현이 쉽다 | 전문성과 확장성이 높다 |
| 단점 | 복잡한 업무에서 역할이 혼재됨 | 오케스트레이션이 필요함 |
| Tool 관리 | 한 Agent에 Tool 집중 | Agent별 Tool 분리 가능 |
| 프롬프트 | 길고 복잡해질 수 있음 | 역할별로 명확하게 분리 가능 |
| 검토 구조 | 자기 검토에 의존 | Reviewer Agent 분리 가능 |
| 운영 통제 | 단순 | 권한, 로그, 상태 관리 필요 |
| 적합한 업무 | 단순 질의, 단일 Tool 작업 | 보고서, 분석, 제안서, 점검, 검토 |

Multi Agent가 항상 좋은 것은 아니다.

작업이 단순하면 Single Agent가 더 적합하다.

```text
단순 요청:
Single Agent

복잡한 분석 / 작성 / 검토 / 협업:
Multi Agent
```

---

## 6. Multi Agent의 기본 구성

Multi Agent 시스템은 일반적으로 다음 구성요소를 가진다.

```text
1. Supervisor
2. Worker Agents
3. Shared State
4. Shared Tools
5. Message Passing
6. Memory
7. Workflow
8. Policy Guard
```

구조는 다음과 같다.

```text
사용자
  ↓
Supervisor Agent
  ↓
작업 분배
  ├─ Research Agent
  ├─ Analysis Agent
  ├─ Writer Agent
  └─ Reviewer Agent
  ↓
결과 취합
  ↓
최종 답변
```

조금 더 상세히 표현하면 다음과 같다.

```text
User Request
    │
    ▼
Supervisor
    │
    ├─ Plan
    ├─ Route
    ├─ Delegate
    ├─ Collect
    └─ Synthesize
        │
        ├─ Research Agent
        ├─ Analysis Agent
        ├─ Writer Agent
        └─ Review Agent
```

---

## 7. Supervisor Agent

Supervisor Agent는 Multi Agent 시스템의 관리자 역할을 한다.

역할은 다음과 같다.

```text
1. 사용자 요청을 분석한다.
2. 어떤 Agent가 필요한지 판단한다.
3. 작업 순서를 정한다.
4. 각 Agent에게 작업을 위임한다.
5. 중간 결과를 수집한다.
6. 부족한 결과를 다시 요청한다.
7. 최종 답변을 통합한다.
```

Supervisor는 사람이 프로젝트 매니저 역할을 하는 것과 비슷하다.

```text
PM:
업무를 나누고 담당자에게 지시하고 결과를 취합한다.

Supervisor Agent:
작업을 나누고 전문 Agent에게 위임하고 결과를 종합한다.
```

Supervisor 구조는 Enterprise 업무에 적합하다.

예를 들어 제안서 작성 업무에서는 다음과 같이 동작할 수 있다.

```text
Supervisor:
RFP 분석은 Analysis Agent에게 맡긴다.
경쟁사 조사 관점은 Research Agent에게 맡긴다.
초안 작성은 Writer Agent에게 맡긴다.
품질 검토는 Reviewer Agent에게 맡긴다.
마지막 답변은 Supervisor가 통합한다.
```

---

## 8. Worker Agent

Worker Agent는 특정 역할에 특화된 Agent이다.

대표적인 Worker Agent는 다음과 같다.

```text
1. Planner Agent
2. Research Agent
3. Analysis Agent
4. Writer Agent
5. Reviewer Agent
6. Tool Agent
7. QA Agent
```

각 Agent는 자신의 역할에 맞는 Prompt와 Tool을 가진다.

예를 들어 Research Agent는 검색 Tool에 강하다.

```text
Research Agent
- RAG 검색 Tool
- Web 검색 Tool
- 파일 읽기 Tool
- 문서 요약 Prompt
```

Writer Agent는 작성에 집중한다.

```text
Writer Agent
- 문서 작성 Prompt
- 톤 조정 Prompt
- Markdown 작성 규칙
- 보고서 구조 템플릿
```

Reviewer Agent는 검토에 집중한다.

```text
Reviewer Agent
- 누락 항목 검토
- 논리 오류 검토
- 보안 위험 검토
- 출처 부족 검토
```

Agent별로 역할을 분리하면 Prompt가 명확해지고 품질 관리가 쉬워진다.

---

## 9. 대표 Agent 역할 예시

| Agent | 역할 | 주요 Tool |
|---|---|---|
| Supervisor Agent | 전체 작업 조율 | Agent 호출, 상태 관리 |
| Planner Agent | 작업 계획 수립 | 없음 또는 Workflow Tool |
| Research Agent | 자료 검색 | RAG, File, Web, DB |
| Analysis Agent | 요구사항 분석 | RAG, DB, 비교 분석 |
| Writer Agent | 초안 작성 | 문서 템플릿, LLM |
| Reviewer Agent | 품질 검토 | 체크리스트, 정책 Tool |
| Security Agent | 보안 검토 | 보안 기준, 정책 검색 |
| Data Agent | 데이터 조회 | DB, API, SQL Tool |
| Report Agent | 보고서 생성 | Markdown, DOCX, PPT Tool |

---

## 10. Multi Agent 협업 패턴

Multi Agent에는 여러 협업 패턴이 있다.

대표적인 패턴은 다음과 같다.

```text
1. Supervisor Pattern
2. Router Pattern
3. Agents-as-Tools Pattern
4. Handoff Pattern
5. Debate Pattern
6. Pipeline Pattern
7. Hierarchical Pattern
```

이번 문서에서는 Enterprise 업무에 가장 많이 쓰이는 네 가지를 중심으로 설명한다.

```text
Supervisor
Router
Agents-as-Tools
Handoff
```

---

## 11. Supervisor Pattern

Supervisor Pattern은 중앙 Supervisor가 여러 Agent를 통제하는 구조이다.

```text
User
 ↓
Supervisor
 ├─ Research Agent
 ├─ Analysis Agent
 ├─ Writer Agent
 └─ Reviewer Agent
 ↓
Final Answer
```

장점은 다음과 같다.

```text
1. 전체 흐름을 통제하기 쉽다.
2. 중간 결과를 Supervisor가 검토할 수 있다.
3. 작업 순서를 명확히 정할 수 있다.
4. Enterprise 업무 절차와 잘 맞는다.
```

단점은 다음과 같다.

```text
1. Supervisor가 복잡해질 수 있다.
2. Supervisor의 판단 오류가 전체 결과에 영향을 준다.
3. 모든 협업이 중앙 집중 구조가 된다.
```

적합한 업무는 다음과 같다.

```text
제안서 작성
보고서 작성
장애 보고
문서 품질 검토
요구사항 분석
```

---

## 12. Router Pattern

Router Pattern은 사용자 요청을 보고 어떤 Agent에게 보낼지 결정하는 구조이다.

```text
User Request
     ↓
Router
 ├─ RAG Agent
 ├─ DB Agent
 ├─ Report Agent
 └─ Security Agent
```

예를 들어 다음과 같이 라우팅할 수 있다.

```text
문서 관련 질문:
RAG Agent

DB 통계 질문:
Data Agent

보고서 작성 요청:
Writer Agent

보안 검토 요청:
Security Agent
```

Router Pattern은 요청 유형이 명확히 나뉘는 서비스에 적합하다.

장점은 다음과 같다.

```text
1. 구조가 단순하다.
2. 요청 유형별 Agent 분리가 쉽다.
3. 확장하기 좋다.
```

단점은 다음과 같다.

```text
1. 복합 요청에는 부족할 수 있다.
2. 한 번 라우팅 후 Agent 간 협업이 제한적일 수 있다.
```

---

## 13. Agents-as-Tools Pattern

Agents-as-Tools는 한 Agent가 다른 Agent를 Tool처럼 호출하는 구조이다.

OpenAI Agents SDK 문서에서는 이와 유사한 방식으로 메인 Agent가 specialist agent를 helper처럼 호출하는 패턴을 설명한다. 또한 Handoff는 한 Agent가 작업을 다른 Agent에게 위임하는 구조로 설명된다.

개념적으로 표현하면 다음과 같다.

```text
Main Agent
  ├─ call Research Agent
  ├─ call Writer Agent
  └─ call Reviewer Agent
```

이 구조에서 메인 Agent는 최종 답변 책임을 유지한다.

```text
Research Agent:
자료를 찾아 결과만 반환

Writer Agent:
초안을 작성해서 반환

Reviewer Agent:
검토 의견을 반환

Main Agent:
모든 결과를 종합해서 최종 답변 생성
```

이 패턴은 Supervisor Pattern과 유사하지만, 각 Agent를 Tool처럼 호출한다는 점이 특징이다.

장점은 다음과 같다.

```text
1. 기존 Tool Calling 구조와 연결하기 쉽다.
2. Agent별 역할을 함수처럼 사용할 수 있다.
3. 최종 답변 책임이 Main Agent에 남는다.
```

---

## 14. Handoff Pattern

Handoff Pattern은 한 Agent가 다른 Agent에게 대화나 작업의 주도권을 넘기는 구조이다.

```text
User
 ↓
General Agent
 ↓
필요 시 Handoff
 ↓
Specialist Agent
```

예를 들어 고객지원 업무에서는 다음과 같이 동작할 수 있다.

```text
General Support Agent
  ↓
환불 요청 감지
  ↓
Refund Agent로 Handoff
```

OpenAI Agents SDK의 Handoff 개념도 서로 다른 전문 Agent에게 작업을 위임하는 데 유용한 패턴으로 설명된다.

Handoff Pattern은 다음 경우에 적합하다.

```text
1. 전문 Agent가 이후 대화를 계속 이어가야 할 때
2. 특정 도메인의 깊은 처리가 필요할 때
3. 사용자가 전문 상담 흐름으로 이동해야 할 때
```

단점은 다음과 같다.

```text
1. 주도권이 바뀌므로 상태 관리가 중요하다.
2. 다시 원래 Agent로 돌아오는 흐름을 설계해야 한다.
3. 무한 Handoff가 발생하지 않도록 제한해야 한다.
```

---

## 15. Pipeline Pattern

Pipeline Pattern은 Agent들이 정해진 순서대로 작업을 수행하는 구조이다.

```text
Planner
  ↓
Researcher
  ↓
Analyst
  ↓
Writer
  ↓
Reviewer
  ↓
Final Answer
```

이 구조는 Step3-5의 Workflow와 유사하다.

차이는 각 단계가 단순 함수가 아니라 Agent라는 점이다.

Pipeline Pattern은 다음 업무에 적합하다.

```text
1. 보고서 작성
2. 문서 요약
3. 품질 검토
4. 제안서 초안 작성
5. 데이터 분석 보고서
```

장점은 다음과 같다.

```text
1. 흐름이 명확하다.
2. 단계별 산출물을 관리하기 쉽다.
3. 중간 검토를 넣기 좋다.
```

단점은 다음과 같다.

```text
1. 유연성이 낮을 수 있다.
2. 앞 단계 오류가 뒤 단계에 영향을 준다.
```

---

## 16. Debate Pattern

Debate Pattern은 여러 Agent가 서로 다른 관점에서 의견을 내고, 최종 Agent가 판단하는 구조이다.

```text
Question
  ↓
Agent A 의견
Agent B 의견
Agent C 의견
  ↓
Judge Agent
  ↓
Final Answer
```

예를 들어 아키텍처 검토에서는 다음과 같이 사용할 수 있다.

```text
Performance Agent:
성능 관점 검토

Security Agent:
보안 관점 검토

Operation Agent:
운영 관점 검토

Judge Agent:
종합 판단
```

장점은 다음과 같다.

```text
1. 다양한 관점을 반영할 수 있다.
2. 검토 품질을 높일 수 있다.
3. 리스크 분석에 유용하다.
```

단점은 다음과 같다.

```text
1. 비용과 시간이 증가한다.
2. 의견 충돌을 조정하는 기준이 필요하다.
3. 최종 판단 Agent의 품질이 중요하다.
```

---

## 17. Hierarchical Pattern

Hierarchical Pattern은 Supervisor가 여러 하위 Supervisor 또는 Agent를 관리하는 구조이다.

```text
Top Supervisor
   ├─ Proposal Supervisor
   │   ├─ Research Agent
   │   └─ Writer Agent
   │
   ├─ Security Supervisor
   │   ├─ Policy Agent
   │   └─ Risk Agent
   │
   └─ Data Supervisor
       ├─ DB Agent
       └─ API Agent
```

이 구조는 대규모 Enterprise Agent Platform에서 사용할 수 있다.

하지만 처음부터 이 구조로 가면 복잡해지므로, Step3-9에서는 개념만 이해하고 Step3-10에서 플랫폼 관점으로 확장한다.

---

## 18. Enterprise Multi Agent 예시: 제안서 작성

제안서 작성 업무를 Multi Agent로 나누면 다음과 같다.

```text
Supervisor Agent
  ↓
Planner Agent:
작성 계획 수립

Research Agent:
RFP / 기존 문서 / 벤치마킹 자료 검색

Analysis Agent:
요구사항 분석 및 핵심 쟁점 정리

Writer Agent:
제안서 초안 작성

Reviewer Agent:
누락, 표현, 논리, 품질 검토

Security Agent:
보안 요구사항 대응 검토

Supervisor Agent:
최종 결과 통합
```

Workflow는 다음과 같다.

```text
START
  ↓
Supervisor
  ↓
Planner
  ↓
Researcher
  ↓
Analyst
  ↓
Writer
  ↓
Reviewer
  ↓
Security Reviewer
  ↓
Supervisor Final
  ↓
END
```

이 구조는 사용자의 실제 업무와 유사하다.

---

## 19. Enterprise Multi Agent 예시: RAG 품질 점검

RAG 품질 점검을 Multi Agent로 나누면 다음과 같다.

```text
RAG Inspector Agent:
Vector DB와 Collection 상태 확인

Document Agent:
문서 Chunk 품질 확인

Search Agent:
검색 테스트 수행

Answer Agent:
LLM 답변 품질 확인

Evaluation Agent:
정답성, 출처, 누락 여부 평가

Supervisor:
최종 점검 보고서 작성
```

이 구조는 AI DATA Platform 프로젝트의 RAG 운영 점검에 활용할 수 있다.

---

## 20. Enterprise Multi Agent 예시: 운영 점검

운영 점검 Agent는 다음과 같이 구성할 수 있다.

```text
Supervisor Agent
  ├─ Docker Agent
  ├─ Ollama Agent
  ├─ Open WebUI Agent
  ├─ ChromaDB Agent
  ├─ Log Analysis Agent
  └─ Report Agent
```

각 Agent의 역할은 다음과 같다.

```text
Docker Agent:
컨테이너 상태 확인

Ollama Agent:
모델 목록과 서버 상태 확인

Open WebUI Agent:
서비스 응답 확인

ChromaDB Agent:
Vector DB 상태 확인

Log Analysis Agent:
오류 로그 분석

Report Agent:
점검 결과 보고서 작성
```

---

## 21. Multi Agent와 LangGraph

LangGraph는 Multi Agent Workflow를 구현하기에 적합하다.

Step3-6에서 학습한 개념을 다시 보면 다음과 같다.

```text
State:
전체 협업 상태

Node:
각 Agent 실행 단위

Edge:
Agent 간 실행 순서

Conditional Edge:
결과에 따라 다음 Agent 선택
```

Multi Agent를 LangGraph로 표현하면 다음과 같다.

```text
START
  ↓
supervisor_node
  ↓
route_next_agent
  ├─ research_agent_node
  ├─ analysis_agent_node
  ├─ writer_agent_node
  └─ reviewer_agent_node
  ↓
supervisor_node
  ↓
END
```

Agent 하나가 LangGraph의 Node가 될 수 있다.

```text
Research Agent Node
Analysis Agent Node
Writer Agent Node
Reviewer Agent Node
```

이렇게 하면 Agent 협업 흐름을 Graph로 제어할 수 있다.

---

## 22. Multi Agent State 설계

Multi Agent에서는 State 설계가 매우 중요하다.

예시 State는 다음과 같다.

```json
{
  "user_request": "제안서 작성 방향을 정리해줘.",
  "plan": [],
  "current_agent": "research",
  "research_result": null,
  "analysis_result": null,
  "draft": null,
  "review_result": null,
  "final_answer": null,
  "errors": []
}
```

Agent별 결과를 구분해서 저장해야 한다.

```text
research_result:
Research Agent 결과

analysis_result:
Analysis Agent 결과

draft:
Writer Agent 결과

review_result:
Reviewer Agent 결과

final_answer:
Supervisor가 통합한 최종 답변
```

State를 잘 설계하면 다음이 가능하다.

```text
1. Agent별 실행 결과 추적
2. 실패 Agent만 재실행
3. 중간 결과 검토
4. 최종 보고서 생성
5. 실행 로그 기록
```

---

## 23. Agent 간 메시지 전달

Multi Agent에서 Agent 간 메시지를 어떻게 전달할지도 중요하다.

단순한 방식은 Shared State를 사용하는 것이다.

```text
Research Agent
  ↓
research_result에 저장

Analysis Agent
  ↓
research_result를 읽고 analysis_result 생성

Writer Agent
  ↓
analysis_result를 읽고 draft 생성
```

또 다른 방식은 Message List를 사용하는 것이다.

```json
{
  "messages": [
    {
      "agent": "research",
      "content": "검색 결과 ..."
    },
    {
      "agent": "analysis",
      "content": "분석 결과 ..."
    }
  ]
}
```

Enterprise 환경에서는 둘을 함께 사용할 수 있다.

```text
Shared State:
구조화된 결과 저장

Message Log:
Agent 간 대화와 판단 이력 저장
```

---

## 24. Multi Agent와 MCP

Step3-8에서 MCP를 학습했다.

Multi Agent 환경에서는 여러 Agent가 같은 MCP Tool을 공유할 수 있다.

```text
Research Agent ─┐
Analysis Agent ─┼─ MCP Client Layer → MCP Server
Data Agent     ─┘
```

예를 들어 다음 MCP Server가 있다고 하자.

```text
File MCP Server
RAG MCP Server
DB MCP Server
API MCP Server
```

Agent별 사용 예시는 다음과 같다.

```text
Research Agent:
RAG MCP Server, File MCP Server 사용

Data Agent:
DB MCP Server, API MCP Server 사용

Security Agent:
Policy RAG MCP Server 사용

Report Agent:
File MCP Server의 문서 템플릿 사용
```

MCP를 사용하면 Agent마다 외부 시스템 연동 코드를 따로 만들 필요가 줄어든다.

---

## 25. Multi Agent와 Memory

Multi Agent에는 두 종류의 Memory가 필요하다.

```text
1. Agent 개별 Memory
2. Shared Memory
```

Agent 개별 Memory는 특정 Agent의 역할 수행 이력을 저장한다.

```text
Research Agent:
이전에 검색한 문서, 검색어, 출처

Writer Agent:
사용자 선호 문체, 보고서 형식

Reviewer Agent:
자주 발견되는 오류 패턴
```

Shared Memory는 모든 Agent가 함께 참고하는 공통 기억이다.

```text
프로젝트 목적
사용자 요청
전체 계획
중간 결과
최종 결정사항
```

Enterprise 환경에서는 Memory를 다음과 같이 분리하는 것이 좋다.

```text
Session Memory:
현재 작업 중의 상태

Long-term Memory:
반복적으로 사용할 수 있는 지식

Audit Memory:
실행 이력과 판단 근거
```

---

## 26. Multi Agent의 위험 요소

Multi Agent는 강력하지만 위험도 있다.

대표적인 위험은 다음과 같다.

```text
1. Agent 간 책임이 불명확해진다.
2. 같은 작업을 중복 수행할 수 있다.
3. Agent 간 결과가 충돌할 수 있다.
4. 비용과 실행 시간이 증가한다.
5. 무한 Handoff 또는 무한 Loop가 발생할 수 있다.
6. 한 Agent의 오류가 전체 결과로 전파될 수 있다.
7. Tool 권한이 과도하게 부여될 수 있다.
8. 최종 책임 Agent가 불명확할 수 있다.
```

따라서 Multi Agent는 반드시 통제 구조와 함께 설계해야 한다.

---

## 27. Enterprise Multi Agent 설계 원칙

Enterprise 환경에서는 다음 원칙을 권장한다.

```text
1. Agent 역할을 명확히 정의한다.
2. 각 Agent가 사용할 Tool을 제한한다.
3. 최종 답변 책임자를 명확히 둔다.
4. Supervisor 또는 Workflow Engine을 둔다.
5. Shared State 구조를 명확히 정의한다.
6. Agent 간 메시지 로그를 남긴다.
7. 중요 작업은 Human Review를 거친다.
8. Handoff 횟수와 Loop 횟수를 제한한다.
9. 실행 비용과 시간을 모니터링한다.
10. 실패 시 중단 또는 재시도 정책을 정의한다.
```

가장 중요한 원칙은 다음이다.

> **Multi Agent는 Agent를 많이 만드는 것이 아니라, 역할과 책임을 명확히 나누는 것이다.**

---

## 28. Multi Agent 설계 체크리스트

Multi Agent를 설계할 때 다음 질문을 먼저 확인한다.

```text
1. 이 업무가 정말 Multi Agent가 필요한가?
2. Single Agent + Tool 구조로 충분하지 않은가?
3. Agent별 역할은 명확한가?
4. 각 Agent의 입력과 출력은 무엇인가?
5. 누가 최종 답변을 책임지는가?
6. Agent 간 결과 충돌은 누가 조정하는가?
7. 어떤 Tool을 어떤 Agent가 사용할 수 있는가?
8. 공유 State에는 무엇을 저장할 것인가?
9. 실행 로그와 감사 이력은 어떻게 남길 것인가?
10. 실패하면 어떻게 복구할 것인가?
```

---

## 29. 실습 목표

이번 Step3-9 실습은 완전한 Multi Agent Platform을 만드는 것이 아니다.

목표는 다음 구조를 이해하는 것이다.

```text
1. Supervisor Agent가 사용자 요청을 받는다.
2. Supervisor가 작업을 여러 Agent에게 분배한다.
3. 각 Agent가 자신의 역할에 맞는 결과를 만든다.
4. Supervisor가 결과를 취합한다.
5. 최종 답변을 생성한다.
```

처음 실습에서는 실제 LLM을 연결하지 않고 규칙 기반 Agent로 시작하는 것을 권장한다.

이유는 다음과 같다.

```text
1. Multi Agent 구조 자체를 이해하기 쉽다.
2. LLM 응답 품질 문제와 구조 문제를 분리할 수 있다.
3. 디버깅이 쉽다.
4. 이후 LangGraph와 MCP를 붙이기 쉽다.
```

---

## 30. 권장 실습 디렉터리 구조

이번 실습은 다음 구조를 추천한다.

```text
labs
└── multi_agent
    ├── README.md
    ├── 01_supervisor_demo.py
    ├── 02_router_agent.py
    ├── 03_agents_as_tools.py
    ├── 04_pipeline_multi_agent.py
    ├── 05_multi_agent_with_mcp.py
    │
    ├── agents
    │   ├── __init__.py
    │   ├── supervisor_agent.py
    │   ├── planner_agent.py
    │   ├── research_agent.py
    │   ├── analysis_agent.py
    │   ├── writer_agent.py
    │   └── reviewer_agent.py
    │
    ├── common
    │   ├── __init__.py
    │   ├── state.py
    │   └── message.py
    │
    └── sample_data
        ├── proposal_request.md
        └── review_checklist.md
```

---

## 31. 실습 파일 역할

| 파일 | 역할 |
|---|---|
| `01_supervisor_demo.py` | Supervisor가 여러 Agent를 호출하는 기본 예제 |
| `02_router_agent.py` | 요청 유형에 따라 Agent를 선택하는 예제 |
| `03_agents_as_tools.py` | Agent를 Tool처럼 호출하는 예제 |
| `04_pipeline_multi_agent.py` | Planner → Research → Writer → Reviewer 순차 실행 |
| `05_multi_agent_with_mcp.py` | MCP Tool을 여러 Agent가 공유하는 확장 예제 |
| `supervisor_agent.py` | 전체 흐름 조율 |
| `planner_agent.py` | 작업 계획 생성 |
| `research_agent.py` | 자료 검색 |
| `analysis_agent.py` | 분석 결과 생성 |
| `writer_agent.py` | 초안 작성 |
| `reviewer_agent.py` | 품질 검토 |

---

## 32. 규칙 기반 Multi Agent 예시

간단한 Agent 함수는 다음처럼 만들 수 있다.

```python
def planner_agent(user_request: str) -> dict:
    return {
        "agent": "planner",
        "result": [
            "요구사항 분석",
            "자료 조사",
            "초안 작성",
            "검토"
        ]
    }


def research_agent(user_request: str) -> dict:
    return {
        "agent": "research",
        "result": "관련 자료를 검색하고 핵심 내용을 정리했습니다."
    }


def writer_agent(research_result: str) -> dict:
    return {
        "agent": "writer",
        "result": f"초안 작성 결과: {research_result}"
    }


def reviewer_agent(draft: str) -> dict:
    return {
        "agent": "reviewer",
        "result": "검토 결과: 초안의 논리 구조와 출처 표시를 보완해야 합니다."
    }
```

Supervisor는 이 Agent들을 순서대로 호출한다.

```python
def supervisor(user_request: str) -> dict:
    plan = planner_agent(user_request)
    research = research_agent(user_request)
    draft = writer_agent(research["result"])
    review = reviewer_agent(draft["result"])

    return {
        "plan": plan,
        "research": research,
        "draft": draft,
        "review": review,
        "final_answer": "Multi Agent 협업 결과를 종합했습니다."
    }
```

이 예제는 단순하지만 Multi Agent의 핵심 구조를 보여준다.

---

## 33. LangGraph 기반 Multi Agent 방향

규칙 기반 실습이 끝나면 LangGraph로 확장한다.

LangGraph 구조는 다음과 같다.

```text
START
  ↓
planner_node
  ↓
research_node
  ↓
analysis_node
  ↓
writer_node
  ↓
reviewer_node
  ↓
supervisor_final_node
  ↓
END
```

각 Node는 하나의 Agent를 실행한다.

```text
planner_node:
Planner Agent 실행

research_node:
Research Agent 실행

writer_node:
Writer Agent 실행

reviewer_node:
Reviewer Agent 실행
```

Conditional Edge를 사용하면 Reviewer 결과에 따라 다시 Writer로 되돌릴 수 있다.

```text
reviewer_node
  ↓
수정 필요?
  ├─ yes → writer_node
  └─ no  → supervisor_final_node
```

---

## 34. Multi Agent와 Human Review

Enterprise 환경에서는 Multi Agent 결과를 바로 실행하거나 제출하면 위험하다.

특히 다음 작업은 Human Review가 필요하다.

```text
1. 제안서 최종 제출
2. 고객사 메일 발송
3. DB 수정
4. 파일 삭제
5. 운영 배포
6. 보안 정책 변경
```

Multi Agent Workflow에 Human Review를 넣으면 다음 구조가 된다.

```text
Writer Agent
  ↓
Reviewer Agent
  ↓
Human Review
  ↓
승인?
  ├─ yes → Final
  └─ no  → Writer Agent 재작성
```

이 구조는 Step3-10 Enterprise AI Agent Platform에서 더 상세히 다룬다.

---

## 35. Multi Agent와 평가

Multi Agent의 품질은 다음 기준으로 평가할 수 있다.

```text
1. 역할 분리가 명확한가?
2. Agent별 출력 품질이 좋은가?
3. 중간 결과가 최종 답변에 잘 반영되었는가?
4. Agent 간 충돌이 해결되었는가?
5. 불필요한 반복이 없는가?
6. 비용과 시간이 적절한가?
7. 출처가 명확한가?
8. 보안 정책을 위반하지 않는가?
```

평가 Agent를 별도로 두는 것도 좋은 방법이다.

```text
Evaluation Agent:
최종 결과의 정확성, 출처, 누락, 표현 품질을 평가한다.
```

---

## 36. 실무 적용 우선순위

AI DATA Platform 프로젝트에서는 다음 순서로 Multi Agent를 적용하는 것을 추천한다.

```text
1. 문서 작성 보조 Multi Agent
2. RAG 품질 점검 Multi Agent
3. 운영 상태 점검 Multi Agent
4. 제안서 검토 Multi Agent
5. 보안 요구사항 검토 Multi Agent
6. 외부 시스템 연동 Multi Agent
```

처음부터 모든 업무에 Multi Agent를 적용하지 않는다.

반복적이고 역할 분리가 명확한 업무부터 적용한다.

---

## 37. 구현 시 주의사항

구현 시 주의할 점은 다음과 같다.

```text
1. Agent를 너무 많이 만들지 않는다.
2. Agent 이름과 역할을 명확히 한다.
3. Agent별 입력과 출력 Schema를 정의한다.
4. Shared State를 단순하게 유지한다.
5. Supervisor가 최종 책임을 갖도록 한다.
6. Tool 권한을 Agent별로 제한한다.
7. Loop 횟수를 제한한다.
8. 비용과 실행 시간을 기록한다.
9. 실패 시 안전하게 중단한다.
10. 사용자 승인 지점을 명확히 둔다.
```

---

## 38. Step3-10으로 이어지는 구조

Step3-9는 Multi Agent 협업 구조를 이해하는 단계이다.

Step3-10에서는 이 구조를 Enterprise AI Agent Platform으로 확장한다.

Step3-10에서 다룰 내용은 다음과 같다.

```text
1. Agent Gateway
2. Agent Registry
3. Tool Registry
4. MCP Client Layer
5. Workflow Runtime
6. Memory Store
7. Policy Guard
8. Human Approval
9. Observability
10. Audit Log
```

Step3-9에서 Agent 간 협업 구조를 이해했다면, Step3-10에서는 이를 운영 가능한 플랫폼 구조로 정리한다.

---

## 39. 핵심 정리

이번 문서의 핵심은 다음과 같다.

```text
1. Multi Agent는 복잡한 업무를 여러 전문 Agent가 나누어 처리하는 구조이다.
2. Supervisor Agent는 전체 작업을 조율하고 결과를 통합한다.
3. Worker Agent는 각자의 전문 역할을 수행한다.
4. 대표 패턴에는 Supervisor, Router, Agents-as-Tools, Handoff, Pipeline이 있다.
5. LangGraph는 Multi Agent Workflow를 Graph로 제어하는 데 적합하다.
6. MCP는 여러 Agent가 외부 Tool을 공유하게 해준다.
7. Multi Agent에서는 Shared State와 Message Log가 중요하다.
8. Enterprise 환경에서는 역할, 권한, 로그, 승인, 실패 처리가 중요하다.
9. Multi Agent는 Agent를 많이 만드는 것이 아니라 역할과 책임을 명확히 나누는 것이다.
10. Step3-10에서는 Multi Agent를 Enterprise Agent Platform 구조로 확장한다.
```

한 문장으로 정리하면 다음과 같다.

> **Multi Agent 협업의 핵심은 여러 Agent를 많이 만드는 것이 아니라, 복잡한 업무를 명확한 역할과 책임으로 나누고 Supervisor 또는 Workflow가 통제하는 것이다.**

---

## 40. 참고 자료

아래 자료는 Multi Agent 구조를 이해하기 위한 참고 자료이다.

```text
LangChain Multi-agent documentation
https://docs.langchain.com/oss/python/langchain/multi-agent

LangGraph Supervisor
https://reference.langchain.com/python/langgraph-supervisor

OpenAI Agents SDK
https://openai.github.io/openai-agents-python/

OpenAI Agents SDK - Handoffs
https://openai.github.io/openai-agents-python/handoffs/

OpenAI Agents SDK - Orchestration
https://developers.openai.com/api/docs/guides/agents/orchestration

CrewAI Documentation
https://docs.crewai.com/
```

---

## 41. 마무리

Step3-9는 AI Agent가 단일 실행 주체에서 협업 구조로 확장되는 단계이다.

지금까지는 하나의 Agent가 Tool을 호출하고 Workflow를 수행하는 구조를 학습했다.

이제부터는 여러 Agent가 각자의 전문 역할을 수행하고, Supervisor 또는 Workflow가 전체 흐름을 조율한다.

이 구조는 실제 기업 업무와 유사하다.

```text
PM
  ↓
분석 담당
자료 조사 담당
작성 담당
검토 담당
보안 담당
```

Multi Agent는 이 업무 구조를 AI 시스템으로 옮기는 방식이다.

다음 Step3-10에서는 이 Multi Agent 구조를 실제 운영 가능한 Enterprise AI Agent Platform으로 확장한다.
