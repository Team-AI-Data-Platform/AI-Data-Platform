# RAG

RAG는 Retrieval Augmented Generation의 약자이다.

외부 문서를 검색하여 LLM 답변의 근거로 활용하는 구조이다.

AI Agent에서는 RAG 검색 기능이 하나의 Tool로 사용될 수 있다.

Step2에서 구축한 ChromaDB 기반 검색 함수를 MCP Tool로 감싸면 여러 Agent가 같은 RAG 기능을 재사용할 수 있다.
