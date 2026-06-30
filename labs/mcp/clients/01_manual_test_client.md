# MCP 수동 테스트 가이드

이 파일은 MCP Inspector를 사용하여 MCP Server를 수동 테스트하는 방법을 정리한다.

## 1. 첫 번째 서버

```bash
cd labs/mcp
mcp dev servers/01_first_mcp_server.py
```

확인 Tool:

```text
hello
add
```

## 2. File 서버

```bash
mcp dev servers/02_file_mcp_server.py
```

확인 Tool:

```text
list_sample_docs
read_sample_doc
```

입력 예:

```json
{
  "filename": "mcp.md"
}
```

## 3. RAG 서버

```bash
mcp dev servers/03_rag_mcp_server.py
```

입력 예:

```json
{
  "query": "Agent",
  "top_k": 3
}
```

## 4. DB 서버

먼저 DB 생성:

```bash
python database/create_sample_db.py
```

서버 실행:

```bash
mcp dev servers/04_database_mcp_server.py
```

입력 예:

```json
{
  "sql": "SELECT * FROM employees",
  "limit": 10
}
```

## 5. API 서버

```bash
mcp dev servers/05_api_mcp_server.py
```

확인 Tool:

```text
get_platform_status
get_notices
get_notice_by_level
```

## 6. 통합 서버

```bash
mcp dev servers/06_all_tools_mcp_server.py
```
