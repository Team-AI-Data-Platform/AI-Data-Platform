# Step3-8 MCP Lab

이 실습 프로젝트는 `Step3-8. MCP 기반 외부 시스템 연동 실습 가이드` 문서에 맞춰 만든 실행 가능한 샘플 코드입니다.

## 1. 구성

```text
labs/mcp
├── README.md
├── requirements.txt
├── servers
├── clients
├── sample_docs
├── sample_data
├── database
└── config
```

## 2. 설치

프로젝트 루트에서 실행합니다.

```bash
python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r labs/mcp/requirements.txt
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r labs/mcp/requirements.txt
```

## 3. DB 생성

`sample.db`는 ZIP에 포함되어 있지만, 다시 만들려면 아래 명령을 실행합니다.

```bash
cd labs/mcp
python database/create_sample_db.py
```

## 4. MCP Inspector 실행

```bash
cd labs/mcp
mcp dev servers/01_first_mcp_server.py
mcp dev servers/02_file_mcp_server.py
mcp dev servers/03_rag_mcp_server.py
mcp dev servers/04_database_mcp_server.py
mcp dev servers/05_api_mcp_server.py
mcp dev servers/06_all_tools_mcp_server.py
```

## 5. Client 실행

```bash
cd labs/mcp
python clients/02_first_mcp_client.py
python clients/03_agent_with_mcp.py
```

## 6. Agent 테스트 문장

```text
문서 목록 보여줘
Agent 검색해줘
플랫폼 상태 확인해줘
직원 테이블 조회해줘
```

## 7. 주의

- `stdio` 기반 MCP Server는 브라우저로 접속하는 웹 서버가 아닙니다.
- MCP Inspector 또는 MCP Client를 통해 호출해야 합니다.
- DB Tool은 안전을 위해 `SELECT`만 허용합니다.
- File Tool은 `sample_docs` 디렉터리 내부의 `.md` 파일만 읽습니다.
