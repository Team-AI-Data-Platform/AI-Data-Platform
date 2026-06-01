# Mac Mini 기반 AI LAB 구축 가이드

# 1. 개요
본 문서는 Mac Mini(M2 Pro 32GB)를 중심으로 생성형 AI 학습 및 실습 환경(AI LAB)을 구축하기 위한 가이드이다.

목표는 단순히 AI를 사용하는 수준이 아니라 다음 역량을 확보하는 것이다.

- Local LLM 구축
- RAG(Retrieval Augmented Generation) 구축
- AI Agent 구축
- AI Data Platform 이해
- LLM Serving Platform 구축

---

# 2. 구축 목표

## 단기 목표
- 로컬 LLM 실행
- 문서 기반 질의응답 구축
- 사내 문서 검색 환경 구축

## 중기 목표
- Agent 기반 문서 생성
- AI API 서비스 구축
- AI 플랫폼 구성요소 이해

## 장기 목표
- 기업용 AI 플랫폼 아키텍처 설계
- AI 기반 업무지원 시스템 구축
- 사내 AI Assistant 구축

---

# 3. 왜 Mac Mini를 AI 서버로 사용하는가?

## 기존 방식
각 사용자가 개별적으로 AI 환경을 구축

### 문제점
- PC 사양 차이
- 설치 환경 차이
- 모델 다운로드 중복
- 실습 환경 불일치
- 장애 대응 어려움
## 개선 방식
Mac Mini를 중앙 AI 서버로 구성

```text

                   +---------------------+
                   |     Mac Mini        |
                   |   M2 Pro / 32GB     |
                   +---------------------+
                   | Ollama              |
                   | Open WebUI          |
                   | Qdrant              |
                   | MinIO               |
                   | LangGraph           |
                   +----------+----------+
                              |
                       WiFi / LAN
                              |
        +---------------------+---------------------+
        |                     |                     |
    사용자1                사용자2               사용자3
   (Browser)            (Browser)           (Browser)
```

## 장점
- 실습 환경 표준화
- 중앙 집중형 운영
- 비용 절감
- 스터디 효율 향상

---

# 4. Mac Mini 사양 검토

## 현재 장비
| 항목 | 사양 |
|--------|--------|--------|
| CPU |	Apple M2 Pro |
| Memory | 32GB Unified Memory |

## 활용 가능 범위
| 영역 | 가능 | 여부 |
|--------|--------|--------|
| Ollama | 가능 |
| Qwen3 8B | 매우 원활 |
| Gemma 12B | 원활 |
| RAG |	가능 |
| Agent | 가능 |
| MinIO | 가능 |
| Qdrant | 가능 |
| Spring Boot API |	가능 |

## 참고
32B급 모델도 구동은 가능할 수 있으나 성능 및 응답속도 측면에서는 8B~14B 모델 중심의 학습을 권장한다.

---

# 5. AI LAB 아키텍처

## 전체 구조

```text
사용자
   |
Open WebUI
   |
Agent Layer
   |
+----------------------+
|      Ollama          |
|   Qwen / Gemma       |
+----------------------+
   |
응답 생성
```

## RAG 구조

```text
PDF / PPT / DOCX / Markdown
              |
          Chunking
              |
         Embedding
              |
         Vector DB
              |
      Context Retrieval
              |
            LLM
              |
           답변
```

## Agent 구조

```text
사용자 요청
      |
    Agent
      |
 +----+----+
 |         |
문서검색   API호출
 |         |
 +----+----+
      |
   LLM 답변
```

---

# 6. 주요 솔루션

## Ollama
역할: 로컬 LLM 실행 엔진

주요 모델

- Qwen3
- Gemma
- Llama

## Open WebUI
역할: 웹 기반 사용자 인터페이스

특징

- ChatGPT 유사 UI
- 다중 사용자 지원
- 문서 업로드 지원

## Qdrant
역할: Vector Database

기능

- 임베딩 저장
- 유사도 검색
- RAG 구현

## MinIO
역할: Object Storage

저장 대상

- PDF
- PPT
- DOCX
- 로그
- 학습 데이터

## LangGraph
역할: Agent Workflow Framework

기능

- Tool Calling
- Memory
- Workflow 구성

---

# 7. 스터디 실습 시나리오

## STEP 1. Local LLM

```bash
ollama run qwen3:8b
```

학습 내용

- LLM 개념
- Token
- Context Window
- Prompt Engineering

## STEP 2. RAG

### 예시 질문

```text
한국장학재단 API 구축 관련 내용을 알려줘
```

### 처리 과정

```text
질문
 ↓
문서 검색
 ↓
관련 내용 추출
 ↓
LLM 답변 생성
```


## STEP 3. Agent
예시

```text
장학재단 API 허브 구축 장표 초안 작성
```
처리 과정

```text
문서 검색
 ↓
RFP 검색
 ↓
유사 제안서 검색
 ↓
초안 생성
```


## STEP 4. AI Data Platform
학습 대상

- MinIO
- Iceberg
- Spark
- Data Catalog

### 목표

AI가 사용할 데이터를 어떻게 저장하고 관리하는지 이해

## STEP 5. AI Serving Platform

학습 대상

- FastAPI
- Spring Boot
- Gateway
- Docker
- Kubernetes

예시 API

```bash
POST /ask
POST /search
POST /agent
```

---


# 8. 최종 프로젝트

## 나만의 AI 비서 구축
기능

- 제안서 검색
- PPT 검색
- RFP 검색
- 회의록 검색
- 문서 요약
- 장표 초안 생성

## 목표 아키텍처
```text
사용자
  |
Open WebUI
  |
Agent
  |
+-----------------+
| Qdrant          |
| MinIO           |
+-----------------+
  |
Ollama
  |
Qwen3
```

---

# 9. 향후 확장 방향

## 장비
현재

- M2 Pro
-  32GB Memory
충분히 학습 가능

향후

- M5 Pro
- 48GB 이상
권장

## 확장 영역
- Multi Agent
- 사내 지식검색
- 문서 자동화
- 개발 생산성 향상

---

# 10. 기대 효과
본 AI LAB을 통해 다음 역량을 확보할 수 있다.

- Local LLM 이해
-  RAG 구축 경험
- Agent 개발 경험
- AI 데이터 플랫폼 이해
-  AI 서비스 아키텍처 설계 역량
궁극적으로 기업 환경에서 AI 플랫폼을 설계하고 구축할 수 있는 AI 플랫폼 아키텍트 역량 확보를 목표로 한다.