# Step2. RAG 구축 개요 가이드

## 문서 개요

본 문서는 AI Data Platform 스터디의 두 번째 단계인 **RAG(Retrieval Augmented Generation)** 구축에 대한 개요를 설명한다.

Step1에서 Local LLM 환경을 구축하였다면, 이제는 단순한 대화형 AI를 넘어 **회사 문서, 업무 지식, 프로젝트 산출물, 운영 매뉴얼 등을 학습한 AI 비서**를 만드는 단계로 진입하게 된다.

RAG는 현재 기업용 AI 시스템 구축 시 가장 많이 사용되는 핵심 기술이며, ChatGPT와 같은 범용 AI를 기업 내부 지식과 연결하는 대표적인 방법이다.

---

# 1. 왜 RAG가 필요한가?

## 1.1 LLM의 한계

Local LLM을 구축했다고 해서 모든 질문에 정확하게 답변할 수 있는 것은 아니다.

예를 들어 아래와 같은 질문을 한다고 가정하자.

```text
MicroServer Framework의 Runtime 모듈 구조를 설명해줘.
```

LLM은 인터넷에 공개되지 않은 내용을 알 수 없다.

따라서 다음과 같은 문제가 발생한다.

- 모르는 내용을 추측함
- 존재하지 않는 내용을 생성함
- 최신 정보를 반영하지 못함
- 회사 내부 자료를 알 수 없음

이를 Hallucination(환각)이라고 한다.

## 1.2 기업 환경의 문제

실제 기업에서는 다음과 같은 문서들이 존재한다.

- 개발 가이드
- 사용자 매뉴얼
- 운영 절차서
- 설계서
- 제안서
- 회의록
- 정책 문서
- 보안 규정

따라서 기업 환경에서는 다음 구조가 필요하다.

```text
LLM + 기업 내부 지식
```

이를 해결하기 위한 대표 기술이 RAG이다.

---

# 2. RAG란 무엇인가?

RAG는 Retrieval Augmented Generation의 약자이며,

우리말로는 **검색 증강 생성**이라고 한다.

즉,

> 질문과 관련된 문서를 먼저 검색한 후, 검색 결과를 기반으로 답변을 생성하는 기술

이다.

---

# 3. RAG 동작 원리

일반적인 LLM

```text
질문
 ↓
LLM
 ↓
답변
```

RAG

```text
질문
 ↓
문서 검색
 ↓
관련 문서 추출
 ↓
LLM 전달
 ↓
답변 생성
```

---

# 4. RAG 아키텍처

```text
사용자
  │
  ▼
질문 입력
  │
  ▼
Retriever
  │
  ▼
Vector DB
  │
  ▼
관련 문서 검색
  │
  ▼
LLM
  │
  ▼
답변 생성
```

---

# 5. RAG 구성 요소

## 5.1 Document

AI가 참고할 원본 문서

- PDF
- Word
- Excel
- Markdown
- Wiki
- Text

## 5.2 Chunk

문서를 검색 가능한 작은 단위로 분할한 데이터

## 5.3 Embedding

문장을 숫자 벡터로 변환하는 과정

## 5.4 Vector Database

임베딩 데이터를 저장하는 저장소

대표 솔루션

- ChromaDB
- Qdrant
- Weaviate
- Milvus
- PGVector

## 5.5 Retriever

질문과 가장 유사한 문서를 검색하는 모듈

## 5.6 LLM

검색된 문서를 기반으로 최종 답변을 생성하는 모델

- Qwen3
- Gemma3
- Llama3
- DeepSeek

---

# 6. 구축 단계

AI Data Platform 스터디에서는 다음 순서로 진행한다.

## Step2-1. RAG 개념 이해

## Step2-2. ChromaDB 구축

## Step2-3. 문서 수집

## Step2-4. 문서 Chunking

## Step2-5. Embedding 생성

## Step2-6. Vector DB 적재

## Step2-7. Retriever 구축

## Step2-8. LLM 연동

## Step2-9. Open WebUI 연동

## Step2-10. 실전 RAG 구축

---

# 7. 최종 목표

```text
사내 문서
   │
   ▼
Vector DB
   │
   ▼
Retriever
   │
   ▼
Local LLM
   │
   ▼
Open WebUI
```

사용자는 Open WebUI에서 질문만 하면 된다.

예)

```text
MicroServer 설치 절차 알려줘.
```

AI는 내부 문서를 검색한 후 정확한 답변을 제공한다.

---

# 8. AI Data Platform과의 관계

RAG는 AI Data Platform의 핵심 구성요소이다.

향후 학습하게 될

- Agent
- MCP
- Data Lakehouse
- Metadata
- Catalog
- AI Workflow

의 기반 기술이 된다.

```text
Local LLM
   ↓
RAG
   ↓
Agent
   ↓
AI Data Platform
```

---

# 9. 다음 단계

다음 문서에서는

**Step2-2 ChromaDB 구축 및 Vector DB 이해 가이드**

를 진행한다.

해당 단계에서는

- Vector DB 개념
- ChromaDB 설치
- Python 연동
- 데이터 저장
- 데이터 검색

을 실습한다.
