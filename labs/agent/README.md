# Step3-3. 첫 번째 AI Agent 구현 실습 패키지

이 실습 패키지는 `Step3-3. 첫 번째 AI Agent 구현 가이드` 문서에 맞춰 바로 실행할 수 있도록 구성한 예제 코드와 실습 데이터입니다.

## 1. 실습 목표

이번 실습의 목표는 LLM API를 바로 연결하기 전에, AI Agent의 기본 실행 흐름을 Python 코드로 이해하는 것입니다.

핵심 흐름은 다음과 같습니다.

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

## 2. 디렉터리 구조

```text
labs/agent
├── README.md
├── 01_first_agent.py
├── 02_tool_calling.py
├── 03_sample_data_search.py
│
├── tools
│   ├── __init__.py
│   ├── calculator.py
│   ├── search.py
│   ├── file_reader.py
│   └── employee_search.py
│
├── common
│   ├── __init__.py
│   ├── tool_registry.py
│   └── tool_executor.py
│
├── sample_docs
│   ├── agent_sample.md
│   ├── rag_intro.md
│   ├── react.md
│   ├── tool_calling.md
│   ├── company_policy.md
│   └── ai_platform.md
│
└── sample_data
    └── employees.json
```

## 3. 실행 방법

프로젝트 루트에서 실행하는 경우:

```bash
PYTHONPATH=./labs/agent python labs/agent/01_first_agent.py
```

또는 `labs/agent` 디렉터리로 이동해서 실행합니다.

```bash
cd labs/agent
python 01_first_agent.py
python 02_tool_calling.py
python 03_sample_data_search.py
```

## 4. 테스트 입력 예시

`01_first_agent.py` 실행 후 아래 문장을 입력해보세요.

```text
12500 * 17 계산해줘
Agent 검색해줘
파일 읽어줘
김철수 직원 찾아줘
AI플랫폼 부서 직원 찾아줘
```

## 5. 학습 포인트

- Python 함수 하나가 Agent Tool이 될 수 있다.
- Tool Registry는 도구 이름과 실제 함수를 연결한다.
- Tool Executor는 Tool Call 요청을 받아 실제 도구를 실행한다.
- ReAct의 Action은 코드에서는 Tool Call dictionary로 표현할 수 있다.
- Observation은 Tool 실행 결과이다.
