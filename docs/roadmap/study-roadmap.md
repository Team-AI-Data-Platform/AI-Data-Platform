# AI Data Platform & Local LLM Study Roadmap

# 1. 스터디 개요

## 목적

본 스터디는 ChatGPT와 같은 생성형 AI를 단순히 사용하는 수준을 넘어,

- Local LLM 구축
- RAG(Retrieval Augmented Generation) 구축
- AI Agent 구축
- AI 데이터 플랫폼 설계
- LLM Serving 플랫폼 구축

역량을 확보하여 AI 플랫폼 아키텍트 수준의 기술 이해를 목표로 한다.

---

## 최종 목표

다음과 같은 AI 서비스를 직접 구축할 수 있는 수준에 도달한다.

### AI 비서

- 제안서 검색
- PPT 검색
- RFP 검색
- 회의록 검색
- 기술문서 검색

### AI Agent

- 장표 초안 생성
- 문서 요약
- API 문서 생성
- 제안서 작성 지원

### AI 플랫폼

- 데이터 수집
- 데이터 저장
- 데이터 분석
- AI 서비스 제공

전체 아키텍처를 설계할 수 있는 수준 확보

---

# STEP 1. Local LLM 시작

## 목표

클라우드 기반 AI가 아닌 개인 PC에서 LLM을 직접 실행하여 LLM 동작 원리를 이해한다.

---

## 왜 배우는가?

ChatGPT를 사용하면 AI가 어떻게 동작하는지 보이지 않는다.

로컬 환경에서 직접 모델을 실행하면

- 모델 크기
- 메모리 사용량
- 응답 속도
- 추론 과정

등을 체험할 수 있다.

---

## 실습

### Ollama 설치

```bash
brew install ollama
```

### 모델 실행

```bash
ollama run qwen3:8b
```

```bash
ollama run gemma3:12b
```

---

## 학습 내용

### LLM 개념

- Transformer
- Token
- Attention
- Context Window

### 모델 크기

- 3B
- 7B
- 14B
- 32B
- 70B

### 모델 최적화

- Quantization
- Q4
- Q8
- GGUF

### Prompt Engineering

- Zero Shot
- Few Shot
- Chain of Thought

---

## 결과물

- 로컬 AI 챗봇 구축
- 다양한 모델 성능 비교

---

# STEP 2. RAG 구축

## 목표

AI가 문서를 검색하여 답변하도록 만든다.

---

## 왜 배우는가?

LLM은 학습되지 않은 사내 문서를 알 수 없다.

따라서

- 제안서
- PPT
- PDF
- 운영문서

를 AI가 검색할 수 있도록 해야 한다.

이를 RAG라고 한다.

---

## 개념

```text
문서

↓

Chunking

↓

Embedding

↓

Vector DB

↓

검색

↓

LLM 답변 생성
```

---

## 실습

### 데이터

- PDF
- PPTX
- DOCX
- Markdown

### Embedding

- BGE
- Nomic

### Vector DB

- ChromaDB
- Qdrant

---

## 학습 내용

### Chunking

문서를 적절한 크기로 분할

### Embedding

문장을 벡터로 변환

### Similarity Search

질문과 가장 유사한 문서 검색

### Vector Database

벡터 저장 및 검색

---

## 결과물

### 제안서 검색 시스템

예시

```text
질문

"한국장학재단 API 구축 관련 내용을 알려줘"

↓

과거 제안서 검색

↓

근거 제시

↓

답변 생성
```

---

# STEP 3. AI Agent 구축

## 목표

AI가 스스로 작업을 수행하도록 만든다.

---

## 왜 배우는가?

일반 LLM은 질문에 대한 답변만 한다.

Agent는

- 검색
- 판단
- 실행

을 수행한다.

---

## 예시

```text
사용자

↓

장학재단 API 관련 장표 작성

↓

관련 문서 검색

↓

RFP 검색

↓

유사 제안서 검색

↓

장표 초안 생성
```

---

## 학습 내용

### Agent

- Tool Calling
- Planning
- Reasoning
- Memory

### Framework

- LangChain
- LangGraph

### MCP

Model Context Protocol

### Tool Integration

- Database
- File System
- API
- Search Engine

---

## 결과물

### 제안서 작성 Agent

### 문서 요약 Agent

### 회의록 분석 Agent

---

# STEP 4. AI Data Platform

## 목표

AI가 사용할 데이터를 저장하고 관리하는 플랫폼을 이해한다.

---

## 왜 배우는가?

AI의 성능은 모델보다 데이터 품질에 더 큰 영향을 받는다.

기업 환경에서는

- 정형 데이터
- 비정형 데이터
- 로그 데이터

를 통합 관리해야 한다.

---

## 아키텍처

```text
DB

File

Log

↓

Object Storage

↓

Iceberg

↓

Spark

↓

AI
```

---

## 학습 내용

### Storage

- MinIO
- Amazon S3

### Data Lake

- Object Storage

### Lakehouse

- Apache Iceberg
- Delta Lake

### Data Processing

- Spark
- Kafka

### Metadata

- Data Catalog
- Data Governance

---

## 결과물

### AI 데이터 플랫폼 설계서

### 데이터 수집 아키텍처

### 데이터 거버넌스 체계

---

# STEP 5. LLM Serving Platform

## 목표

LLM을 서비스 형태로 제공한다.

---

## 왜 배우는가?

기업 환경에서는 수백~수천 명이 AI를 동시에 사용한다.

따라서

- 모델 실행
- API 제공
- 확장성
- 모니터링

구조가 필요하다.

---

## 아키텍처

```text
LLM

↓

Serving Engine

↓

REST API

↓

Gateway

↓

Agent

↓

User
```

---

## 학습 내용

### Inference Engine

- Ollama
- MLX
- vLLM

### API

- FastAPI
- Spring Boot

### Gateway

- Spring Cloud Gateway
- NGINX

### Container

- Docker
- Kubernetes

### Monitoring

- Prometheus
- Grafana

---

## 결과물

### 사내 AI 플랫폼 PoC

### AI Gateway 구축

### AI API 서비스 구축

---

# 추천 실습 환경

## 현재 장비

### M2 Pro Mac Mini

- Memory : 32GB

가능 범위

- Ollama
- MLX
- Qwen 8B
- Qwen 14B
- Gemma
- RAG
- Agent

스터디 진행에 충분

---

## 향후 업그레이드

### M5 Pro

권장 사양

- Memory 48GB 이상

활용 범위

- 32B 모델
- 장문 Context
- Multi Agent
- 대규모 실습

---

# 스터디 운영 계획

| 단계 | 기간 | 목표 |
|--------|--------|--------|
| STEP1 | 1주 | Local LLM |
| STEP2 | 2주 | RAG |
| STEP3 | 2주 | Agent |
| STEP4 | 2주 | AI Data Platform |
| STEP5 | 2주 | LLM Serving |

총 9주 과정

---

# 최종 프로젝트

## 나만의 AI 비서 구축

### 기능

- 제안서 검색
- PPT 검색
- RFP 검색
- 회의록 검색
- 문서 요약
- 장표 초안 생성

### 기술 스택

- Ollama
- OpenWebUI
- Qdrant
- LangGraph
- MinIO
- Iceberg
- Spring Boot
- Kubernetes

### 기대 효과

- 제안서 작성 생산성 향상
- 사내 지식 검색 체계 구축
- AI 플랫폼 아키텍처 역량 확보
