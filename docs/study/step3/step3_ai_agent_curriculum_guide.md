# Step3. AI Agent 연구학습 가이드

> AI DATA Platform 연구 프로젝트  
> Step3. AI Agent 학습 과정 설계 문서  
> 작성일: 2026-06-29

---

## 1. 문서 목적

이 문서는 AI DATA Platform 연구 프로젝트의 **Step3. AI Agent 학습 과정**을 정의하기 위한 가이드 문서이다.

Step1에서는 Local LLM 실행 환경을 구축했고, Step2에서는 RAG 기반 문서 검색과 LLM 연계를 실습했다.  
Step3부터는 LLM이 단순히 답변을 생성하는 수준을 넘어, **목표를 이해하고, 필요한 도구를 선택하고, 실행 결과를 바탕으로 다음 행동을 결정하는 AI Agent 구조**를 학습한다.

이번 Step3의 목표는 단순한 예제 구현이 아니다.  
최종적으로는 사내 시스템, 문서 저장소, 데이터베이스, 업무 API, 파일 시스템, RAG, MCP, Workflow, Multi Agent를 연결할 수 있는 **Enterprise AI Agent Platform 아키텍처**를 이해하고 직접 설계할 수 있는 수준까지 가는 것이다.

---

## 2. Step3 학습 방향

Step3는 다음 세 가지 관점을 함께 다룬다.

```text
1. 개념 이해
   - Agent가 왜 필요한가?
   - ReAct, Planning, Tool Calling, Memory는 어떤 문제를 해결하는가?

2. Python 실습
   - 단일 Agent 구현
   - Tool Calling 구현
   - Memory 구현
   - Workflow 기반 Agent 구현
   - MCP Client/Server 연동 실습

3. Enterprise 아키텍처
   - 사내 시스템 연동
   - 보안과 권한
   - Agent Gateway
   - MCP 기반 도구 표준화
   - Multi Agent 협업 구조
```

기존 RAG 단계가 **문서를 찾아 답변하는 AI**를 만드는 과정이었다면, Step3는 **업무를 수행하는 AI**를 만드는 과정이다.

---

## 3. Step3 전체 목차

아래 목차는 MkDocs의 `nav` 구조에 반영할 수 있도록 설계한다.

```yaml
- Step3. AI Agent:
    - Part1. AI Agent 기초:

        - Step3-1. AI Agent 개요:
            study/step3/step3_1_ai_agent_overview_guide.md

        - Step3-2. ReAct와 Tool Calling:
            study/step3/step3_2_react_and_tool_calling_guide.md

        - Step3-3. 첫 번째 AI Agent 구현:
            study/step3/step3_3_first_ai_agent_guide.md

        - Step3-4. Agent Memory와 상태 관리:
            study/step3/step3_4_agent_memory_guide.md

    - Part2. AI Agent 심화:

        - Step3-5. Workflow Agent(LangGraph):
            study/step3/step3_5_langgraph_workflow_agent_guide.md

        - Step3-6. MCP 아키텍처 이해:
            study/step3/step3_6_mcp_architecture_guide.md

        - Step3-7. MCP 기반 외부 시스템 연동:
            study/step3/step3_7_mcp_practice_guide.md

    - Part3. Enterprise AI Agent:

        - Step3-8. Multi Agent 협업:
            study/step3/step3_8_multi_agent_guide.md

        - Step3-9. Enterprise AI Agent Platform:
            study/step3/step3_9_enterprise_ai_agent_platform_guide.md
```

---

## 4. Part 구성

Step3는 크게 세 개의 Part로 구성한다.

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
│   ├─ Step3-5. Workflow Agent(LangGraph)
│   ├─ Step3-6. MCP 아키텍처 이해
│   └─ Step3-7. MCP 기반 외부 시스템 연동
│
└─ Part3. Enterprise AI Agent
    ├─ Step3-8. Multi Agent 협업
    └─ Step3-9. Enterprise AI Agent Platform
```

---

# Part1. AI Agent 기초

Part1에서는 AI Agent의 기본 개념과 동작 원리를 학습한다.

이 단계에서는 아직 복잡한 프레임워크보다 **Agent가 어떤 방식으로 생각하고 행동하는지**를 이해하는 것이 중요하다.

---

## Step3-1. AI Agent 개요

### 문서 경로

```text
docs/study/step3/step3_1_ai_agent_overview_guide.md
```

### 학습 목표

이 문서에서는 AI Agent의 개념과 등장 배경을 학습한다.

기존 LLM은 사용자의 질문에 대해 답변을 생성하는 역할을 주로 수행한다.  
하지만 AI Agent는 사용자의 목표를 이해한 뒤, 필요한 작업을 나누고, 적절한 도구를 선택하고, 실행 결과를 확인하면서 다음 행동을 결정한다.

### 핵심 내용

```text
1. AI Agent란 무엇인가?
2. 기존 LLM과 Agent의 차이
3. Chatbot, RAG, Agent의 차이
4. Agent의 기본 구성 요소
5. Agent의 동작 흐름
6. Agent가 필요한 업무 사례
7. Enterprise Agent의 개념
```

### 주요 설명 포인트

AI Agent는 단순히 답변을 잘하는 모델이 아니다.  
Agent는 다음 요소를 함께 가진 시스템이다.

```text
LLM
+ 목표 이해
+ 계획 수립
+ 도구 선택
+ 도구 실행
+ 결과 검증
+ 반복 수행
```

예를 들어 사용자가 다음과 같이 요청했다고 가정한다.

```text
"지난주 장애 내용을 정리해서 보고서 초안을 만들어줘."
```

일반 LLM은 보고서 양식을 설명할 수는 있지만, 실제 장애 이력을 조회하거나 파일을 읽거나 보고서를 생성하지는 못한다.

반면 Agent는 다음과 같은 절차를 수행할 수 있다.

```text
1. 장애 이력 조회
2. 관련 로그 또는 문서 검색
3. 장애 유형 분류
4. 원인과 조치 내용 요약
5. 보고서 초안 생성
```

### 실습 방향

이 단계에서는 아직 복잡한 코드를 작성하지 않고, Agent의 동작 방식을 그림과 의사코드로 이해한다.

---

## Step3-2. ReAct와 Tool Calling

### 문서 경로

```text
docs/study/step3/step3_2_react_and_tool_calling_guide.md
```

### 학습 목표

이 문서에서는 Agent의 핵심 동작 방식인 **ReAct**와 **Tool Calling**을 학습한다.

ReAct는 Reasoning과 Acting을 결합한 방식이다.  
즉, Agent가 생각만 하는 것이 아니라 생각한 내용을 바탕으로 행동하고, 행동 결과를 다시 관찰하여 다음 판단을 수행하는 구조이다.

Tool Calling은 LLM이 외부 도구를 직접 호출할 수 있도록 하는 방식이다.  
예를 들어 계산기, 파일 읽기, 검색, 데이터베이스 조회, API 호출 등을 LLM이 필요에 따라 사용할 수 있게 한다.

### 핵심 내용

```text
1. ReAct란 무엇인가?
2. Reasoning과 Acting의 차이
3. Thought / Action / Observation 구조
4. Tool Calling 개념
5. Tool Schema의 역할
6. 도구 선택 기준
7. Tool Calling과 Function Calling의 관계
8. 잘못된 도구 호출을 방지하는 방법
```

### ReAct 기본 흐름

```text
사용자 질문
   ↓
Thought: 무엇을 해야 하는지 판단
   ↓
Action: 필요한 도구 선택
   ↓
Observation: 도구 실행 결과 확인
   ↓
Thought: 결과를 보고 다음 행동 판단
   ↓
Final Answer: 최종 답변
```

### 예시

```text
질문:
"12,500원의 상품을 17개 구매하면 총액이 얼마야?"

Thought:
계산이 필요하다.

Action:
calculator 도구를 사용한다.

Observation:
212,500

Final Answer:
총액은 212,500원입니다.
```

### 실습 방향

이 단계에서는 Python으로 간단한 도구를 만든다.

```text
tools/
├─ calculator.py
├─ file_reader.py
└─ search.py
```

각 도구는 Agent가 호출할 수 있는 함수 형태로 작성한다.

---

## Step3-3. 첫 번째 AI Agent 구현

### 문서 경로

```text
docs/study/step3/step3_3_first_ai_agent_guide.md
```

### 학습 목표

이 문서에서는 Python으로 첫 번째 단일 Agent를 구현한다.

목표는 복잡한 프레임워크 없이 다음 흐름을 직접 이해하는 것이다.

```text
사용자 질문
   ↓
LLM 판단
   ↓
도구 선택
   ↓
도구 실행
   ↓
결과를 바탕으로 답변 생성
```

### 핵심 내용

```text
1. Agent 실행 루프 구조
2. 사용자 질문 입력
3. 도구 목록 정의
4. LLM 프롬프트 구성
5. 도구 호출 판단
6. 도구 실행 결과 반영
7. 최종 답변 생성
```

### 실습 파일

```text
labs/agent/01_first_agent.py
labs/agent/02_tool_calling.py
```

### 예시 구조

```text
사용자:
"sample.txt 파일을 읽고 핵심 내용을 요약해줘."

Agent:
1. 파일 읽기 도구가 필요하다고 판단
2. file_reader 도구 호출
3. 파일 내용 확인
4. LLM에게 요약 요청
5. 최종 답변 반환
```

### 구현 관점

이 단계에서는 LangGraph나 MCP를 사용하지 않고, Agent의 기본 동작을 직접 구현한다.  
직접 구현해보면 나중에 프레임워크를 사용할 때 내부 동작을 훨씬 쉽게 이해할 수 있다.

---

## Step3-4. Agent Memory와 상태 관리

### 문서 경로

```text
docs/study/step3/step3_4_agent_memory_guide.md
```

### 학습 목표

이 문서에서는 Agent Memory와 상태 관리 개념을 학습한다.

Agent가 한 번의 질문에만 답하는 경우에는 Memory가 필요하지 않을 수 있다.  
하지만 실제 업무에서는 사용자의 이전 요청, 진행 중인 작업, 선택한 파일, 중간 결과, 도구 실행 이력 등을 기억해야 한다.

### 핵심 내용

```text
1. Memory가 필요한 이유
2. Short-term Memory
3. Long-term Memory
4. Conversation History
5. Task State
6. Tool Execution History
7. Memory 저장 위치
8. Memory와 개인정보/보안
```

### Memory 유형

```text
Short-term Memory
- 현재 대화 안에서만 유지되는 기억
- 대화 흐름, 최근 질문, 중간 결과 저장

Long-term Memory
- 여러 대화에 걸쳐 유지되는 기억
- 사용자 선호, 프로젝트 설정, 자주 사용하는 경로 저장

Task State
- 특정 작업의 진행 상태
- 예: 보고서 작성 중, 파일 분석 완료, 검토 대기
```

### 실습 파일

```text
labs/agent/03_memory.py
```

### 실습 방향

처음에는 JSON 파일 또는 Python dictionary로 간단한 Memory를 구현한다.  
이후에는 SQLite, ChromaDB, LangGraph Store 등으로 확장할 수 있다.

---

# Part2. AI Agent 심화

Part2에서는 단순 Agent를 넘어, 복잡한 업무 흐름을 안정적으로 제어하는 방법을 학습한다.

Agent가 스스로 판단하는 구조는 유연하지만, 엔터프라이즈 업무에서는 예측 가능성과 통제 가능성이 매우 중요하다.  
따라서 Workflow 기반 Agent와 MCP 기반 외부 시스템 연동 구조를 함께 학습한다.

---

## Step3-5. Workflow Agent(LangGraph)

### 문서 경로

```text
docs/study/step3/step3_5_langgraph_workflow_agent_guide.md
```

### 학습 목표

이 문서에서는 Workflow 기반 Agent 구조를 학습한다.

LangGraph는 Agent의 상태와 실행 흐름을 그래프 형태로 구성할 수 있도록 도와주는 프레임워크이다.  
일반 Agent가 매번 자유롭게 판단하는 구조라면, Workflow Agent는 정해진 노드와 조건에 따라 안정적으로 흐름을 제어할 수 있다.

### 핵심 내용

```text
1. Workflow Agent가 필요한 이유
2. 자유형 Agent의 한계
3. Graph 기반 실행 흐름
4. Node와 Edge 개념
5. State 관리
6. Conditional Edge
7. Human-in-the-loop
8. Retry와 Error Handling
```

### 기본 구조

```text
START
  ↓
질문 분석 Node
  ↓
도구 선택 Node
  ↓
도구 실행 Node
  ↓
결과 검증 Node
  ↓
답변 생성 Node
  ↓
END
```

### 실습 파일

```text
labs/agent/04_langgraph.py
```

### Enterprise 관점

기업 업무에서는 다음과 같은 이유로 Workflow Agent가 중요하다.

```text
1. 실행 흐름을 통제할 수 있다.
2. 승인 단계를 넣을 수 있다.
3. 실패 시 재시도 또는 예외 처리가 가능하다.
4. 특정 업무 프로세스를 표준화할 수 있다.
5. 감사 로그를 남기기 쉽다.
```

---

## Step3-6. MCP 아키텍처 이해

### 문서 경로

```text
docs/study/step3/step3_6_mcp_architecture_guide.md
```

### 학습 목표

이 문서에서는 MCP(Model Context Protocol)의 개념과 아키텍처를 학습한다.

MCP는 AI 애플리케이션이 외부 시스템과 표준화된 방식으로 연결될 수 있도록 하는 프로토콜이다.  
MCP를 사용하면 Agent가 파일, 데이터베이스, API, 검색 시스템, 업무 시스템 등을 일관된 방식으로 호출할 수 있다.

### 핵심 내용

```text
1. MCP가 등장한 배경
2. MCP가 해결하는 문제
3. MCP Host
4. MCP Client
5. MCP Server
6. Tools, Resources, Prompts
7. Client/Server 연결 구조
8. MCP와 API Gateway의 차이
9. MCP와 Tool Calling의 관계
```

### MCP 기본 구조

```text
AI Application / Host
        │
        ▼
    MCP Client
        │
        ▼
    MCP Server
        │
        ├─ Tools
        ├─ Resources
        └─ Prompts
```

### Enterprise 관점

기존에는 Agent가 외부 시스템마다 별도 방식으로 연동해야 했다.

```text
Jira API 연동 방식
GitHub API 연동 방식
DB 연동 방식
파일 시스템 연동 방식
사내 업무 API 연동 방식
```

MCP를 사용하면 이러한 연동 방식을 표준화할 수 있다.

```text
Agent
  ↓
MCP Client
  ↓
각 업무별 MCP Server
```

---

## Step3-7. MCP 기반 외부 시스템 연동

### 문서 경로

```text
docs/study/step3/step3_7_mcp_practice_guide.md
```

### 학습 목표

이 문서에서는 MCP를 이용해 외부 시스템을 연동하는 실습을 진행한다.

처음에는 단순한 파일 시스템 또는 계산기 MCP Server를 만들고, 이후에는 RAG 검색, 데이터베이스, 사내 API로 확장한다.

### 핵심 내용

```text
1. MCP Server 기본 구현
2. Tool 정의
3. Resource 정의
4. MCP Client에서 Server 연결
5. Agent에서 MCP Tool 호출
6. 파일 시스템 연동
7. RAG 검색 연동
8. 사내 API 연동 구조
```

### 실습 파일

```text
labs/agent/05_mcp_client.py

labs/agent/mcp/
├─ file_mcp_server.py
├─ rag_mcp_server.py
└─ sample_mcp_client.py
```

### 실습 예시

```text
사용자:
"docs 폴더에 있는 Step2 문서 중 RAG 관련 내용을 찾아서 요약해줘."

Agent:
1. MCP File Server에 문서 목록 요청
2. MCP RAG Server에 검색 요청
3. 검색 결과를 LLM에 전달
4. 요약 답변 생성
```

### 확장 방향

```text
File MCP Server
DB MCP Server
Git MCP Server
Jira MCP Server
Confluence MCP Server
Mail MCP Server
Calendar MCP Server
RAG MCP Server
```

---

# Part3. Enterprise AI Agent

Part3에서는 실제 기업 환경에서 AI Agent를 어떻게 설계하고 운영할지 학습한다.

여기서는 단일 Agent가 아니라 여러 Agent가 역할을 나누어 협업하는 구조와, 이를 통합 운영하기 위한 Enterprise AI Agent Platform 아키텍처를 다룬다.

---

## Step3-8. Multi Agent 협업

### 문서 경로

```text
docs/study/step3/step3_8_multi_agent_guide.md
```

### 학습 목표

이 문서에서는 Multi Agent 구조를 학습한다.

하나의 Agent가 모든 일을 처리할 수도 있지만, 업무가 복잡해질수록 역할 분리가 필요하다.  
Multi Agent는 여러 Agent가 각자 전문 역할을 맡고, Supervisor 또는 Orchestrator가 전체 흐름을 조정하는 구조이다.

### 핵심 내용

```text
1. Multi Agent가 필요한 이유
2. 단일 Agent의 한계
3. 역할 기반 Agent 설계
4. Supervisor Agent
5. Planner Agent
6. Search Agent
7. Report Agent
8. QA Agent
9. Agent 간 메시지 전달
10. 협업 실패와 충돌 해결
```

### 예시 구조

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

### 실습 파일

```text
labs/agent/06_multi_agent.py
```

### Enterprise 적용 예시

```text
장애 보고서 작성 Multi Agent

1. Planner Agent
   - 필요한 작업을 분해한다.

2. Search Agent
   - 장애 이력, 로그, 문서를 검색한다.

3. Analysis Agent
   - 원인과 영향도를 분석한다.

4. Report Agent
   - 보고서 초안을 작성한다.

5. QA Agent
   - 누락 항목과 표현을 검토한다.
```

---

## Step3-9. Enterprise AI Agent Platform

### 문서 경로

```text
docs/study/step3/step3_9_enterprise_ai_agent_platform_guide.md
```

### 학습 목표

이 문서에서는 Enterprise AI Agent Platform의 전체 아키텍처를 설계한다.

이 단계는 Step3의 최종 정리 단계이다.  
Local LLM, RAG, Agent, Memory, LangGraph, MCP, Multi Agent를 하나의 플랫폼 구조로 통합한다.

### 핵심 내용

```text
1. Enterprise AI Agent Platform 개요
2. 전체 아키텍처
3. Agent Gateway
4. Agent Runtime
5. Tool Registry
6. MCP Client Layer
7. MCP Server Layer
8. RAG 연동
9. Memory Store
10. Observability
11. 보안과 권한
12. 감사 로그
13. 운영 정책
14. 확장 전략
```

### 전체 아키텍처 예시

```text
사용자 / Open WebUI
        │
        ▼
AI Agent Gateway
        │
        ▼
Agent Orchestrator
        │
        ├─ Planner Agent
        ├─ Search Agent
        ├─ Report Agent
        └─ QA Agent
        │
        ▼
MCP Client Layer
        │
        ├─ File MCP Server
        ├─ RAG MCP Server
        ├─ DB MCP Server
        ├─ Git MCP Server
        └─ 업무 API MCP Server
        │
        ▼
Enterprise Systems
        ├─ 문서 저장소
        ├─ Vector DB
        ├─ 업무 DB
        ├─ Git Repository
        └─ 사내 시스템
```

### 실습 파일

```text
labs/agent/07_enterprise_agent.py
```

### 최종 목표

Step3의 최종 목표는 다음 구조를 이해하고 설명할 수 있는 것이다.

```text
LLM은 판단을 담당한다.
Agent는 실행 흐름을 담당한다.
Tool은 실제 작업을 수행한다.
MCP는 외부 시스템 연결을 표준화한다.
Workflow는 실행 흐름을 통제한다.
Memory는 상태와 맥락을 유지한다.
Multi Agent는 복잡한 업무를 역할별로 분리한다.
Enterprise Platform은 이 모든 것을 안전하게 운영한다.
```

---

# 5. 모든 Step 문서 공통 템플릿

Step3의 각 문서는 아래 템플릿을 기준으로 작성한다.

```text
1. 학습 목표

2. 왜 필요한가?

3. 기존 방식의 한계

4. AI Agent가 해결하는 문제

5. 핵심 개념

6. 전체 아키텍처

7. 동작 과정

8. 실습 준비

9. Python 실습

10. 코드 분석

11. 실행 결과

12. Enterprise 적용 사례

13. Best Practice

14. 트러블슈팅

15. 핵심 정리

16. 다음 단계 예고
```

이 템플릿을 사용하면 모든 문서가 동일한 흐름으로 작성되기 때문에 학습자 입장에서 문서 구조를 예측하기 쉽다.

---

# 6. Step3 실습 디렉터리 구조

Step3 실습 코드는 `labs/agent` 하위에 구성한다.

```text
labs
└── agent
    ├── README.md
    │
    ├── common
    │   ├── config.py
    │   ├── llm_client.py
    │   └── logger.py
    │
    ├── tools
    │   ├── calculator.py
    │   ├── file_reader.py
    │   ├── search.py
    │   ├── weather.py
    │   └── shell.py
    │
    ├── memory
    │   ├── simple_memory.py
    │   └── sqlite_memory.py
    │
    ├── langgraph
    │   └── workflow_agent.py
    │
    ├── mcp
    │   ├── file_mcp_server.py
    │   ├── rag_mcp_server.py
    │   └── sample_mcp_client.py
    │
    ├── enterprise
    │   ├── agent_gateway.py
    │   ├── tool_registry.py
    │   └── audit_logger.py
    │
    ├── 01_first_agent.py
    ├── 02_tool_calling.py
    ├── 03_memory.py
    ├── 04_langgraph.py
    ├── 05_mcp_client.py
    ├── 06_multi_agent.py
    └── 07_enterprise_agent.py
```

---

# 7. Step3 문서 디렉터리 생성 명령

프로젝트 루트에서 아래 명령을 실행한다.

```bash
mkdir -p docs/study/step3
mkdir -p labs/agent/common
mkdir -p labs/agent/tools
mkdir -p labs/agent/memory
mkdir -p labs/agent/langgraph
mkdir -p labs/agent/mcp
mkdir -p labs/agent/enterprise
```

---

# 8. Step3 문서 파일 생성 명령

아래 명령으로 빈 문서 파일을 먼저 생성할 수 있다.

```bash
touch docs/study/step3/step3_1_ai_agent_overview_guide.md
touch docs/study/step3/step3_2_react_and_tool_calling_guide.md
touch docs/study/step3/step3_3_first_ai_agent_guide.md
touch docs/study/step3/step3_4_agent_memory_guide.md
touch docs/study/step3/step3_5_langgraph_workflow_agent_guide.md
touch docs/study/step3/step3_6_mcp_architecture_guide.md
touch docs/study/step3/step3_7_mcp_practice_guide.md
touch docs/study/step3/step3_8_multi_agent_guide.md
touch docs/study/step3/step3_9_enterprise_ai_agent_platform_guide.md
```

---

# 9. mkdocs.yml 반영 예시

기존 `mkdocs.yml`의 `nav` 항목 중 적절한 위치에 아래 내용을 추가한다.

```yaml
- Step3. AI Agent:
    - Part1. AI Agent 기초:
        - Step3-1. AI Agent 개요:
            study/step3/step3_1_ai_agent_overview_guide.md
        - Step3-2. ReAct와 Tool Calling:
            study/step3/step3_2_react_and_tool_calling_guide.md
        - Step3-3. 첫 번째 AI Agent 구현:
            study/step3/step3_3_first_ai_agent_guide.md
        - Step3-4. Agent Memory와 상태 관리:
            study/step3/step3_4_agent_memory_guide.md

    - Part2. AI Agent 심화:
        - Step3-5. Workflow Agent(LangGraph):
            study/step3/step3_5_langgraph_workflow_agent_guide.md
        - Step3-6. MCP 아키텍처 이해:
            study/step3/step3_6_mcp_architecture_guide.md
        - Step3-7. MCP 기반 외부 시스템 연동:
            study/step3/step3_7_mcp_practice_guide.md

    - Part3. Enterprise AI Agent:
        - Step3-8. Multi Agent 협업:
            study/step3/step3_8_multi_agent_guide.md
        - Step3-9. Enterprise AI Agent Platform:
            study/step3/step3_9_enterprise_ai_agent_platform_guide.md
```

---

# 10. Step3 진행 순서

Step3는 아래 순서로 진행한다.

```text
1주차
- Step3-1. AI Agent 개요
- Step3-2. ReAct와 Tool Calling

2주차
- Step3-3. 첫 번째 AI Agent 구현
- Step3-4. Agent Memory와 상태 관리

3주차
- Step3-5. Workflow Agent(LangGraph)
- Step3-6. MCP 아키텍처 이해

4주차
- Step3-7. MCP 기반 외부 시스템 연동
- Step3-8. Multi Agent 협업

5주차
- Step3-9. Enterprise AI Agent Platform
- Step3 전체 통합 실습
```

이 일정은 절대적인 기준은 아니며, 실습 난이도에 따라 조정할 수 있다.

---

# 11. Part별 종료 프로젝트

각 Part가 끝날 때마다 작은 프로젝트를 수행한다.

---

## 11.1 Part1 종료 프로젝트

```text
프로젝트명:
파일을 읽고 요약하는 AI Agent 만들기

포함 내용:
- Tool Calling
- ReAct
- 파일 읽기 도구
- 간단한 Memory
- 최종 요약 답변
```

---

## 11.2 Part2 종료 프로젝트

```text
프로젝트명:
MCP 기반 사내 문서 검색 Agent 만들기

포함 내용:
- LangGraph Workflow
- MCP Client
- File MCP Server
- RAG MCP Server
- 검색 결과 요약
```

---

## 11.3 Part3 종료 프로젝트

```text
프로젝트명:
Enterprise AI Agent Platform Prototype

포함 내용:
- Agent Gateway
- Multi Agent
- MCP Server Layer
- RAG 연동
- Memory Store
- Audit Log
- Open WebUI 연동 구조
```

---

# 12. Step3에서 특히 주의할 점

AI Agent는 강력하지만, 통제 없이 사용하면 위험할 수 있다.  
따라서 Step3에서는 기능 구현뿐 아니라 다음 항목을 반드시 함께 다룬다.

```text
1. 도구 실행 권한 제어
2. 파일 시스템 접근 범위 제한
3. Shell 명령 실행 제한
4. 개인정보와 민감정보 보호
5. API Key 관리
6. 실행 로그와 감사 로그
7. Human-in-the-loop 승인 절차
8. 실패 시 복구 전략
9. 비용과 성능 관리
10. Agent 오동작 방지
```

특히 Enterprise 환경에서는 Agent가 실제 시스템에 영향을 줄 수 있으므로, 읽기 전용 도구와 쓰기 도구를 반드시 구분해야 한다.

---

# 13. Step3와 Step4의 연결

Step3는 이후 Step4. AI Data Platform으로 자연스럽게 연결된다.

```text
Step1. Local LLM
   ↓
Step2. RAG
   ↓
Step3. AI Agent
   ↓
Step4. AI Data Platform
   ↓
Step5. AI Service / Serving
```

Step3에서 Agent가 도구를 사용하고 외부 시스템을 호출하는 구조를 학습하면, Step4에서는 이를 플랫폼 형태로 확장한다.

Step4에서는 다음 주제를 다룰 수 있다.

```text
1. Agent Gateway 고도화
2. AI 서비스 API화
3. 사용자별 권한 관리
4. 모델 라우팅
5. RAG 서비스화
6. MCP Server 운영
7. Agent Observability
8. 운영 대시보드
9. 서비스 배포
10. 사내 AI 업무 플랫폼화
```

---

# 14. 참고 자료

아래 자료는 Step3 학습 시 참고할 수 있는 공식 문서이다.

```text
Model Context Protocol 공식 문서
https://modelcontextprotocol.io/docs/getting-started/intro

MCP Architecture Overview
https://modelcontextprotocol.io/docs/learn/architecture

MCP Tools Specification
https://modelcontextprotocol.io/specification/2025-06-18/server/tools

LangGraph 공식 문서
https://langchain-ai.github.io/langgraph/

LangGraph Memory / LangMem 문서
https://langchain-ai.github.io/langmem/

OpenAI Tool Calling / Function Calling 문서
https://platform.openai.com/docs/
```

---

# 15. 핵심 정리

Step3는 AI DATA Platform 연구 프로젝트에서 매우 중요한 전환점이다.

Step1과 Step2가 LLM과 RAG를 이해하는 단계였다면, Step3는 LLM을 실제 업무 시스템과 연결하여 **스스로 판단하고 실행하는 AI 시스템**으로 확장하는 단계이다.

이번 Step3의 핵심은 다음과 같다.

```text
1. Agent는 단순 답변 생성기가 아니라 작업 수행 구조이다.
2. ReAct는 생각과 행동을 반복하는 Agent의 기본 패턴이다.
3. Tool Calling은 Agent가 외부 기능을 사용할 수 있게 한다.
4. Memory는 Agent가 맥락과 상태를 유지하게 한다.
5. LangGraph는 복잡한 Agent 흐름을 안정적으로 제어한다.
6. MCP는 외부 시스템 연동을 표준화한다.
7. Multi Agent는 복잡한 업무를 역할별로 분리한다.
8. Enterprise Agent Platform은 Agent를 안전하게 운영하기 위한 구조이다.
```

따라서 Step3는 단순한 코딩 실습이 아니라,  
**AI 아키텍트가 Enterprise AI Platform을 설계하기 위해 반드시 이해해야 하는 핵심 과정**이다.

---

# 16. 다음 작업

이 문서를 기준으로 다음 순서로 세부 가이드를 작성한다.

```text
1. step3_1_ai_agent_overview_guide.md 작성
2. step3_2_react_and_tool_calling_guide.md 작성
3. labs/agent 기본 디렉터리 생성
4. 첫 번째 Agent 실습 코드 작성
5. Step3 전체 MkDocs nav 반영
```

---
