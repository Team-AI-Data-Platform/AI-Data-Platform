# Step3-2. ReAct와 Tool Calling 가이드

> AI DATA Platform 연구 프로젝트  
> Step3. AI Agent  
> Part1. AI Agent 기초  
> 문서 경로: `docs/study/step3/step3_2_react_and_tool_calling_guide.md`  
> 작성일: 2026-06-29

---

## 1. 문서 목적

이 문서는 AI Agent의 핵심 동작 원리인 **ReAct**와 **Tool Calling**을 설명하기 위한 가이드 문서이다.

앞 단계인 `Step3-1. AI Agent 개요`에서는 AI Agent가 무엇인지, Chatbot·RAG·Agent가 어떻게 다른지, Agent가 어떤 구성 요소로 이루어지는지 학습했다.

이번 `Step3-2`에서는 Agent가 실제로 **어떻게 생각하고**, **어떻게 도구를 선택하고**, **도구 실행 결과를 어떻게 다시 판단에 반영하는지**를 학습한다.

이 문서는 구현 실습보다는 개념과 설계 원리를 중심으로 작성한다.  
실제 Python 코드 구현은 다음 단계인 `Step3-3. 첫 번째 AI Agent 구현`에서 본격적으로 다룬다.

---

## 2. 이번 문서의 위치

전체 Step3 목차에서 이 문서의 위치는 다음과 같다.

```text
Step3. AI Agent
│
├─ Part1. AI Agent 기초
│   ├─ Step3-1. AI Agent 개요
│   ├─ Step3-2. ReAct와 Tool Calling   ← 현재 문서
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

Step3-2는 Step3 전체에서 매우 중요한 위치를 가진다.

```text
Step3-1:
AI Agent의 큰 그림을 이해한다.

Step3-2:
Agent가 생각하고 행동하는 핵심 원리를 이해한다.

Step3-3:
그 원리를 Python 코드로 직접 구현한다.
```

따라서 이번 문서에서는 코드를 많이 작성하기보다, 다음 구현 단계에서 헷갈리지 않도록 Agent의 내부 동작 방식을 충분히 이해하는 데 집중한다.

---

## 3. 학습 목표

이 문서를 마치면 다음 내용을 설명할 수 있어야 한다.

```text
1. ReAct가 무엇인지 설명할 수 있다.
2. Reasoning과 Acting의 차이를 설명할 수 있다.
3. Thought, Action, Observation 구조를 설명할 수 있다.
4. Chain of Thought와 ReAct의 차이를 설명할 수 있다.
5. Tool Calling이 무엇인지 설명할 수 있다.
6. Function Calling과 Tool Calling의 관계를 설명할 수 있다.
7. Tool Schema가 왜 중요한지 설명할 수 있다.
8. LLM이 도구를 직접 실행하는 것이 아니라는 점을 이해한다.
9. Tool Calling 기반 Agent Loop의 흐름을 설명할 수 있다.
10. Enterprise 환경에서 Tool Calling을 통제해야 하는 이유를 설명할 수 있다.
```

---

## 4. 왜 ReAct와 Tool Calling을 먼저 배워야 하는가?

AI Agent를 구현하려면 가장 먼저 다음 질문에 답할 수 있어야 한다.

```text
Agent는 어떻게 다음 행동을 결정하는가?
```

Agent는 단순히 사용자의 질문에 바로 답변하지 않는다.  
필요한 경우 스스로 다음과 같은 판단을 수행한다.

```text
1. 지금 바로 답변할 수 있는가?
2. 추가 정보가 필요한가?
3. 어떤 도구를 사용해야 하는가?
4. 도구에 어떤 값을 전달해야 하는가?
5. 도구 실행 결과가 충분한가?
6. 추가 도구 호출이 필요한가?
7. 최종 답변을 만들어도 되는가?
```

이 판단과 실행이 반복되는 구조가 Agent의 핵심이다.

이때 ReAct는 Agent가 **생각과 행동을 번갈아 수행하는 패턴**을 제공한다.  
Tool Calling은 Agent가 **외부 도구를 구조화된 방식으로 호출하는 방법**을 제공한다.

즉, 두 개념의 관계는 다음과 같다.

```text
ReAct:
- Agent가 어떻게 생각하고 행동할지에 대한 패턴

Tool Calling:
- Agent의 행동을 실제 도구 호출로 연결하는 기술
```

---

## 5. 기존 LLM 방식의 한계

일반 LLM은 다음 구조로 동작한다.

```text
사용자 질문
   ↓
LLM
   ↓
답변 생성
```

이 구조는 단순한 질문에는 충분하다.

```text
"RAG가 뭐야?"
"Python의 tuple이 뭐야?"
"이 문장을 공손하게 다듬어줘."
```

하지만 실제 업무 요청은 단순하지 않다.

```text
"프로젝트 문서를 검색해서 요약해줘."
"지난주 장애 내용을 보고서로 정리해줘."
"서버 상태를 점검하고 이상 여부를 알려줘."
"엑셀 파일을 읽고 합계를 계산해줘."
```

이런 요청에는 외부 정보 조회, 파일 읽기, 계산, 상태 확인, 보고서 생성 같은 행동이 필요하다.

LLM 단독 구조에서는 다음 한계가 있다.

```text
1. 로컬 파일을 직접 읽지 못한다.
2. 데이터베이스를 직접 조회하지 못한다.
3. 최신 운영 상태를 직접 확인하지 못한다.
4. 외부 API를 직접 호출하지 못한다.
5. 복잡한 작업을 여러 단계로 나누어 실행하기 어렵다.
6. 실행 결과를 바탕으로 다음 행동을 결정하기 어렵다.
```

Agent는 이 한계를 해결하기 위해 LLM에 외부 도구 사용 능력을 연결한다.

---

## 6. Chain of Thought의 한계

ReAct를 이해하려면 먼저 Chain of Thought를 이해해야 한다.

Chain of Thought는 LLM이 바로 답을 내지 않고, 중간 추론 과정을 거쳐 답을 생성하도록 유도하는 방식이다.

예를 들어 다음 질문이 있다고 하자.

```text
"12,500원짜리 상품을 17개 구매하면 총액이 얼마야?"
```

Chain of Thought 방식은 다음처럼 사고 과정을 거친다.

```text
상품 1개의 가격은 12,500원이다.
17개를 구매하므로 12,500 × 17을 계산해야 한다.
12,500 × 10 = 125,000
12,500 × 7 = 87,500
합계는 212,500이다.
따라서 총액은 212,500원이다.
```

이 방식은 복잡한 문제를 풀 때 도움이 된다.

하지만 Chain of Thought에는 한계가 있다.

```text
1. 생각만 할 수 있고 행동은 하지 못한다.
2. 외부 시스템에서 정보를 가져오지 못한다.
3. 잘못된 정보를 기반으로 계속 추론할 수 있다.
4. 최신 정보가 필요한 문제에 약하다.
5. 계산이나 검색 같은 작업을 실제 도구에 맡기지 못한다.
```

즉, Chain of Thought는 **Reasoning 중심**이다.  
하지만 실제 Agent에는 Reasoning뿐 아니라 Acting도 필요하다.

---

## 7. ReAct란 무엇인가?

ReAct는 **Reasoning + Acting**의 합성어이다.

```text
Reasoning:
- 생각하기
- 문제를 분석하기
- 다음에 무엇을 해야 할지 판단하기

Acting:
- 행동하기
- 도구를 사용하기
- 외부 환경과 상호작용하기
```

ReAct는 LLM이 Reasoning과 Acting을 번갈아 수행하도록 만드는 패턴이다.

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

각 단계는 다음 의미를 가진다.

```text
Thought:
현재 문제를 해결하기 위해 무엇이 필요한지 생각한다.

Action:
필요한 도구를 선택하고 호출한다.

Observation:
도구 실행 결과를 확인한다.

Final Answer:
충분한 정보가 모이면 최종 답변을 생성한다.
```

ReAct의 핵심은 **생각과 행동이 분리되어 있지 않고 서로 연결되어 있다는 점**이다.

```text
생각이 행동을 결정한다.
행동 결과가 다음 생각을 바꾼다.
다음 생각이 다음 행동을 결정한다.
```

---

## 8. ReAct 논문의 핵심 아이디어

ReAct는 2022년에 발표된 논문인 **ReAct: Synergizing Reasoning and Acting in Language Models**에서 널리 알려졌다.

논문의 핵심 문제의식은 다음과 같다.

```text
기존 연구에서는 LLM의 추론 능력과 행동 능력을 따로 다루는 경우가 많았다.
하지만 실제 문제 해결에서는 생각과 행동이 함께 필요하다.
```

ReAct는 LLM이 다음 두 가지를 함께 생성하도록 한다.

```text
1. Reasoning Trace
   - 문제를 해결하기 위한 추론 과정

2. Task-specific Action
   - 외부 환경이나 도구에 대한 행동
```

논문에서는 ReAct가 외부 지식 베이스나 환경과 상호작용하면서 환각과 오류 전파를 줄이고, 사람이 이해하기 쉬운 문제 해결 과정을 만들 수 있다고 설명한다.

특히 ReAct의 장점은 다음과 같다.

```text
1. 외부 정보와 상호작용할 수 있다.
2. 잘못된 추론을 도구 결과로 보정할 수 있다.
3. 중간 과정이 드러나므로 해석 가능성이 높아진다.
4. 단순 답변이 아니라 문제 해결 궤적을 만들 수 있다.
```

---

## 9. ReAct 기본 패턴

ReAct의 대표적인 표현은 다음과 같다.

```text
Question:
사용자 질문

Thought:
무엇을 해야 하는지 생각한다.

Action:
사용할 도구를 선택한다.

Action Input:
도구에 전달할 입력값을 만든다.

Observation:
도구 실행 결과를 확인한다.

Thought:
결과를 보고 다음 행동을 판단한다.

Final Answer:
최종 답변을 생성한다.
```

이를 구조화하면 다음과 같다.

```text
Question
  ↓
Thought
  ↓
Action + Action Input
  ↓
Observation
  ↓
Thought
  ↓
Final Answer
```

실제 Agent 구현에서는 이 구조가 다음 형태로 바뀐다.

```text
사용자 메시지
  ↓
LLM 응답
  ↓
Tool Call
  ↓
Tool Result
  ↓
LLM 응답
  ↓
Final Answer
```

즉, ReAct는 개념적 패턴이고, Tool Calling은 이 패턴을 실제 시스템에서 구현하는 방식 중 하나이다.

---

## 10. ReAct 예시 1: 계산 문제

사용자 질문:

```text
"12,500원짜리 상품을 17개 구매하면 총액이 얼마야?"
```

ReAct 흐름:

```text
Thought:
총액 계산이 필요하다. 상품 가격과 수량을 곱해야 한다.

Action:
calculator

Action Input:
12500 * 17

Observation:
212500

Thought:
계산 결과가 나왔으므로 최종 답변을 만들 수 있다.

Final Answer:
총액은 212,500원입니다.
```

이 예시에서 중요한 점은 LLM이 직접 암산하지 않고 계산기 도구를 사용할 수 있다는 점이다.  
실무에서는 계산, 집계, 날짜 계산처럼 정확성이 중요한 작업은 가능하면 도구를 사용하는 것이 좋다.

---

## 11. ReAct 예시 2: 문서 검색 문제

사용자 질문:

```text
"Step2 RAG 문서에서 ChromaDB 관련 내용을 요약해줘."
```

ReAct 흐름:

```text
Thought:
사용자는 특정 문서 내용 요약을 요청했다. 먼저 관련 문서를 검색해야 한다.

Action:
search_documents

Action Input:
ChromaDB RAG Step2

Observation:
ChromaDB 구축, Collection 생성, 문서 Chunk 저장, 유사도 검색 관련 문서가 검색되었다.

Thought:
검색 결과를 바탕으로 요약할 수 있다. 출처도 함께 표시해야 한다.

Final Answer:
Step2 RAG 문서에서 ChromaDB는 문서 Chunk를 벡터로 저장하고, 질문과 유사한 문서를 검색하는 Vector DB 역할을 합니다...
```

이 예시에서 RAG는 Agent가 사용하는 도구가 된다.

```text
RAG = 검색 도구
Agent = 검색 도구를 사용할지 판단하는 주체
```

---

## 12. ReAct 예시 3: 운영 점검 문제

사용자 질문:

```text
"AI 플랫폼 상태를 점검해줘."
```

ReAct 흐름:

```text
Thought:
AI 플랫폼 상태를 확인하려면 여러 구성 요소를 점검해야 한다.

Action:
check_docker_status

Observation:
Open WebUI 컨테이너가 실행 중이다.

Thought:
Ollama 상태도 확인해야 한다.

Action:
check_ollama_status

Observation:
Ollama 서버는 실행 중이지만 현재 메모리에 올라간 모델은 없다.

Thought:
ChromaDB 저장 경로도 확인해야 한다.

Action:
check_chroma_status

Observation:
chroma_db 디렉터리가 존재하고 컬렉션 파일이 확인된다.

Thought:
각 점검 결과를 종합해서 보고할 수 있다.

Final Answer:
현재 Open WebUI와 Ollama는 실행 중이며, ChromaDB 경로도 확인됩니다. 다만 현재 Ollama 메모리에 로드된 모델은 없습니다...
```

이 예시는 Agent가 하나의 도구만 쓰는 것이 아니라, 여러 도구를 순차적으로 사용할 수 있음을 보여준다.

---

## 13. ReAct와 Agent Loop

Agent Loop는 Agent가 작업을 완료할 때까지 반복하는 실행 구조이다.

```text
while not done:
    LLM이 현재 상태를 보고 다음 행동을 결정한다.

    if tool_call:
        도구를 실행한다.
        도구 결과를 상태에 추가한다.
    else:
        최종 답변을 생성한다.
        종료한다.
```

ReAct 관점으로 표현하면 다음과 같다.

```text
Thought → Action → Observation → Thought → Action → Observation → Final Answer
```

Tool Calling 관점으로 표현하면 다음과 같다.

```text
LLM Response → Tool Call → Tool Result → LLM Response → Final Answer
```

LangChain은 Agent를 모델이 작업을 완료할 때까지 도구를 반복 호출하는 구조로 설명한다.  
이 설명은 ReAct와 Tool Calling을 이해하는 데 매우 유용하다.

---

## 14. Tool Calling이란 무엇인가?

Tool Calling은 LLM이 외부 도구를 호출할 수 있도록 하는 방식이다.

여기서 도구는 다음과 같은 것들이 될 수 있다.

```text
1. Python 함수
2. 검색 함수
3. 계산기
4. 파일 읽기 함수
5. 데이터베이스 조회 함수
6. 외부 API 호출 함수
7. RAG 검색 함수
8. MCP Server가 제공하는 Tool
```

Tool Calling에서 중요한 점은 다음이다.

```text
LLM이 도구를 직접 실행하는 것이 아니다.
LLM은 어떤 도구를 어떤 인자로 호출해야 하는지 구조화된 요청을 만든다.
실제 실행은 애플리케이션 코드가 담당한다.
```

예를 들어 LLM은 다음과 같은 요청을 만들 수 있다.

```json
{
  "tool_name": "search_documents",
  "arguments": {
    "query": "ChromaDB RAG"
  }
}
```

그러면 애플리케이션은 이 요청을 해석해서 실제 함수를 실행한다.

```text
search_documents(query="ChromaDB RAG")
```

그리고 실행 결과를 다시 LLM에게 전달한다.

---

## 15. Function Calling과 Tool Calling의 관계

초기에는 LLM이 외부 함수를 호출하는 기능을 주로 **Function Calling**이라고 불렀다.  
최근에는 더 넓은 의미로 **Tool Calling**이라는 표현을 많이 사용한다.

두 개념의 관계를 정리하면 다음과 같다.

```text
Function Calling:
- LLM이 특정 함수를 호출하도록 구조화된 요청을 생성하는 방식
- 함수 이름과 파라미터가 핵심이다.

Tool Calling:
- Function Calling을 포함하는 더 넓은 개념
- 함수뿐 아니라 검색, 파일, 코드 실행, MCP, 웹 검색, DB 조회 등 다양한 도구를 포함한다.
```

따라서 다음과 같이 이해하면 된다.

```text
Function Calling은 Tool Calling의 한 형태이다.
```

OpenAI 문서에서도 function calling을 tool calling으로 함께 설명하며, 외부 데이터와 시스템을 모델에 연결하는 방식으로 다룬다.  
Anthropic 문서에서도 Claude가 사용자 요청과 도구 설명을 바탕으로 도구 호출 여부를 결정하고, 애플리케이션이 구조화된 호출을 실행하는 방식으로 설명한다.

---

## 16. Tool Calling 기본 흐름

Tool Calling의 기본 흐름은 다음과 같다.

```text
1. 애플리케이션이 LLM에게 도구 목록을 알려준다.
2. 사용자가 질문한다.
3. LLM이 도구 호출이 필요한지 판단한다.
4. 필요하면 도구 이름과 입력값을 생성한다.
5. 애플리케이션이 도구 호출 요청을 검증한다.
6. 애플리케이션이 실제 도구를 실행한다.
7. 도구 실행 결과를 LLM에게 다시 전달한다.
8. LLM이 결과를 바탕으로 최종 답변을 생성한다.
```

그림으로 표현하면 다음과 같다.

```text
사용자
  │
  ▼
Agent Application
  │
  ├─ Tool 목록 전달
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
        ▼
   실제 도구 실행
        │
        ▼
   Tool Result
        │
        ▼
      LLM
        │
        ▼
   Final Answer
```

---

## 17. Tool Schema란 무엇인가?

Tool Schema는 LLM에게 도구 사용 방법을 알려주는 설명서이다.

LLM이 도구를 잘 사용하려면 다음 정보를 알아야 한다.

```text
1. 도구 이름
2. 도구 설명
3. 언제 사용해야 하는지
4. 입력 파라미터
5. 파라미터 타입
6. 필수 파라미터
7. 반환 결과의 의미
8. 사용하면 안 되는 경우
```

예를 들어 문서 검색 도구의 Schema는 다음과 같이 표현할 수 있다.

```json
{
  "name": "search_documents",
  "description": "사내 문서에서 사용자의 질문과 관련된 내용을 검색한다.",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "검색할 질문 또는 키워드"
      },
      "top_k": {
        "type": "integer",
        "description": "가져올 검색 결과 개수"
      }
    },
    "required": ["query"]
  }
}
```

좋은 Tool Schema는 Agent 품질에 큰 영향을 준다.

도구 설명이 모호하면 LLM은 잘못된 도구를 선택할 수 있다.  
파라미터 설명이 부족하면 잘못된 입력값을 만들 수 있다.

---

## 18. 좋은 Tool Schema의 조건

좋은 Tool Schema는 다음 조건을 만족해야 한다.

```text
1. 도구 이름이 명확하다.
2. 도구 설명이 구체적이다.
3. 사용해야 하는 상황이 분명하다.
4. 사용하면 안 되는 상황도 설명한다.
5. 파라미터 타입이 명확하다.
6. 필수값과 선택값이 구분되어 있다.
7. 예시 입력값이 있다.
8. 반환 결과의 의미가 설명되어 있다.
```

좋은 예시는 다음과 같다.

```json
{
  "name": "read_project_text_file",
  "description": "프로젝트 루트 하위의 UTF-8 텍스트 파일을 읽는다. 프로젝트 외부 경로는 읽을 수 없다.",
  "parameters": {
    "type": "object",
    "properties": {
      "relative_path": {
        "type": "string",
        "description": "프로젝트 루트를 기준으로 한 상대 경로. 예: docs/index.md"
      }
    },
    "required": ["relative_path"]
  }
}
```

나쁜 예시는 다음과 같다.

```json
{
  "name": "file",
  "description": "파일 도구",
  "parameters": {}
}
```

나쁜 Schema는 LLM에게 충분한 판단 기준을 제공하지 못한다.

---

## 19. Tool Calling에서 애플리케이션의 역할

Tool Calling에서 가장 중요한 점은 **도구 실행 주체가 LLM이 아니라 애플리케이션**이라는 것이다.

LLM의 역할은 다음과 같다.

```text
1. 도구가 필요한지 판단한다.
2. 어떤 도구를 사용할지 선택한다.
3. 도구 입력값을 생성한다.
4. 도구 결과를 해석한다.
5. 최종 답변을 생성한다.
```

애플리케이션의 역할은 다음과 같다.

```text
1. 도구 목록을 관리한다.
2. Tool Schema를 LLM에게 전달한다.
3. LLM의 Tool Call 요청을 파싱한다.
4. 허용된 도구인지 검증한다.
5. 입력값을 검증한다.
6. 실제 도구를 실행한다.
7. 실행 결과를 LLM에게 전달한다.
8. 도구 실행 로그를 남긴다.
```

이 구분이 매우 중요하다.

```text
LLM은 판단한다.
Application은 실행한다.
Tool은 실제 작업을 수행한다.
```

---

## 20. Tool Calling과 RAG의 관계

RAG는 Agent가 사용할 수 있는 대표적인 도구이다.

Step2에서 만든 RAG 구조는 다음과 같았다.

```text
사용자 질문
   ↓
Embedding
   ↓
Vector DB 검색
   ↓
관련 문서 Chunk 조회
   ↓
LLM 답변 생성
```

Agent 관점에서는 이 전체 과정을 하나의 Tool로 만들 수 있다.

```text
Tool Name:
search_rag_documents

Input:
query

Output:
관련 문서 Chunk 목록
```

Agent는 사용자의 질문을 보고 RAG 검색이 필요하다고 판단하면 이 도구를 호출한다.

```text
사용자:
"Step2 문서에서 ChromaDB 관련 내용을 찾아줘."

Agent Thought:
사내 문서 검색이 필요하다.

Tool Call:
search_rag_documents(query="ChromaDB Step2 RAG")

Tool Result:
관련 문서 Chunk 목록

Final Answer:
검색 결과를 바탕으로 답변 생성
```

따라서 RAG와 Agent의 관계는 다음처럼 이해하면 된다.

```text
RAG는 문서를 검색하는 능력이다.
Agent는 언제 RAG를 사용할지 판단하는 실행 주체이다.
```

---

## 21. Tool Calling과 MCP의 관계

MCP는 Model Context Protocol의 약자이다.

Tool Calling은 LLM이 도구를 호출하는 개념이다.  
MCP는 이러한 도구와 외부 시스템 연결을 표준화하는 구조이다.

단순 Tool Calling에서는 애플리케이션 내부에 도구가 직접 등록될 수 있다.

```text
Agent Application
  ├─ calculator 함수
  ├─ file_reader 함수
  └─ search_documents 함수
```

하지만 Enterprise 환경에서는 도구가 많아진다.

```text
파일 시스템
DB
Git
Jira
Confluence
메일
캘린더
RAG
업무 API
```

각 시스템을 매번 다른 방식으로 연결하면 복잡해진다.

MCP를 사용하면 다음처럼 표준화할 수 있다.

```text
Agent
  ↓
MCP Client
  ↓
MCP Server
  ↓
외부 시스템
```

즉, MCP는 Tool Calling을 확장하기 위한 표준 연결 계층으로 볼 수 있다.

Step3에서는 먼저 Tool Calling을 이해하고, 이후 Step3-7과 Step3-8에서 MCP로 확장한다.

---

## 22. ReAct와 Tool Calling의 관계

ReAct와 Tool Calling은 서로 다른 개념이지만 함께 사용된다.

```text
ReAct:
Agent의 사고/행동 패턴

Tool Calling:
행동을 실제 도구 호출로 구현하는 방식
```

예를 들어 ReAct 관점의 Action은 다음과 같다.

```text
Action:
search_documents
```

Tool Calling 관점에서는 다음처럼 구조화된다.

```json
{
  "tool_name": "search_documents",
  "arguments": {
    "query": "AI Agent 개요"
  }
}
```

즉, ReAct의 Action이 실제 시스템에서는 Tool Call로 표현된다.

관계를 정리하면 다음과 같다.

```text
Thought:
LLM이 다음 행동을 판단한다.

Action:
사용할 도구를 결정한다.

Tool Call:
도구 이름과 입력값을 구조화한다.

Tool Execution:
애플리케이션이 실제 도구를 실행한다.

Observation:
도구 실행 결과를 LLM에게 전달한다.

Final Answer:
LLM이 최종 답변을 생성한다.
```

---

## 23. Agent Prompt 설계 기본

ReAct와 Tool Calling을 사용하려면 Prompt도 중요하다.

Agent Prompt에는 보통 다음 내용이 포함된다.

```text
1. Agent의 역할
2. 사용할 수 있는 도구 목록
3. 도구 사용 기준
4. 도구 사용 금지 조건
5. 답변 형식
6. 출처 표시 방식
7. 오류 발생 시 처리 방식
8. 보안 규칙
```

예시는 다음과 같다.

```text
너는 AI DATA Platform 프로젝트의 학습 도우미이다.

사용자의 질문에 답변할 때 다음 규칙을 따른다.

1. 문서 검색이 필요한 경우 search_documents 도구를 사용한다.
2. 계산이 필요한 경우 calculator 도구를 사용한다.
3. 파일 내용 확인이 필요한 경우 read_text_file 도구를 사용한다.
4. 도구 결과에 없는 내용은 추측하지 않는다.
5. 답변 마지막에는 사용한 도구와 근거를 요약한다.
6. 파일 삭제, DB 수정, 외부 전송 작업은 수행하지 않는다.
```

Prompt는 Agent의 행동을 제어하는 중요한 장치이다.

---

## 24. 도구 선택 기준

Agent가 모든 질문에 도구를 사용할 필요는 없다.

도구가 필요한 경우는 다음과 같다.

```text
1. 최신 정보가 필요한 경우
2. 사내 문서 검색이 필요한 경우
3. 로컬 파일을 읽어야 하는 경우
4. 정확한 계산이 필요한 경우
5. 데이터베이스 조회가 필요한 경우
6. 외부 API 호출이 필요한 경우
7. 이전 실행 결과 확인이 필요한 경우
```

도구가 필요 없는 경우는 다음과 같다.

```text
1. 일반 개념 설명
2. 단순 문장 다듬기
3. 사용자가 이미 제공한 텍스트 요약
4. 일반적인 프로그래밍 문법 설명
5. 창의적 글쓰기
```

도구 사용 기준이 없으면 Agent가 불필요하게 도구를 호출하거나, 반대로 필요한 도구를 호출하지 않을 수 있다.

---

## 25. 읽기 도구와 쓰기 도구

Enterprise 환경에서는 도구를 반드시 읽기 도구와 쓰기 도구로 나누어야 한다.

```text
읽기 도구:
- 문서 검색
- 파일 읽기
- DB 조회
- 상태 확인
- 로그 조회

쓰기 도구:
- 파일 생성
- 파일 수정
- DB 변경
- 메일 발송
- 티켓 생성
- 배포 실행
```

처음 Agent를 만들 때는 읽기 도구부터 시작하는 것이 안전하다.

쓰기 도구는 반드시 추가 통제를 둬야 한다.

```text
1. 사용자 확인
2. 승인 절차
3. 권한 검사
4. 실행 전 Preview
5. 실행 로그
6. 취소 또는 복구 방법
```

---

## 26. Tool Calling 보안 원칙

Tool Calling은 강력하지만 위험할 수 있다.

특히 다음 도구는 신중하게 다뤄야 한다.

```text
1. Shell 명령 실행 도구
2. 파일 삭제 도구
3. DB 수정 도구
4. 메일 발송 도구
5. 외부 API 호출 도구
6. 배포 실행 도구
7. 결제 또는 계약 관련 도구
```

보안 원칙은 다음과 같다.

```text
1. 허용된 도구만 등록한다.
2. 사용자 권한에 따라 도구 사용 가능 여부를 판단한다.
3. 도구 입력값을 반드시 검증한다.
4. 프로젝트 외부 파일 접근을 제한한다.
5. 민감정보를 로그에 그대로 남기지 않는다.
6. 쓰기 작업은 실행 전 확인 절차를 둔다.
7. 모든 도구 실행 이력을 기록한다.
8. 실패했을 때 안전하게 중단한다.
```

---

## 27. Tool Calling 로그 설계

Agent가 도구를 사용하면 반드시 로그를 남겨야 한다.

로그에는 다음 정보가 포함되는 것이 좋다.

```text
1. 실행 시간
2. 사용자
3. 세션 ID
4. 도구 이름
5. 입력 파라미터
6. 실행 결과 상태
7. 오류 메시지
8. 실행 시간
9. 승인 여부
10. 최종 답변 ID
```

예시는 다음과 같다.

```json
{
  "timestamp": "2026-06-29T10:30:00+09:00",
  "user_id": "user001",
  "session_id": "session-20260629-001",
  "tool_name": "search_documents",
  "arguments": {
    "query": "ChromaDB RAG"
  },
  "status": "success",
  "elapsed_ms": 351,
  "approval_required": false
}
```

로그는 다음 목적에 사용된다.

```text
1. 장애 분석
2. 보안 감사
3. 사용량 분석
4. Agent 품질 개선
5. 비용 최적화
6. 문제 재현
```

---

## 28. ReAct / Tool Calling 설계 시 자주 하는 실수

---

### 28.1 도구를 너무 많이 등록한다

도구가 너무 많으면 LLM이 어떤 도구를 선택해야 할지 혼란스러워질 수 있다.

처음에는 최소한의 도구만 등록하는 것이 좋다.

```text
1. calculator
2. search_documents
3. read_text_file
```

이후 필요에 따라 도구를 추가한다.

---

### 28.2 도구 설명이 모호하다

나쁜 설명:

```text
문서를 처리하는 도구입니다.
```

좋은 설명:

```text
프로젝트 내부 Markdown 문서에서 질문과 관련된 내용을 검색한다. 문서 원문 전체를 읽는 것이 아니라 검색 결과 Chunk를 반환한다.
```

도구 설명은 LLM의 선택 품질에 직접 영향을 준다.

---

### 28.3 도구 실행 결과를 그대로 믿는다

도구 결과도 오류가 있을 수 있다.

```text
1. 검색 결과가 부족할 수 있다.
2. 파일이 오래되었을 수 있다.
3. DB 조회 조건이 잘못되었을 수 있다.
4. API 응답이 실패했을 수 있다.
```

따라서 Agent는 도구 결과를 확인하고, 부족하면 추가 검색이나 사용자 확인을 해야 한다.

---

### 28.4 쓰기 도구를 바로 실행한다

메일 발송, DB 수정, 파일 삭제 같은 작업은 바로 실행하면 위험하다.

좋은 흐름은 다음과 같다.

```text
1. Agent가 실행 계획을 만든다.
2. 사용자에게 Preview를 보여준다.
3. 사용자가 승인한다.
4. 실제 도구를 실행한다.
5. 실행 결과를 보고한다.
```

---

## 29. Step3-3 구현으로 이어지는 설계

이번 문서에서는 실제 코드를 많이 작성하지 않는다.  
하지만 다음 단계에서 구현할 구조를 미리 이해해야 한다.

Step3-3에서는 다음 파일을 만들게 된다.

```text
labs/agent
├── tools
│   ├── calculator.py
│   ├── search.py
│   └── file_reader.py
│
├── common
│   ├── tool_registry.py
│   └── tool_executor.py
│
├── 01_first_agent.py
└── 02_tool_calling.py
```

각 파일의 역할은 다음과 같다.

```text
calculator.py:
계산 도구

search.py:
간단한 문서 검색 도구

file_reader.py:
프로젝트 내부 텍스트 파일 읽기 도구

tool_registry.py:
사용 가능한 도구 목록과 Schema 관리

tool_executor.py:
Tool Call 요청을 받아 실제 도구 실행

01_first_agent.py:
가장 단순한 Agent 실행 흐름

02_tool_calling.py:
Tool Calling 기반 Agent 실행 흐름
```

Step3-3에서 구현할 전체 구조는 다음과 같다.

```text
사용자 질문
   ↓
Agent Prompt + Tool Schema
   ↓
LLM 또는 규칙 기반 판단
   ↓
Tool Call 생성
   ↓
Tool Executor
   ↓
Tool Result
   ↓
최종 답변 생성
```

---

## 30. 핵심 정리

이번 문서의 핵심은 다음과 같다.

```text
1. Chain of Thought는 생각 중심이고, ReAct는 생각과 행동을 함께 다룬다.
2. ReAct는 Thought, Action, Observation을 반복하는 Agent 패턴이다.
3. Tool Calling은 ReAct의 Action을 실제 도구 호출로 구현하는 방법이다.
4. LLM은 도구를 직접 실행하지 않고, 도구 호출 요청을 생성한다.
5. 실제 도구 실행은 애플리케이션의 Tool Executor가 담당한다.
6. Tool Schema는 LLM에게 도구 사용법을 알려주는 설명서이다.
7. RAG는 Agent가 사용할 수 있는 중요한 검색 도구이다.
8. MCP는 Tool Calling을 외부 시스템 연동 구조로 확장하는 표준 계층이다.
9. Enterprise 환경에서는 도구 권한, 입력 검증, 로그, 승인 절차가 중요하다.
10. Step3-3에서는 이번 개념을 바탕으로 첫 번째 Agent를 Python으로 구현한다.
```

한 문장으로 정리하면 다음과 같다.

> **ReAct는 Agent가 생각하고 행동하는 패턴이고, Tool Calling은 그 행동을 실제 도구 실행으로 연결하는 방식이다.**

---

## 31. 다음 단계 예고

다음 문서는 다음과 같다.

```text
Step3-3. 첫 번째 AI Agent 구현
docs/study/step3/step3_3_first_ai_agent_guide.md
```

다음 단계에서는 이번 문서에서 배운 개념을 바탕으로 Python으로 직접 Agent 구조를 구현한다.

다음 문서에서 다룰 내용은 다음과 같다.

```text
1. 실습 디렉터리 생성
2. calculator 도구 구현
3. search 도구 구현
4. file_reader 도구 구현
5. Tool Registry 구현
6. Tool Executor 구현
7. 첫 번째 Agent 실행
8. Tool Calling 흐름 확인
9. 코드 상세 주석 분석
```

---

## 32. 참고 자료

아래 자료는 ReAct와 Tool Calling 개념을 이해하기 위한 참고 자료이다.

```text
ReAct: Synergizing Reasoning and Acting in Language Models
https://arxiv.org/abs/2210.03629

Google Research Blog - ReAct: Synergizing Reasoning and Acting in Language Models
https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/

OpenAI Function Calling Guide
https://developers.openai.com/api/docs/guides/function-calling

Anthropic Tool Use Documentation
https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview

LangChain Agents Documentation
https://docs.langchain.com/oss/python/langchain/agents

LangChain Tools Documentation
https://docs.langchain.com/oss/python/langchain/tools

Model Context Protocol 공식 문서
https://modelcontextprotocol.io/docs/getting-started/intro
```

---

## 33. 부록: 용어 정리

| 용어 | 설명 |
|---|---|
| LLM | Large Language Model. 자연어를 이해하고 생성하는 모델 |
| Agent | 목표를 달성하기 위해 판단하고 도구를 사용하는 실행 구조 |
| ReAct | Reasoning과 Acting을 결합한 Agent 동작 패턴 |
| Thought | Agent가 다음 행동을 판단하는 사고 단계 |
| Action | Agent가 선택한 행동 또는 도구 호출 |
| Observation | 도구 실행 결과를 관찰하는 단계 |
| Tool Calling | LLM이 외부 도구 호출 요청을 구조화해서 생성하는 방식 |
| Function Calling | Tool Calling의 한 형태로, 특정 함수를 호출하는 방식 |
| Tool Schema | 도구 이름, 설명, 입력값을 정의한 도구 사용 설명서 |
| Tool Executor | Tool Call 요청을 받아 실제 도구를 실행하는 애플리케이션 구성 요소 |
| RAG | 문서 검색 결과를 LLM 답변에 활용하는 구조 |
| MCP | 외부 시스템과 AI 애플리케이션 연결을 표준화하는 프로토콜 |

---
