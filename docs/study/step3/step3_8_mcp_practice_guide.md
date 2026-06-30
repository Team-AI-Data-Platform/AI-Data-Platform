# Step3-8. MCP 기반 외부 시스템 연동 실습 가이드

> AI DATA Platform 연구 프로젝트  
> Step3. AI Agent  
> Part2. AI Agent 심화  
> 문서 경로: `docs/study/step3/step3_8_mcp_practice_guide.md`  
> 작성일: 2026-06-30

---

## 1. 문서 목적

이 문서는 `Step3-7. MCP 아키텍처 이해`에서 학습한 MCP 개념을 바탕으로, Python을 사용하여 **MCP Server와 MCP Client를 직접 구현하고 외부 시스템을 Agent 도구로 연결하는 실습 가이드**이다.

Step3-7에서는 MCP를 다음과 같이 이해했다.

```text
MCP = AI Agent가 외부 시스템의 Tool, Resource, Prompt를 표준 방식으로 사용할 수 있게 해주는 연결 프로토콜
```

이번 Step3-8에서는 이 개념을 실제 코드로 옮긴다.

이번 문서에서 다룰 외부 시스템은 다음 네 가지이다.

```text
1. File
2. RAG
3. Database
4. API
```

처음부터 실제 운영 시스템을 연결하지는 않는다. 대신 실습용 샘플 파일, 샘플 문서, SQLite DB, Mock API 데이터를 만들어 MCP Tool로 감싸는 방식으로 진행한다.

이번 문서의 핵심은 다음 한 문장으로 요약할 수 있다.

> **Step3-8의 목표는 File, RAG, DB, API 기능을 MCP Server의 Tool로 제공하고, Agent가 MCP Client를 통해 호출하는 구조를 이해하는 것이다.**

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
│   └─ Step3-8. MCP 기반 외부 시스템 연동   ← 현재 문서
│
└─ Part3. Enterprise AI Agent
    ├─ Step3-9. Multi Agent 협업
    └─ Step3-10. Enterprise AI Agent Platform
```

Step3-8은 Part2의 마지막 단계이다.

```text
Step3-5:
복잡한 작업을 계획하고 Workflow로 나눈다.

Step3-6:
Workflow를 LangGraph로 제어한다.

Step3-7:
외부 시스템 연동 표준인 MCP 아키텍처를 이해한다.

Step3-8:
MCP Server와 MCP Client를 구현하고 File, RAG, DB, API를 연결한다.
```

즉, Step3-8은 Part3의 Multi Agent와 Enterprise Agent Platform으로 넘어가기 위한 실습 기반이다.

---

## 3. 학습 목표

이 문서를 마치면 다음 내용을 직접 설명하고 실행할 수 있어야 한다.

```text
1. MCP Python SDK를 설치할 수 있다.
2. FastMCP를 사용하여 첫 번째 MCP Server를 만들 수 있다.
3. MCP Tool을 정의하고 호출할 수 있다.
4. File Tool을 MCP Server에 등록할 수 있다.
5. RAG 검색 기능을 MCP Tool로 감쌀 수 있다.
6. SQLite DB 조회 기능을 MCP Tool로 감쌀 수 있다.
7. Mock API 데이터를 MCP Tool로 제공할 수 있다.
8. MCP Client에서 MCP Server의 Tool 목록을 조회할 수 있다.
9. MCP Client에서 Tool을 호출할 수 있다.
10. Agent 구조에서 MCP Tool을 호출하는 흐름을 이해할 수 있다.
11. LangGraph Node에서 MCP Tool을 호출하는 확장 방향을 이해할 수 있다.
12. Enterprise 환경에서 MCP Tool 보안 원칙을 설명할 수 있다.
```

---

## 4. 실습 범위

MCP Server는 다음 기능을 제공할 수 있다.

```text
1. Tools
2. Resources
3. Prompts
```

이번 Step3-8에서는 **Tools 중심**으로 실습한다.

```text
이번 실습의 중심:
MCP Tools

개념만 확인:
MCP Resources
MCP Prompts
```

이유는 다음과 같다.

```text
1. Step3-2에서 학습한 Tool Calling과 바로 연결된다.
2. Step3-3에서 만든 Tool Executor 개념과 연결된다.
3. File, RAG, DB, API 기능을 Tool로 감싸기 쉽다.
4. Agent가 외부 시스템을 호출하는 흐름을 가장 빨리 확인할 수 있다.
```

이번 실습의 핵심 흐름은 다음과 같다.

```text
Agent
  ↓
MCP Client
  ↓
MCP Server
  ↓
Tool
  ↓
File / RAG / DB / API
```

---

## 5. Transport 선택

MCP는 여러 Transport를 사용할 수 있다.

대표적으로 다음이 있다.

```text
1. stdio
2. Streamable HTTP
3. SSE
```

이번 실습에서는 `stdio` 중심으로 진행한다.

이유는 다음과 같다.

```text
1. 로컬 실습에 적합하다.
2. 별도 웹 서버 배포가 필요 없다.
3. 처음 MCP 구조를 이해하기 쉽다.
4. Python 프로세스 하나로 Server를 실행할 수 있다.
```

운영 환경 또는 여러 사용자가 함께 사용하는 환경에서는 Streamable HTTP 구조를 검토할 수 있다.

정리하면 다음과 같다.

| 구분 | 적합한 상황 |
|---|---|
| stdio | 로컬 실습, 개발자 PC, 간단한 서버 실행 |
| Streamable HTTP | 사내 서버, 여러 사용자, 운영 환경 |
| SSE | 일부 기존 예제나 레거시 환경 |

이번 실습에서는 안전하게 `stdio` 기반부터 시작한다.

---

## 6. 최종 실습 디렉터리 구조

이번 실습의 최종 디렉터리 구조는 다음과 같다.

```text
labs
└── mcp
    ├── README.md
    ├── requirements.txt
    │
    ├── servers
    │   ├── 01_first_mcp_server.py
    │   ├── 02_file_mcp_server.py
    │   ├── 03_rag_mcp_server.py
    │   ├── 04_database_mcp_server.py
    │   ├── 05_api_mcp_server.py
    │   └── 06_all_tools_mcp_server.py
    │
    ├── clients
    │   ├── 01_manual_test_client.md
    │   ├── 02_first_mcp_client.py
    │   └── 03_agent_with_mcp.py
    │
    ├── sample_docs
    │   ├── agent.md
    │   ├── rag.md
    │   ├── langgraph.md
    │   └── mcp.md
    │
    ├── sample_data
    │   ├── employees.json
    │   ├── products.json
    │   ├── orders.json
    │   └── sample_api.json
    │
    ├── database
    │   ├── create_sample_db.py
    │   └── sample.db
    │
    └── config
        └── mcp_config.json
```

이번 문서에서는 위 구조를 기준으로 설명한다.

---

## 7. 실습 준비

프로젝트 루트에서 아래 명령으로 디렉터리를 만든다.

```bash
mkdir -p labs/mcp/servers
mkdir -p labs/mcp/clients
mkdir -p labs/mcp/sample_docs
mkdir -p labs/mcp/sample_data
mkdir -p labs/mcp/database
mkdir -p labs/mcp/config
```

가상환경을 사용하는 것을 권장한다.

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell에서는 다음과 같이 활성화한다.

```powershell
.venv\Scripts\Activate.ps1
```

패키지를 설치한다.

```bash
python -m pip install --upgrade pip
python -m pip install "mcp[cli]"
```

설치 확인은 다음과 같이 한다.

```bash
python -c "import mcp; print('mcp installed')"
```

---

## 8. requirements.txt

파일 경로:

```text
labs/mcp/requirements.txt
```

내용:

```text
mcp[cli]
```

SQLite는 Python 표준 라이브러리의 `sqlite3`를 사용하므로 별도 설치가 필요 없다.

이번 실습에서는 복잡한 RAG 라이브러리를 바로 붙이지 않고, Markdown 문서에 대한 단순 키워드 검색으로 RAG MCP Tool의 개념을 먼저 확인한다.

이후 Step2에서 만든 ChromaDB 기반 RAG 검색 코드와 연결할 수 있다.

---

# Part A. 샘플 데이터 준비

## 9. 샘플 문서 만들기

파일 경로:

```text
labs/mcp/sample_docs/agent.md
```

내용:

```markdown
# AI Agent

AI Agent는 사용자의 목표를 이해하고 필요한 도구를 선택하여 작업을 수행하는 AI 시스템이다.

Agent는 LLM, Tool, Memory, Planner, Executor로 구성될 수 있다.

단순 Chatbot이 답변 중심이라면 Agent는 판단과 실행 중심이다.
```

파일 경로:

```text
labs/mcp/sample_docs/rag.md
```

내용:

```markdown
# RAG

RAG는 Retrieval Augmented Generation의 약자이다.

외부 문서를 검색하여 LLM 답변의 근거로 활용하는 구조이다.

AI Agent에서는 RAG 검색 기능이 하나의 Tool로 사용될 수 있다.
```

파일 경로:

```text
labs/mcp/sample_docs/langgraph.md
```

내용:

```markdown
# LangGraph

LangGraph는 Agent Workflow를 State, Node, Edge 기반 Graph 구조로 제어하는 프레임워크이다.

복잡한 Agent 흐름, 조건 분기, 반복 실행, Human-in-the-Loop 구조를 표현하는 데 유용하다.
```

파일 경로:

```text
labs/mcp/sample_docs/mcp.md
```

내용:

```markdown
# MCP

MCP는 Model Context Protocol의 약자이다.

LLM 애플리케이션과 외부 시스템을 표준 방식으로 연결하기 위한 프로토콜이다.

MCP Server는 Tools, Resources, Prompts를 제공할 수 있다.
```

---

## 10. 샘플 JSON 데이터 만들기

파일 경로:

```text
labs/mcp/sample_data/employees.json
```

내용:

```json
[
  {
    "id": 1,
    "name": "김철수",
    "department": "AI플랫폼",
    "role": "AI Engineer",
    "skills": ["Python", "RAG", "Agent"]
  },
  {
    "id": 2,
    "name": "이영희",
    "department": "R&D",
    "role": "Data Scientist",
    "skills": ["Python", "Pandas", "Machine Learning"]
  },
  {
    "id": 3,
    "name": "박민수",
    "department": "플랫폼개발",
    "role": "Backend Developer",
    "skills": ["FastAPI", "Docker", "PostgreSQL"]
  }
]
```

파일 경로:

```text
labs/mcp/sample_data/products.json
```

내용:

```json
[
  {
    "id": 101,
    "name": "AI 문서 검색 서비스",
    "category": "RAG",
    "price": 3000000
  },
  {
    "id": 102,
    "name": "Agent Workflow PoC",
    "category": "Agent",
    "price": 5000000
  },
  {
    "id": 103,
    "name": "MCP 연동 모듈",
    "category": "MCP",
    "price": 4000000
  }
]
```

파일 경로:

```text
labs/mcp/sample_data/orders.json
```

내용:

```json
[
  {
    "order_id": "ORD-001",
    "product_id": 101,
    "customer": "A은행",
    "amount": 3000000
  },
  {
    "order_id": "ORD-002",
    "product_id": 102,
    "customer": "B증권",
    "amount": 5000000
  },
  {
    "order_id": "ORD-003",
    "product_id": 103,
    "customer": "C카드",
    "amount": 4000000
  }
]
```

파일 경로:

```text
labs/mcp/sample_data/sample_api.json
```

내용:

```json
{
  "platform_status": {
    "open_webui": "running",
    "ollama": "running",
    "chroma_db": "ready",
    "last_checked": "2026-06-30T10:00:00+09:00"
  },
  "notices": [
    {
      "id": 1,
      "title": "AI DATA Platform 점검 완료",
      "level": "info"
    },
    {
      "id": 2,
      "title": "RAG 인덱스 재생성 필요",
      "level": "warning"
    }
  ]
}
```

---

# Part B. 첫 번째 MCP Server

## 11. 첫 번째 MCP Server 만들기

파일 경로:

```text
labs/mcp/servers/01_first_mcp_server.py
```

코드:

```python
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("first-mcp-server")


@mcp.tool()
def hello(name: str) -> str:
    \"\"\"
    이름을 입력받아 인사말을 반환한다.
    \"\"\"
    return f"안녕하세요, {name}님. 첫 번째 MCP Tool 호출에 성공했습니다."


@mcp.tool()
def add(a: int, b: int) -> int:
    \"\"\"
    두 숫자를 더한다.
    \"\"\"
    return a + b


if __name__ == "__main__":
    mcp.run()
```

이 서버는 두 개의 Tool을 제공한다.

```text
hello
add
```

이 예제의 목적은 MCP Server가 Python 함수 하나를 Tool로 노출할 수 있다는 점을 확인하는 것이다.

---

## 12. MCP Inspector로 확인

`mcp[cli]`를 설치했다면 MCP Inspector를 사용할 수 있다.

```bash
cd labs/mcp
mcp dev servers/01_first_mcp_server.py
```

Inspector에서 확인할 수 있는 것은 다음과 같다.

```text
1. Server 연결 여부
2. Tool 목록
3. Tool 입력 Schema
4. Tool 호출 결과
5. 오류 메시지
```

처음 MCP Server를 만들 때는 Inspector로 확인하는 것을 권장한다.

---

# Part C. File MCP Server

## 13. File MCP Server 목표

File MCP Server의 목표는 프로젝트 내부 파일을 읽는 기능을 MCP Tool로 제공하는 것이다.

이번 실습에서는 다음 Tool을 만든다.

```text
list_sample_docs:
sample_docs 디렉터리의 Markdown 파일 목록 조회

read_sample_doc:
sample_docs 디렉터리의 Markdown 파일 읽기
```

보안상 중요한 점은 다음이다.

```text
1. sample_docs 디렉터리 밖의 파일은 읽지 않는다.
2. Markdown 파일만 읽는다.
3. 상대 경로에 ../ 같은 경로 탈출이 들어오면 차단한다.
```

---

## 14. File MCP Server 코드

파일 경로:

```text
labs/mcp/servers/02_file_mcp_server.py
```

코드:

```python
from pathlib import Path

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("file-mcp-server")

BASE_DIR = Path(__file__).resolve().parents[1]
SAMPLE_DOCS_DIR = BASE_DIR / "sample_docs"


def resolve_doc_path(filename: str) -> Path:
    \"\"\"
    sample_docs 내부의 Markdown 파일 경로만 허용한다.
    \"\"\"
    if not filename or not filename.strip():
        raise ValueError("파일명이 비어 있습니다.")

    if "/" in filename or "\\\\" in filename or ".." in filename:
        raise ValueError("파일명에는 경로 문자를 사용할 수 없습니다.")

    path = (SAMPLE_DOCS_DIR / filename).resolve()

    if not str(path).startswith(str(SAMPLE_DOCS_DIR.resolve())):
        raise ValueError("sample_docs 디렉터리 밖의 파일은 읽을 수 없습니다.")

    if path.suffix != ".md":
        raise ValueError("Markdown 파일만 읽을 수 있습니다.")

    if not path.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {filename}")

    return path


@mcp.tool()
def list_sample_docs() -> list[str]:
    \"\"\"
    sample_docs 디렉터리에 있는 Markdown 파일 목록을 반환한다.
    \"\"\"
    return sorted(path.name for path in SAMPLE_DOCS_DIR.glob("*.md"))


@mcp.tool()
def read_sample_doc(filename: str) -> str:
    \"\"\"
    sample_docs 디렉터리의 Markdown 파일 내용을 읽는다.
    \"\"\"
    path = resolve_doc_path(filename)
    return path.read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run()
```

---

## 15. File MCP Server 확인

Inspector로 실행한다.

```bash
cd labs/mcp
mcp dev servers/02_file_mcp_server.py
```

Tool 목록에서 다음이 보이면 정상이다.

```text
list_sample_docs
read_sample_doc
```

테스트 예시는 다음과 같다.

```json
{
  "filename": "mcp.md"
}
```

예상 결과:

```text
# MCP
...
```

---

# Part D. RAG MCP Server

## 16. RAG MCP Server 목표

이번 실습의 RAG MCP Server는 간단한 키워드 검색으로 구현한다.

실제 RAG라면 다음이 필요하다.

```text
1. 문서 Chunk
2. Embedding Model
3. Vector DB
4. Similarity Search
```

하지만 Step3-8의 목적은 MCP 구조를 이해하는 것이므로, 처음에는 단순 검색으로 시작한다.

이번 Tool은 다음과 같다.

```text
search_docs:
sample_docs Markdown 문서에서 키워드를 검색한다.
```

이후 Step2에서 만든 ChromaDB 검색 함수를 이 Tool 내부로 교체하면 실제 RAG MCP Server로 확장할 수 있다.

---

## 17. RAG MCP Server 코드

파일 경로:

```text
labs/mcp/servers/03_rag_mcp_server.py
```

코드:

```python
from pathlib import Path

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("rag-mcp-server")

BASE_DIR = Path(__file__).resolve().parents[1]
SAMPLE_DOCS_DIR = BASE_DIR / "sample_docs"


@mcp.tool()
def search_docs(query: str, top_k: int = 3) -> list[dict[str, str]]:
    \"\"\"
    sample_docs Markdown 문서에서 query가 포함된 문서를 검색한다.

    실제 운영 RAG에서는 이 부분을 Embedding + Vector DB 검색으로 교체할 수 있다.
    \"\"\"
    if not query or not query.strip():
        raise ValueError("검색어가 비어 있습니다.")

    query_lower = query.lower()
    results: list[dict[str, str]] = []

    for path in sorted(SAMPLE_DOCS_DIR.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        content_lower = content.lower()

        if query_lower in content_lower or query_lower in path.stem.lower():
            preview = content.replace("\\n", " ").strip()

            if len(preview) > 200:
                preview = preview[:200] + "..."

            results.append(
                {
                    "filename": path.name,
                    "title": path.stem,
                    "preview": preview,
                }
            )

    return results[:top_k]


if __name__ == "__main__":
    mcp.run()
```

---

## 18. RAG MCP Server 확인

Inspector로 실행한다.

```bash
cd labs/mcp
mcp dev servers/03_rag_mcp_server.py
```

테스트 입력:

```json
{
  "query": "Agent",
  "top_k": 3
}
```

예상 결과:

```text
agent.md
rag.md
```

검색어를 바꿔 테스트한다.

```json
{
  "query": "LangGraph",
  "top_k": 3
}
```

예상 결과:

```text
langgraph.md
```

---

## 19. 실제 ChromaDB RAG로 확장하는 방향

Step2에서 만든 RAG 검색 함수가 있다고 가정하자.

예를 들어 다음 함수가 있다고 하자.

```python
def search_documents(query: str, top_k: int = 3) -> list[dict]:
    ...
```

그러면 MCP Tool은 다음처럼 감쌀 수 있다.

```python
@mcp.tool()
def search_rag_documents(query: str, top_k: int = 3) -> list[dict]:
    return search_documents(query=query, top_k=top_k)
```

즉, 기존 RAG 코드를 크게 바꾸지 않아도 된다.

```text
기존 RAG 함수
   ↓
MCP Tool Wrapper
   ↓
MCP Server
   ↓
Agent에서 표준 방식으로 호출
```

이것이 MCP의 장점이다.

---

# Part E. Database MCP Server

## 20. SQLite 샘플 DB 만들기

이번 실습에서는 SQLite를 사용한다.

SQLite는 Python 표준 라이브러리로 사용할 수 있고, 별도 DB 서버가 필요 없다.

파일 경로:

```text
labs/mcp/database/create_sample_db.py
```

코드:

```python
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "sample.db"


def main() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        \"\"\"
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            role TEXT NOT NULL
        )
        \"\"\"
    )

    cursor.execute(
        \"\"\"
        CREATE TABLE projects (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            status TEXT NOT NULL
        )
        \"\"\"
    )

    cursor.executemany(
        "INSERT INTO employees VALUES (?, ?, ?, ?)",
        [
            (1, "김철수", "AI플랫폼", "AI Engineer"),
            (2, "이영희", "R&D", "Data Scientist"),
            (3, "박민수", "플랫폼개발", "Backend Developer"),
        ],
    )

    cursor.executemany(
        "INSERT INTO projects VALUES (?, ?, ?, ?)",
        [
            (1, "Local LLM 구축", "LLM", "done"),
            (2, "RAG 실습", "RAG", "done"),
            (3, "AI Agent 연구", "Agent", "in_progress"),
            (4, "MCP 연동", "MCP", "planned"),
        ],
    )

    conn.commit()
    conn.close()

    print(f"DB 생성 완료: {DB_PATH}")


if __name__ == "__main__":
    main()
```

실행:

```bash
cd labs/mcp
python database/create_sample_db.py
```

---

## 21. DB MCP Server 목표

DB MCP Server는 SQLite DB를 조회하는 Tool을 제공한다.

이번 실습에서는 읽기 전용 Tool만 만든다.

```text
list_tables:
테이블 목록 조회

describe_table:
테이블 컬럼 정보 조회

run_select_query:
SELECT 쿼리 실행
```

중요한 보안 원칙은 다음이다.

```text
1. SELECT만 허용한다.
2. INSERT, UPDATE, DELETE, DROP, ALTER는 금지한다.
3. 결과 건수를 제한한다.
4. DB 파일 경로는 고정한다.
```

---

## 22. DB MCP Server 코드

파일 경로:

```text
labs/mcp/servers/04_database_mcp_server.py
```

코드:

```python
import sqlite3
from pathlib import Path

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("database-mcp-server")

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "sample.db"


def connect_db() -> sqlite3.Connection:
    if not DB_PATH.exists():
        raise FileNotFoundError(
            "sample.db 파일이 없습니다. 먼저 database/create_sample_db.py를 실행하세요."
        )

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def validate_select_query(sql: str) -> None:
    \"\"\"
    SELECT 쿼리만 허용한다.
    \"\"\"
    normalized = sql.strip().lower()

    if not normalized.startswith("select"):
        raise ValueError("SELECT 쿼리만 실행할 수 있습니다.")

    blocked_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "replace",
        "truncate",
    ]

    for keyword in blocked_keywords:
        if keyword in normalized:
            raise ValueError(f"허용되지 않은 SQL 키워드입니다: {keyword}")


@mcp.tool()
def list_tables() -> list[str]:
    \"\"\"
    SQLite DB의 테이블 목록을 조회한다.
    \"\"\"
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )

    rows = cursor.fetchall()
    conn.close()

    return [row["name"] for row in rows]


@mcp.tool()
def describe_table(table_name: str) -> list[dict[str, str]]:
    \"\"\"
    테이블 컬럼 정보를 조회한다.
    \"\"\"
    if not table_name or not table_name.strip():
        raise ValueError("테이블명이 비어 있습니다.")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info({table_name})")

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "name": row["name"],
            "type": row["type"],
            "not_null": str(bool(row["notnull"])),
            "primary_key": str(bool(row["pk"])),
        }
        for row in rows
    ]


@mcp.tool()
def run_select_query(sql: str, limit: int = 20) -> list[dict]:
    \"\"\"
    SELECT 쿼리를 실행한다.

    운영 환경에서는 SQL Parser, 권한 검사, 테이블 허용 목록, Row-Level Security가 추가로 필요하다.
    \"\"\"
    validate_select_query(sql)

    safe_limit = min(max(limit, 1), 100)

    conn = connect_db()
    cursor = conn.cursor()

    query = f"SELECT * FROM ({sql}) LIMIT {safe_limit}"
    cursor.execute(query)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


if __name__ == "__main__":
    mcp.run()
```

---

## 23. DB MCP Server 확인

먼저 DB를 생성한다.

```bash
cd labs/mcp
python database/create_sample_db.py
```

Inspector로 실행한다.

```bash
mcp dev servers/04_database_mcp_server.py
```

테스트 1:

```text
Tool:
list_tables
```

예상 결과:

```text
employees
projects
```

테스트 2:

```json
{
  "table_name": "employees"
}
```

테스트 3:

```json
{
  "sql": "SELECT * FROM employees",
  "limit": 10
}
```

테스트 4:

```json
{
  "sql": "DELETE FROM employees",
  "limit": 10
}
```

예상 결과:

```text
오류 발생
SELECT 쿼리만 실행할 수 있습니다.
```

---

# Part F. API MCP Server

## 24. API MCP Server 목표

이번 실습에서는 실제 외부 API를 호출하지 않고, `sample_api.json` 파일을 Mock API 응답처럼 사용한다.

이유는 다음과 같다.

```text
1. 네트워크 의존성을 줄인다.
2. API Key가 필요 없다.
3. 실습 결과가 항상 동일하다.
4. MCP 구조 이해에 집중할 수 있다.
```

이번 Tool은 다음과 같다.

```text
get_platform_status:
AI 플랫폼 상태 정보 조회

get_notices:
공지 목록 조회

get_notice_by_level:
level 기준 공지 조회
```

---

## 25. API MCP Server 코드

파일 경로:

```text
labs/mcp/servers/05_api_mcp_server.py
```

코드:

```python
import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("api-mcp-server")

BASE_DIR = Path(__file__).resolve().parents[1]
API_DATA_PATH = BASE_DIR / "sample_data" / "sample_api.json"


def load_api_data() -> dict:
    if not API_DATA_PATH.exists():
        raise FileNotFoundError(f"API 샘플 데이터를 찾을 수 없습니다: {API_DATA_PATH}")

    return json.loads(API_DATA_PATH.read_text(encoding="utf-8"))


@mcp.tool()
def get_platform_status() -> dict:
    \"\"\"
    AI DATA Platform 상태 정보를 조회한다.
    \"\"\"
    data = load_api_data()
    return data["platform_status"]


@mcp.tool()
def get_notices() -> list[dict]:
    \"\"\"
    공지 목록을 조회한다.
    \"\"\"
    data = load_api_data()
    return data["notices"]


@mcp.tool()
def get_notice_by_level(level: str) -> list[dict]:
    \"\"\"
    level 기준으로 공지를 조회한다.
    예: info, warning
    \"\"\"
    if not level or not level.strip():
        raise ValueError("level 값이 비어 있습니다.")

    data = load_api_data()

    return [
        notice
        for notice in data["notices"]
        if notice["level"].lower() == level.lower()
    ]


if __name__ == "__main__":
    mcp.run()
```

---

## 26. API MCP Server 확인

Inspector로 실행한다.

```bash
cd labs/mcp
mcp dev servers/05_api_mcp_server.py
```

테스트 1:

```text
Tool:
get_platform_status
```

예상 결과:

```json
{
  "open_webui": "running",
  "ollama": "running",
  "chroma_db": "ready",
  "last_checked": "2026-06-30T10:00:00+09:00"
}
```

테스트 2:

```text
Tool:
get_notices
```

테스트 3:

```json
{
  "level": "warning"
}
```

예상 결과:

```text
RAG 인덱스 재생성 필요
```

---

# Part G. 통합 MCP Server

## 27. 통합 MCP Server 목표

지금까지는 기능별로 MCP Server를 분리했다.

```text
File MCP Server
RAG MCP Server
DB MCP Server
API MCP Server
```

실습 편의를 위해 하나의 통합 MCP Server를 만들 수도 있다.

통합 서버의 장점은 다음과 같다.

```text
1. 한 번에 여러 Tool을 테스트할 수 있다.
2. Agent Client에서 하나의 MCP Server만 연결하면 된다.
3. 실습 구성이 단순하다.
```

단점은 다음과 같다.

```text
1. 서버 책임이 커진다.
2. 실제 운영에서는 도메인별 분리가 더 적합할 수 있다.
3. 권한 통제가 복잡해질 수 있다.
```

실습에서는 통합 MCP Server를 사용하고, 운영 설계에서는 도메인별 MCP Server 분리를 권장한다.

---

## 28. 통합 MCP Server 코드

파일 경로:

```text
labs/mcp/servers/06_all_tools_mcp_server.py
```

코드:

```python
import json
import sqlite3
from pathlib import Path

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("ai-data-platform-mcp-server")

BASE_DIR = Path(__file__).resolve().parents[1]
SAMPLE_DOCS_DIR = BASE_DIR / "sample_docs"
API_DATA_PATH = BASE_DIR / "sample_data" / "sample_api.json"
DB_PATH = BASE_DIR / "database" / "sample.db"


@mcp.tool()
def list_sample_docs() -> list[str]:
    \"\"\"
    sample_docs 디렉터리의 Markdown 파일 목록을 반환한다.
    \"\"\"
    return sorted(path.name for path in SAMPLE_DOCS_DIR.glob("*.md"))


@mcp.tool()
def read_sample_doc(filename: str) -> str:
    \"\"\"
    sample_docs 디렉터리의 Markdown 파일을 읽는다.
    \"\"\"
    if "/" in filename or "\\\\" in filename or ".." in filename:
        raise ValueError("파일명에는 경로 문자를 사용할 수 없습니다.")

    path = (SAMPLE_DOCS_DIR / filename).resolve()

    if not str(path).startswith(str(SAMPLE_DOCS_DIR.resolve())):
        raise ValueError("sample_docs 밖의 파일은 읽을 수 없습니다.")

    if path.suffix != ".md":
        raise ValueError("Markdown 파일만 읽을 수 있습니다.")

    if not path.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {filename}")

    return path.read_text(encoding="utf-8")


@mcp.tool()
def search_docs(query: str, top_k: int = 3) -> list[dict[str, str]]:
    \"\"\"
    sample_docs Markdown 문서에서 query가 포함된 문서를 검색한다.
    \"\"\"
    if not query or not query.strip():
        raise ValueError("검색어가 비어 있습니다.")

    query_lower = query.lower()
    results: list[dict[str, str]] = []

    for path in sorted(SAMPLE_DOCS_DIR.glob("*.md")):
        content = path.read_text(encoding="utf-8")

        if query_lower in content.lower() or query_lower in path.stem.lower():
            preview = content.replace("\\n", " ").strip()

            if len(preview) > 200:
                preview = preview[:200] + "..."

            results.append(
                {
                    "filename": path.name,
                    "title": path.stem,
                    "preview": preview,
                }
            )

    return results[:top_k]


@mcp.tool()
def get_platform_status() -> dict:
    \"\"\"
    AI DATA Platform 상태 정보를 조회한다.
    \"\"\"
    data = json.loads(API_DATA_PATH.read_text(encoding="utf-8"))
    return data["platform_status"]


@mcp.tool()
def list_tables() -> list[str]:
    \"\"\"
    SQLite DB 테이블 목록을 조회한다.
    \"\"\"
    if not DB_PATH.exists():
        raise FileNotFoundError("sample.db가 없습니다. create_sample_db.py를 먼저 실행하세요.")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )

    rows = cursor.fetchall()
    conn.close()

    return [row["name"] for row in rows]


@mcp.tool()
def run_select_query(sql: str, limit: int = 20) -> list[dict]:
    \"\"\"
    SELECT 쿼리만 실행한다.
    \"\"\"
    normalized = sql.strip().lower()

    if not normalized.startswith("select"):
        raise ValueError("SELECT 쿼리만 실행할 수 있습니다.")

    blocked_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "replace",
        "truncate",
    ]

    for keyword in blocked_keywords:
        if keyword in normalized:
            raise ValueError(f"허용되지 않은 SQL 키워드입니다: {keyword}")

    safe_limit = min(max(limit, 1), 100)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = f"SELECT * FROM ({sql}) LIMIT {safe_limit}"
    cursor.execute(query)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


if __name__ == "__main__":
    mcp.run()
```

---

## 29. 통합 MCP Server 확인

먼저 DB를 생성한다.

```bash
cd labs/mcp
python database/create_sample_db.py
```

Inspector로 실행한다.

```bash
mcp dev servers/06_all_tools_mcp_server.py
```

확인할 Tool은 다음과 같다.

```text
list_sample_docs
read_sample_doc
search_docs
get_platform_status
list_tables
run_select_query
```

---

# Part H. MCP Client

## 30. MCP Client가 하는 일

MCP Server를 만들었으면 이제 Client에서 호출해야 한다.

MCP Client의 역할은 다음과 같다.

```text
1. MCP Server 프로세스를 실행하거나 연결한다.
2. Server와 초기화한다.
3. Tool 목록을 조회한다.
4. Tool을 호출한다.
5. 결과를 받아 Agent에 전달한다.
```

이번 실습에서는 Python Client를 만든다.

단, MCP Python SDK의 Client API는 버전에 따라 세부 코드가 바뀔 수 있다.

따라서 처음에는 MCP Inspector로 Tool을 충분히 확인한 후 Python Client 코드를 작성하는 것을 추천한다.

---

## 31. MCP Client 구성 파일

파일 경로:

```text
labs/mcp/config/mcp_config.json
```

내용:

```json
{
  "mcpServers": {
    "ai-data-platform": {
      "command": "python",
      "args": [
        "servers/06_all_tools_mcp_server.py"
      ]
    }
  }
}
```

이 설정은 MCP Host 또는 Client가 어떤 MCP Server를 어떤 명령으로 실행할지 알려준다.

핵심은 다음이다.

```text
서버 이름
실행 명령
실행 인자
환경변수
```

---

## 32. 첫 번째 MCP Client 예시

파일 경로:

```text
labs/mcp/clients/02_first_mcp_client.py
```

예시 코드:

```python
import asyncio
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


BASE_DIR = Path(__file__).resolve().parents[1]


async def main() -> None:
    server_script = BASE_DIR / "servers" / "06_all_tools_mcp_server.py"

    server_params = StdioServerParameters(
        command="python",
        args=[str(server_script)],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()

            print("=" * 80)
            print("Tool 목록")
            print("=" * 80)

            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            print("=" * 80)
            print("Tool 호출: list_sample_docs")
            print("=" * 80)

            result = await session.call_tool("list_sample_docs", {})
            print(result)

            print("=" * 80)
            print("Tool 호출: search_docs")
            print("=" * 80)

            result = await session.call_tool(
                "search_docs",
                {
                    "query": "Agent",
                    "top_k": 3,
                },
            )
            print(result)


if __name__ == "__main__":
    asyncio.run(main())
```

실행:

```bash
cd labs/mcp
python clients/02_first_mcp_client.py
```

이 예제의 목적은 다음이다.

```text
1. Python Client에서 MCP Server 실행
2. Tool 목록 조회
3. Tool 호출
4. 결과 확인
```

---

## 33. Client 코드 이해

핵심 코드는 다음이다.

```python
server_params = StdioServerParameters(
    command="python",
    args=[str(server_script)],
)
```

이 코드는 MCP Server를 어떤 명령으로 실행할지 정의한다.

다음 코드는 stdio로 MCP Server와 연결한다.

```python
async with stdio_client(server_params) as (read, write):
```

다음 코드는 MCP 세션을 생성한다.

```python
async with ClientSession(read, write) as session:
```

다음 코드는 초기화 과정이다.

```python
await session.initialize()
```

다음 코드는 Tool 목록을 조회한다.

```python
tools = await session.list_tools()
```

다음 코드는 Tool을 호출한다.

```python
result = await session.call_tool(
    "search_docs",
    {
        "query": "Agent",
        "top_k": 3,
    },
)
```

즉, MCP Client는 기존 Tool Executor와 비슷한 역할을 한다.

```text
기존 Tool Executor:
Python 함수 직접 호출

MCP Client:
MCP Server의 Tool 호출
```

---

# Part I. Agent에서 MCP Tool 호출

## 34. Agent with MCP 목표

이제 MCP Tool을 Agent 구조에서 사용해본다.

이번 예제에서는 실제 LLM을 연결하지 않고, 규칙 기반 Agent를 만든다.

입력 예시는 다음과 같다.

```text
문서 목록 보여줘
Agent 검색해줘
플랫폼 상태 확인해줘
직원 테이블 조회해줘
```

Agent는 입력을 보고 MCP Tool을 선택한다.

```text
문서 목록 → list_sample_docs
검색 → search_docs
상태 → get_platform_status
직원 테이블 → run_select_query
```

---

## 35. Agent with MCP 코드

파일 경로:

```text
labs/mcp/clients/03_agent_with_mcp.py
```

코드:

```python
import asyncio
import json
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


BASE_DIR = Path(__file__).resolve().parents[1]


def select_mcp_tool(user_input: str) -> tuple[str, dict[str, Any]]:
    \"\"\"
    사용자 입력을 기반으로 호출할 MCP Tool을 선택한다.
    실제 Agent에서는 이 판단을 LLM이 수행할 수 있다.
    \"\"\"
    text = user_input.strip()

    if "문서 목록" in text:
        return "list_sample_docs", {}

    if "검색" in text or "찾아" in text:
        query = (
            text.replace("검색해줘", "")
            .replace("검색", "")
            .replace("찾아줘", "")
            .replace("찾아", "")
            .strip()
        )

        return "search_docs", {"query": query, "top_k": 3}

    if "상태" in text:
        return "get_platform_status", {}

    if "직원" in text or "employees" in text:
        return "run_select_query", {
            "sql": "SELECT * FROM employees",
            "limit": 10,
        }

    return "", {}


async def run_agent() -> None:
    server_script = BASE_DIR / "servers" / "06_all_tools_mcp_server.py"

    server_params = StdioServerParameters(
        command="python",
        args=[str(server_script)],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            user_input = input("질문을 입력하세요: ").strip()

            tool_name, arguments = select_mcp_tool(user_input)

            if not tool_name:
                print("처리할 수 있는 요청이 아닙니다.")
                print("예: 문서 목록 보여줘 / Agent 검색해줘 / 플랫폼 상태 확인해줘 / 직원 테이블 조회해줘")
                return

            print("=" * 80)
            print("MCP Tool Call")
            print("=" * 80)
            print(json.dumps(
                {
                    "tool_name": tool_name,
                    "arguments": arguments,
                },
                ensure_ascii=False,
                indent=2,
            ))

            result = await session.call_tool(tool_name, arguments)

            print("=" * 80)
            print("MCP Tool Result")
            print("=" * 80)
            print(result)


if __name__ == "__main__":
    asyncio.run(run_agent())
```

실행:

```bash
cd labs/mcp
python clients/03_agent_with_mcp.py
```

입력 예시:

```text
Agent 검색해줘
```

---

## 36. Agent with MCP 구조 이해

이 예제의 전체 흐름은 다음과 같다.

```text
사용자 입력
   ↓
select_mcp_tool
   ↓
MCP Tool Call 생성
   ↓
MCP Client
   ↓
MCP Server
   ↓
Tool 실행
   ↓
MCP Tool Result
   ↓
Agent 출력
```

Step3-3의 기본 Agent와 비교하면 다음과 같다.

```text
Step3-3:
Agent → Tool Executor → Python 함수

Step3-8:
Agent → MCP Client → MCP Server → Python 함수 / 외부 시스템
```

즉, MCP는 Tool Executor 뒤쪽의 외부 시스템 연결 구조를 표준화한다고 볼 수 있다.

---

# Part J. LangGraph와 MCP 연결 방향

## 37. LangGraph Node에서 MCP Tool 호출하기

Step3-6에서 LangGraph Node를 만들었다.

LangGraph Node 안에서 MCP Tool을 호출하면 다음 구조가 된다.

```text
LangGraph Workflow
        │
        ▼
Node
        │
        ▼
MCP Client
        │
        ▼
MCP Server
        │
        ▼
External System
```

예를 들어 문서 검색 Node는 다음 역할을 할 수 있다.

```text
1. State에서 query를 읽는다.
2. MCP Client로 search_docs Tool을 호출한다.
3. 결과를 State의 search_results에 저장한다.
```

의사코드는 다음과 같다.

```python
async def search_node(state: dict) -> dict:
    result = await mcp_client.call_tool(
        "search_docs",
        {
            "query": state["query"],
            "top_k": 3,
        },
    )

    return {
        "search_results": result
    }
```

이 구조를 사용하면 LangGraph는 Workflow를 제어하고, MCP는 외부 Tool 호출을 담당한다.

```text
LangGraph:
흐름 제어

MCP:
외부 시스템 연동
```

---

## 38. LangGraph + MCP 활용 예시

문서 검토 Workflow:

```text
START
  ↓
prepare_query
  ↓
search_docs MCP Tool
  ↓
read_sample_doc MCP Tool
  ↓
summarize
  ↓
final_answer
  ↓
END
```

운영 점검 Workflow:

```text
START
  ↓
get_platform_status MCP Tool
  ↓
상태 판단
  ↓
warning 있음?
   ├─ 예 → 조치 가이드 생성
   └─ 아니오 → 정상 보고
  ↓
END
```

DB 분석 Workflow:

```text
START
  ↓
list_tables MCP Tool
  ↓
describe_table MCP Tool
  ↓
run_select_query MCP Tool
  ↓
분석 요약
  ↓
END
```

---

# Part K. 보안과 운영 고려사항

## 39. MCP Tool 보안 원칙

MCP Tool은 외부 시스템에 접근할 수 있으므로 보안 통제가 매우 중요하다.

이번 실습에서는 읽기 중심 Tool만 만들었다.

운영 환경에서는 다음 원칙을 반드시 적용해야 한다.

```text
1. 읽기 Tool과 쓰기 Tool을 분리한다.
2. 쓰기 Tool은 사용자 승인 후 실행한다.
3. 파일 접근 경로를 제한한다.
4. DB는 SELECT부터 허용한다.
5. API 호출은 허용 목록 기반으로 제한한다.
6. Tool 입력값을 검증한다.
7. 실행 로그를 남긴다.
8. 민감정보를 응답과 로그에서 마스킹한다.
9. MCP Server 실행 권한을 제한한다.
10. Transport 보안을 고려한다.
```

---

## 40. 파일 Tool 보안

파일 Tool은 다음을 반드시 제한해야 한다.

```text
1. 프로젝트 루트 밖 접근 금지
2. ../ 경로 차단
3. 허용 확장자 제한
4. 숨김 파일 접근 제한
5. 민감 파일 접근 제한
6. 파일 삭제 Tool 기본 비활성화
```

이번 실습의 `read_sample_doc`에서는 다음을 적용했다.

```text
1. sample_docs 내부만 허용
2. Markdown 파일만 허용
3. 경로 문자 차단
```

---

## 41. DB Tool 보안

DB Tool은 특히 위험하다.

처음에는 읽기 전용으로 시작해야 한다.

이번 실습에서는 다음을 적용했다.

```text
1. SELECT만 허용
2. INSERT, UPDATE, DELETE, DROP, ALTER 차단
3. 결과 건수 제한
```

운영 환경에서는 추가로 다음이 필요하다.

```text
1. 테이블 허용 목록
2. 컬럼 마스킹
3. Row-Level Security
4. 사용자별 권한
5. Query Timeout
6. SQL Parser 기반 검증
7. 감사 로그
```

---

## 42. API Tool 보안

API Tool은 외부 시스템에 영향을 줄 수 있다.

따라서 API Tool은 다음처럼 나누어야 한다.

```text
읽기 API:
- 상태 조회
- 목록 조회
- 상세 조회

쓰기 API:
- 생성
- 수정
- 삭제
- 발송
- 배포
```

쓰기 API는 반드시 다음 구조를 권장한다.

```text
1. Preview 생성
2. 사용자 확인
3. 승인 후 실행
4. 실행 로그 저장
```

---

## 43. MCP 실행 로그

MCP Tool 호출 시 다음 로그를 남기는 것이 좋다.

```json
{
  "timestamp": "2026-06-30T10:30:00+09:00",
  "session_id": "session-001",
  "mcp_server": "ai-data-platform-mcp-server",
  "tool_name": "search_docs",
  "arguments": {
    "query": "Agent",
    "top_k": 3
  },
  "status": "success",
  "elapsed_ms": 120
}
```

로그는 다음에 사용된다.

```text
1. 장애 분석
2. 보안 감사
3. 사용량 분석
4. Tool 품질 개선
5. Agent 실행 흐름 재현
```

---

# Part L. 실습 검증 체크리스트

## 44. 환경 검증

```text
1. Python 가상환경을 만들었는가?
2. mcp[cli]를 설치했는가?
3. import mcp가 정상 동작하는가?
4. labs/mcp 디렉터리 구조를 만들었는가?
```

---

## 45. Server 검증

```text
1. 01_first_mcp_server.py가 실행되는가?
2. mcp dev로 Tool 목록이 보이는가?
3. hello Tool을 호출할 수 있는가?
4. add Tool을 호출할 수 있는가?
```

---

## 46. File Tool 검증

```text
1. list_sample_docs가 파일 목록을 반환하는가?
2. read_sample_doc으로 mcp.md를 읽을 수 있는가?
3. ../ 경로 입력 시 차단되는가?
4. Markdown 외 파일이 차단되는가?
```

---

## 47. RAG Tool 검증

```text
1. search_docs로 Agent 검색이 되는가?
2. search_docs로 LangGraph 검색이 되는가?
3. top_k 값이 적용되는가?
4. 빈 검색어 입력 시 오류가 나는가?
```

---

## 48. DB Tool 검증

```text
1. create_sample_db.py로 sample.db가 생성되는가?
2. list_tables가 employees, projects를 반환하는가?
3. run_select_query로 SELECT가 실행되는가?
4. DELETE 같은 쿼리가 차단되는가?
```

---

## 49. API Tool 검증

```text
1. get_platform_status가 상태 정보를 반환하는가?
2. get_notices가 공지 목록을 반환하는가?
3. get_notice_by_level로 warning 공지를 조회할 수 있는가?
```

---

## 50. Client 검증

```text
1. 02_first_mcp_client.py가 Server에 연결되는가?
2. Tool 목록을 출력하는가?
3. list_sample_docs 호출 결과가 출력되는가?
4. search_docs 호출 결과가 출력되는가?
```

---

## 51. Agent 검증

```text
1. 문서 목록 보여줘 입력 시 list_sample_docs가 호출되는가?
2. Agent 검색해줘 입력 시 search_docs가 호출되는가?
3. 플랫폼 상태 확인해줘 입력 시 get_platform_status가 호출되는가?
4. 직원 테이블 조회해줘 입력 시 run_select_query가 호출되는가?
```

---

# Part M. 자주 발생하는 오류

## 52. ModuleNotFoundError: No module named 'mcp'

원인:

```text
mcp 패키지가 설치되지 않았거나, 다른 Python 환경에서 실행 중이다.
```

해결:

```bash
python -m pip install "mcp[cli]"
python -c "import mcp; print('ok')"
```

가상환경을 사용하는 경우 활성화 여부를 확인한다.

---

## 53. sample.db 파일을 찾을 수 없음

원인:

```text
SQLite 샘플 DB를 아직 생성하지 않았다.
```

해결:

```bash
cd labs/mcp
python database/create_sample_db.py
```

---

## 54. MCP Server를 직접 실행했는데 아무 반응이 없음

stdio 기반 MCP Server는 브라우저용 웹 서버가 아니다.

MCP Client가 표준 입출력으로 통신해야 한다.

확인은 다음 명령을 사용한다.

```bash
mcp dev servers/01_first_mcp_server.py
```

---

## 55. Client에서 Server 경로 오류

원인:

```text
Client 코드에서 server_script 경로가 잘못되었을 수 있다.
```

해결:

```text
1. clients/02_first_mcp_client.py 위치 확인
2. BASE_DIR 계산 확인
3. servers/06_all_tools_mcp_server.py 파일 존재 확인
```

---

## 56. SQL 검증 오류

예:

```text
SELECT 쿼리만 실행할 수 있습니다.
```

원인:

```text
run_select_query Tool은 SELECT만 허용한다.
```

좋은 입력:

```sql
SELECT * FROM employees
```

나쁜 입력:

```sql
DELETE FROM employees
```

---

# Part N. Enterprise 확장 방향

## 57. Streamable HTTP MCP Server로 확장

이번 실습은 stdio 기반이다.

Enterprise 환경에서는 원격 MCP Server가 필요할 수 있다.

이 경우 Streamable HTTP를 검토한다.

구조는 다음과 같다.

```text
Agent Runtime
   ↓ HTTP
MCP Server
   ↓
Enterprise System
```

장점은 다음과 같다.

```text
1. 여러 Agent가 같은 MCP Server를 사용할 수 있다.
2. API Gateway, 인증, 로깅과 연동하기 쉽다.
3. 서버 배포와 모니터링이 가능하다.
4. 사내 시스템 연동 계층으로 운영하기 좋다.
```

---

## 58. RAG MCP Server 고도화

현재 실습 RAG는 키워드 검색이다.

이후에는 Step2의 ChromaDB RAG와 연결한다.

확장 구조:

```text
search_docs Tool
   ↓
Embedding 생성
   ↓
ChromaDB 검색
   ↓
Document Chunk 반환
   ↓
Agent 답변
```

추가할 기능은 다음과 같다.

```text
1. Collection 목록 조회
2. Chunk 검색
3. 문서 메타데이터 반환
4. 출처 정보 반환
5. 검색 품질 평가
```

---

## 59. DB MCP Server 고도화

현재 DB Tool은 SQLite와 SELECT만 다룬다.

운영 확장 방향은 다음과 같다.

```text
1. PostgreSQL / Oracle 연결
2. 사용자별 권한 적용
3. 테이블 허용 목록
4. SQL 생성과 SQL 실행 분리
5. 실행 전 Preview
6. 민감정보 마스킹
7. Query Timeout
8. 결과 건수 제한
```

---

## 60. API MCP Server 고도화

Mock API를 실제 API로 바꾸려면 다음이 필요하다.

```text
1. API Base URL 설정
2. 인증 Token 관리
3. Timeout 설정
4. Retry 정책
5. 오류 응답 처리
6. Rate Limit 대응
7. 쓰기 API 승인 절차
8. 실행 로그
```

---

## 61. Agent Gateway와 통합

Enterprise 환경에서는 MCP Client를 Agent 코드에 직접 넣기보다 Agent Gateway 또는 Agent Runtime에서 관리하는 것이 좋다.

구조는 다음과 같다.

```text
사용자
  ↓
Agent UI
  ↓
Agent Gateway
  ↓
LangGraph Agent Runtime
  ↓
MCP Client Layer
  ↓
MCP Server Layer
  ↓
External Systems
```

Agent Gateway의 역할은 다음과 같다.

```text
1. 사용자 인증
2. 권한 확인
3. Agent 라우팅
4. Tool 사용 정책 적용
5. 감사 로그
6. 실행 추적
```

---

## 62. Open WebUI와 연결 방향

AI DATA Platform 프로젝트에서 Open WebUI를 사용하고 있다면 MCP 연결은 다음 순서로 검토하는 것이 좋다.

```text
1. Python MCP Server 단독 실습
2. MCP Inspector로 Tool 확인
3. Python MCP Client에서 Tool 호출
4. LangGraph Node에서 MCP Client 호출
5. Open WebUI의 Tool 또는 Function 연동 구조 확인
6. MCP Tool을 Open WebUI에서 사용할 수 있는 방식 검토
```

Open WebUI 버전에 따라 MCP 지원 방식이나 Tool 연결 방식이 달라질 수 있으므로, 먼저 Python 코드에서 MCP 구조를 확실히 이해하는 것이 좋다.

---

# Part O. 핵심 정리

## 63. 이번 문서의 핵심

이번 문서의 핵심은 다음과 같다.

```text
1. MCP Server는 외부 기능을 Tool로 제공한다.
2. MCP Client는 Server에 연결하여 Tool 목록을 조회하고 Tool을 호출한다.
3. FastMCP를 사용하면 Python 함수에 @mcp.tool()을 붙여 Tool로 노출할 수 있다.
4. File 기능은 list_sample_docs, read_sample_doc Tool로 제공할 수 있다.
5. RAG 기능은 search_docs Tool로 제공할 수 있다.
6. DB 기능은 list_tables, describe_table, run_select_query Tool로 제공할 수 있다.
7. API 기능은 get_platform_status 같은 Tool로 제공할 수 있다.
8. 처음 실습은 stdio Transport가 적합하다.
9. 운영 환경에서는 Streamable HTTP와 보안 통제를 검토해야 한다.
10. LangGraph는 Workflow를 제어하고, MCP는 외부 시스템 연동을 담당한다.
```

한 문장으로 정리하면 다음과 같다.

> **MCP 실습의 핵심은 기존 Python 함수를 MCP Tool로 감싸고, Agent가 MCP Client를 통해 외부 시스템 기능을 표준 방식으로 호출하게 만드는 것이다.**

---

## 64. 다음 단계 예고

다음 문서는 다음과 같다.

```text
Step3-9. Multi Agent 협업
docs/study/step3/step3_9_multi_agent_collaboration_guide.md
```

다음 단계에서는 여러 Agent가 역할을 나누어 협업하는 구조를 학습한다.

다음 문서에서 다룰 내용은 다음과 같다.

```text
1. Multi Agent가 필요한 이유
2. Supervisor Agent
3. Worker Agent
4. Planner Agent
5. Research Agent
6. Writer Agent
7. Reviewer Agent
8. Agent 간 메시지 전달
9. LangGraph 기반 Multi Agent
10. MCP Tool을 여러 Agent가 공유하는 구조
```

---

## 65. 참고 자료

아래 자료는 MCP 실습을 진행할 때 참고할 수 있는 공식 자료이다.

```text
Model Context Protocol 공식 문서
https://modelcontextprotocol.io/

Model Context Protocol Specification
https://modelcontextprotocol.io/specification/

MCP Python SDK
https://github.com/modelcontextprotocol/python-sdk

MCP Python SDK PyPI
https://pypi.org/project/mcp/

Build an MCP Server
https://modelcontextprotocol.io/docs/develop/build-server

Build an MCP Client
https://modelcontextprotocol.io/docs/develop/build-client
```

---

## 66. 부록: MCP 실습 파일 작성 순서

처음부터 만든다면 아래 순서로 작성하는 것을 추천한다.

```text
1. requirements.txt
2. sample_docs/*.md
3. sample_data/*.json
4. database/create_sample_db.py
5. servers/01_first_mcp_server.py
6. servers/02_file_mcp_server.py
7. servers/03_rag_mcp_server.py
8. servers/04_database_mcp_server.py
9. servers/05_api_mcp_server.py
10. servers/06_all_tools_mcp_server.py
11. clients/02_first_mcp_client.py
12. clients/03_agent_with_mcp.py
```

---

## 67. 부록: MCP 실습 명령어 모음

패키지 설치:

```bash
python -m pip install "mcp[cli]"
```

첫 번째 서버 확인:

```bash
cd labs/mcp
mcp dev servers/01_first_mcp_server.py
```

File 서버 확인:

```bash
mcp dev servers/02_file_mcp_server.py
```

RAG 서버 확인:

```bash
mcp dev servers/03_rag_mcp_server.py
```

DB 생성:

```bash
python database/create_sample_db.py
```

DB 서버 확인:

```bash
mcp dev servers/04_database_mcp_server.py
```

API 서버 확인:

```bash
mcp dev servers/05_api_mcp_server.py
```

통합 서버 확인:

```bash
mcp dev servers/06_all_tools_mcp_server.py
```

Client 실행:

```bash
python clients/02_first_mcp_client.py
```

Agent 실행:

```bash
python clients/03_agent_with_mcp.py
```

---

## 68. 부록: 실습 완료 후 확인할 것

실습을 완료한 후 다음 질문에 답할 수 있어야 한다.

```text
1. MCP Server는 무엇을 제공하는가?
2. MCP Client는 어떤 역할을 하는가?
3. @mcp.tool()은 어떤 의미인가?
4. File Tool에서 경로 제한이 왜 필요한가?
5. DB Tool에서 SELECT만 허용하는 이유는 무엇인가?
6. RAG 기능을 MCP Tool로 감싸면 어떤 장점이 있는가?
7. LangGraph와 MCP는 각각 어떤 역할을 하는가?
8. stdio와 Streamable HTTP는 어떤 상황에서 사용하는가?
9. Agent가 MCP Tool을 호출하는 흐름은 어떻게 되는가?
10. Enterprise 환경에서 추가해야 할 보안 요소는 무엇인가?
```

---

## 69. 마무리

Step3-8은 Part2의 마지막 실습이다.

이제 AI Agent는 내부 Python 함수만 호출하는 수준을 넘어 외부 시스템과 연결될 수 있다.

지금까지의 흐름을 정리하면 다음과 같다.

```text
Step3-3:
Python 함수 기반 Tool Agent

Step3-4:
Memory와 상태 관리

Step3-5:
Planning Agent와 Workflow

Step3-6:
LangGraph 기반 Workflow Agent

Step3-7:
MCP 아키텍처 이해

Step3-8:
MCP 기반 File / RAG / DB / API 연동 실습
```

이 구조가 갖춰지면 다음 단계인 Multi Agent 협업과 Enterprise Agent Platform 설계로 확장할 수 있다.

MCP는 단순한 실습 기술이 아니라, AI DATA Platform에서 외부 시스템 연동 계층을 표준화하기 위한 핵심 기반이다.
