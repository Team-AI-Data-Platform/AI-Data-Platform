# RAG 개요

RAG는 Retrieval Augmented Generation의 약자이다.

LLM이 자체 지식만으로 답변하지 않고, 외부 문서를 검색한 뒤 검색 결과를 근거로 답변을 생성하는 방식이다.

RAG의 기본 흐름은 다음과 같다.

1. 사용자 질문 입력
2. 질문을 Embedding으로 변환
3. Vector DB에서 유사 문서 검색
4. 검색된 문서를 Prompt에 포함
5. LLM이 근거 기반 답변 생성

AI Agent 구조에서는 RAG 검색 기능이 하나의 Tool로 사용될 수 있다.
