# Step 2-1-1. Knowledge 개념과 RAG 데이터 흐름 이해 가이드

## 1. 문서 목적

이 문서는 RAG 구축 과정에서 자주 등장하는 **Knowledge** 개념을 이해하고,  
Open WebUI의 Knowledge 기능이 RAG 아키텍처 안에서 어떤 역할을 하는지 정리하기 위한 가이드이다.

현재 Step 2에서는 다음과 같은 흐름으로 RAG를 학습하고 있다.

```text
RAG 개요 이해
    ↓
임베딩 모델 이해
    ↓
Vector DB 구축
    ↓
RAG 질의응답 구현
    ↓
Open WebUI 연동
    ↓
실전 사내 문서 RAG
```

이 과정에서 Open WebUI를 사용하면 사내 문서를 **Knowledge**로 등록하게 된다.  
처음 보면 Knowledge가 표준 용어인지, Open WebUI에서만 사용하는 메뉴명인지 헷갈릴 수 있다.

따라서 이 문서에서는 다음 내용을 중심으로 정리한다.

- Knowledge라는 용어의 의미
- Knowledge와 RAG의 관계
- Open WebUI Knowledge 기능의 역할
- 사내 문서를 Knowledge로 등록했을 때 내부적으로 일어나는 처리 흐름
- AI Data Platform 관점에서 Knowledge를 어떻게 이해해야 하는지

---

## 2. Knowledge란 무엇인가?

AI와 RAG 분야에서 Knowledge는 보통 다음과 같은 의미로 사용된다.

> LLM이 답변할 때 참고할 수 있도록 등록한 외부 지식 또는 문서 집합

즉, Knowledge는 모델이 원래부터 알고 있는 지식이 아니라,  
사용자가 별도로 제공한 문서, 파일, 매뉴얼, 업무 규정, FAQ, 보고서 같은 자료를 의미한다.

예를 들면 다음과 같은 자료가 Knowledge가 될 수 있다.

```text
사내 업무 매뉴얼
시스템 운영 가이드
API 명세서
프로젝트 산출물
PDF 보고서
PPT 제안서
Word 문서
Excel 목록
Markdown 문서
FAQ 문서
```

이러한 자료를 LLM이 직접 학습하는 것은 아니다.  
대신 RAG 구조에서는 문서를 검색 가능한 형태로 변환해 두고, 사용자의 질문과 관련 있는 내용을 찾아 LLM에게 참고 자료로 전달한다.

---

## 3. Knowledge는 표준 용어인가?

Knowledge는 엄밀한 의미의 기술 표준은 아니다.

예를 들어 SQL, HTTP, REST, JSON 같은 것은 명확한 규칙과 형식이 있는 표준 또는 널리 합의된 기술 규격에 가깝다.  
반면 Knowledge는 특정한 파일 형식이나 프로토콜을 의미하지 않는다.

다만 AI 서비스와 RAG 제품에서는 매우 널리 사용되는 개념적 용어이다.

제품이나 프레임워크마다 표현은 조금씩 다르다.

| 구분 | 자주 사용하는 표현 |
|---|---|
| Open WebUI | Knowledge |
| RAG 일반 개념 | Knowledge Base, Document Store |
| LangChain | Documents, Retriever |
| LlamaIndex | Index, Data Source |
| OpenAI API | Files, Vector Store |
| 기업 시스템 | 지식베이스, 문서 저장소, 업무 지식 자산 |

따라서 Knowledge는 다음과 같이 이해하면 된다.

> Knowledge는 표준 규격이라기보다, LLM이 참고할 수 있는 외부 지식 자산을 부르는 대중적인 표현이다.

---

## 4. RAG 관점에서 Knowledge의 위치

RAG는 Retrieval-Augmented Generation의 약자이다.

의미를 풀어보면 다음과 같다.

- Retrieval: 관련 문서를 검색한다.
- Augmented: 검색 결과를 LLM에게 참고 자료로 보강한다.
- Generation: LLM이 참고 자료를 기반으로 답변을 생성한다.

이때 Knowledge는 Retrieval의 대상이 되는 원본 지식 자산이다.

```text
Knowledge
    ↓
문서 수집
    ↓
문서 파싱
    ↓
Chunk 분할
    ↓
Embedding 생성
    ↓
Vector DB 저장
    ↓
질문 입력
    ↓
질문 Embedding 생성
    ↓
유사 문서 검색
    ↓
LLM에게 참고 문서 전달
    ↓
문서 기반 답변 생성
```

즉, Knowledge는 RAG 파이프라인의 출발점이다.

---

## 5. Open WebUI에서 Knowledge의 의미

Open WebUI에서는 Knowledge라는 메뉴를 통해 문서를 등록하고,  
등록한 문서를 특정 모델이나 채팅에서 사용할 수 있다.

사용자 입장에서는 다음과 같은 흐름으로 보인다.

```text
Open WebUI 접속
    ↓
Knowledge 생성
    ↓
문서 업로드
    ↓
모델 또는 채팅에서 Knowledge 선택
    ↓
문서 기반 질문
    ↓
Local LLM 답변
```

하지만 내부적으로는 단순히 파일을 저장하는 것만으로 끝나지 않는다.

문서 기반 질의응답을 위해 다음과 같은 처리가 필요하다.

```text
파일 업로드
    ↓
텍스트 추출
    ↓
문서 Chunk 분할
    ↓
Embedding 생성
    ↓
Vector DB 저장
    ↓
질문 시 관련 Chunk 검색
    ↓
검색 결과를 프롬프트에 포함
    ↓
LLM 답변 생성
```

따라서 Open WebUI의 Knowledge 기능은 다음 역할을 한다.

> 사용자가 업로드한 문서를 RAG에 사용할 수 있도록 관리하는 기능

---

## 6. Knowledge와 LLM 학습의 차이

Knowledge를 등록한다고 해서 Local LLM 자체가 다시 학습되는 것은 아니다.

이 부분은 반드시 구분해야 한다.

### 6.1 LLM 학습

LLM 학습은 모델의 파라미터 자체를 변경하는 작업이다.  
많은 데이터, GPU 자원, 학습 코드, 튜닝 과정이 필요하다.

```text
학습 데이터
    ↓
모델 학습
    ↓
모델 파라미터 변경
    ↓
새 모델 생성
```

### 6.2 Knowledge 등록

Knowledge 등록은 모델 자체를 바꾸는 것이 아니다.  
문서를 검색 가능한 형태로 저장해 두었다가, 질문 시 관련 내용을 찾아 LLM에게 전달하는 방식이다.

```text
문서 등록
    ↓
Vector DB 저장
    ↓
질문 시 관련 문서 검색
    ↓
LLM에게 참고 자료로 전달
    ↓
답변 생성
```

정리하면 다음과 같다.

| 구분 | LLM 학습 | Knowledge 등록 |
|---|---|---|
| 모델 변경 여부 | 모델 자체가 변경됨 | 모델은 변경되지 않음 |
| 난이도 | 높음 | 상대적으로 낮음 |
| 비용 | 큼 | 비교적 작음 |
| 목적 | 모델 능력 자체 개선 | 특정 문서 기반 답변 |
| 대표 방식 | Pre-training, Fine-tuning | RAG |

따라서 Open WebUI에서 Knowledge를 등록하는 것은  
모델을 학습시키는 것이 아니라 **문서를 RAG 검색 대상으로 추가하는 것**에 가깝다.

---

## 7. Knowledge, Document, Chunk, Embedding의 관계

RAG를 이해하려면 Knowledge 아래에 있는 세부 개념을 구분해야 한다.

```text
Knowledge
    └── Document
            └── Chunk
                    └── Embedding
```

### 7.1 Knowledge

문서 묶음 또는 지식 저장소를 의미한다.

예를 들어 `AI Data Platform Knowledge`라는 Knowledge를 만들고,  
그 안에 여러 개의 문서를 등록할 수 있다.

### 7.2 Document

Knowledge 안에 등록된 개별 파일 또는 문서를 의미한다.

예를 들어 다음 파일들이 각각 Document가 된다.

```text
rag_overview.md
system_architecture.pdf
api_specification.docx
project_plan.pptx
```

### 7.3 Chunk

문서를 검색하기 좋게 잘라낸 작은 단위이다.

LLM은 긴 문서를 한 번에 모두 참고하기 어렵다.  
그래서 문서를 적절한 크기로 나누고, 질문과 가장 관련 있는 Chunk만 검색해서 사용한다.

### 7.4 Embedding

텍스트를 숫자 벡터로 변환한 값이다.

Embedding을 사용하면 문장의 의미적 유사도를 계산할 수 있다.

예를 들어 다음 두 문장은 표현은 다르지만 의미는 비슷하다.

```text
RAG는 문서를 검색해서 답변한다.
문서 기반으로 LLM 답변을 생성한다.
```

Embedding을 사용하면 이런 의미적 유사성을 계산할 수 있다.

---

## 8. Open WebUI Knowledge 처리 흐름

Open WebUI에서 Knowledge를 등록했을 때의 흐름을 단순화하면 다음과 같다.

```text
[1] 사용자가 문서 업로드
        ↓
[2] Open WebUI가 문서에서 텍스트 추출
        ↓
[3] 텍스트를 Chunk 단위로 분할
        ↓
[4] 각 Chunk를 Embedding 모델로 벡터화
        ↓
[5] Vector DB에 저장
        ↓
[6] 사용자가 질문 입력
        ↓
[7] 질문도 Embedding으로 변환
        ↓
[8] Vector DB에서 유사 Chunk 검색
        ↓
[9] 검색된 Chunk를 LLM 프롬프트에 포함
        ↓
[10] LLM이 문서 기반 답변 생성
```

여기서 중요한 점은 LLM이 문서를 직접 외우는 것이 아니라는 점이다.  
LLM은 질문 시점에 검색된 문서 내용을 참고해서 답변한다.

---

## 9. Local LLM과 Knowledge의 관계

Open WebUI에서 Local LLM을 연결하면, 사용자는 웹 화면에서 로컬 모델에게 질문할 수 있다.

예를 들어 Ollama에 `qwen`, `llama`, `gemma` 같은 모델이 올라가 있고,  
Open WebUI가 Ollama API와 연결되어 있다면 다음 구조가 된다.

```text
사용자
    ↓
Open WebUI
    ↓
Knowledge 검색
    ↓
관련 문서 Chunk 추출
    ↓
Ollama Local LLM 호출
    ↓
문서 기반 답변 반환
```

이 구조에서 각 구성요소의 역할은 다음과 같다.

| 구성요소 | 역할 |
|---|---|
| 사용자 | 질문 입력 |
| Open WebUI | 화면, Knowledge 관리, RAG 흐름 제어 |
| Knowledge | 문서 기반 지식 저장소 |
| Embedding 모델 | 문서와 질문을 벡터로 변환 |
| Vector DB | 유사 문서 검색 |
| Ollama | Local LLM 실행 |
| Local LLM | 검색된 문서를 참고해 답변 생성 |

---

## 10. 사내 문서 RAG에서 Knowledge가 중요한 이유

사내 문서 RAG에서는 Knowledge 관리가 매우 중요하다.

일반적인 LLM은 회사 내부 문서, 프로젝트 산출물, 업무 규정, 고객사별 시스템 구조를 알지 못한다.  
따라서 사내 문서를 Knowledge로 잘 등록해야 문서 기반 답변이 가능해진다.

예를 들어 다음과 같은 질문은 일반 LLM만으로는 정확하게 답하기 어렵다.

```text
우리 프로젝트의 RAG 실습 디렉터리 구조는 어떻게 되어 있지?
Step2-5에서 AI OCR은 어떤 목적으로 다루고 있지?
사내 문서 전처리 파이프라인은 어떤 단계로 구성되어 있지?
Open WebUI Knowledge는 어떤 문서를 기준으로 구성해야 하지?
```

이 질문에 답하려면 프로젝트 문서가 Knowledge로 등록되어 있어야 한다.

즉, 사내 문서 RAG에서 Knowledge는 단순한 파일 저장소가 아니라  
**AI가 참고할 수 있는 업무 지식 자산**이라고 볼 수 있다.

---

## 11. Knowledge 설계 시 고려할 점

Knowledge를 만들 때는 아무 문서나 한꺼번에 넣는 것보다 목적에 맞게 나누는 것이 좋다.

### 11.1 주제별 분리

예를 들어 AI Data Platform 프로젝트라면 다음과 같이 나눌 수 있다.

```text
Knowledge 1: RAG 학습 문서
Knowledge 2: Local LLM 구축 문서
Knowledge 3: Open WebUI 운영 문서
Knowledge 4: 사내 문서 전처리 문서
Knowledge 5: 제안서 작성 가이드
```

이렇게 나누면 질문의 목적에 맞는 Knowledge를 선택할 수 있다.

### 11.2 문서 품질 관리

Knowledge에 들어가는 문서는 가능한 정리된 상태가 좋다.

다음과 같은 문서는 답변 품질을 떨어뜨릴 수 있다.

```text
중복 문서
오래된 문서
내용이 충돌하는 문서
제목과 본문 구조가 없는 문서
스캔 이미지로만 구성된 PDF
표나 그림만 있고 설명이 없는 문서
```

따라서 Knowledge 등록 전에는 문서 정리와 전처리가 필요하다.

### 11.3 메타데이터 관리

실전 RAG에서는 문서 내용뿐 아니라 메타데이터도 중요하다.

예를 들어 다음과 같은 정보가 있으면 검색과 출처 표시가 쉬워진다.

```text
문서명
작성일
수정일
작성자
업무 영역
문서 유형
보안 등급
버전
페이지 번호
섹션 제목
```

메타데이터가 잘 관리되면 답변 마지막에 출처를 표시하거나,  
특정 업무 영역의 문서만 검색하는 것도 가능해진다.

---

## 12. AI Data Platform 관점의 Knowledge

AI Data Platform 관점에서는 Knowledge를 단순한 Open WebUI 메뉴로 보면 안 된다.

플랫폼 관점에서는 Knowledge를 다음과 같이 이해하는 것이 좋다.

```text
사내 지식 자산
    ↓
문서 저장소
    ↓
문서 수집
    ↓
문서 파싱
    ↓
OCR / Vision LLM
    ↓
Chunking
    ↓
Embedding
    ↓
Vector DB
    ↓
Retriever
    ↓
LLM / Agent
```

즉, Knowledge는 AI 서비스의 기반 데이터이다.

향후 Agent 단계로 넘어가면 Knowledge는 더 중요해진다.  
Agent가 업무를 수행하려면 내부 문서, 정책, 매뉴얼, 시스템 정보, API 정보 등을 참고해야 하기 때문이다.

예를 들어 Agent가 다음과 같은 일을 하려면 Knowledge가 필요하다.

```text
프로젝트 문서 검색
업무 규정 확인
장표 초안 작성
시스템 아키텍처 설명
API 명세 기반 코드 작성
제안서 유사 사례 검색
```

따라서 Knowledge는 RAG뿐 아니라 Agent, Multi-Agent, AI Data Platform 단계에서도 계속 연결되는 핵심 개념이다.

---

## 13. 기존 Step 2 목차와의 연결

현재 Step 2 목차는 다음과 같은 구조이다.

```text
Step 2 RAG 구축
    ├── 개념 이해
    │   ├── RAG 개요 및 아키텍처 이해
    │   ├── Knowledge 개념과 RAG 데이터 흐름 이해
    │   └── 임베딩 모델 이해
    │
    ├── 기본 구축
    │   ├── Vector DB 구축 및 문서 적재
    │   ├── RAG 질의응답 구현
    │   └── Open WebUI 연동
    │
    └── 실전 사내 문서 RAG
        ├── 개요 및 아키텍처
        ├── 문서 전처리 파이프라인
        ├── 실습파일 사용 가이드
        ├── Open WebUI Knowledge 구축
        └── AI OCR / Vision LLM
```

이 문서는 `RAG 개요 및 아키텍처 이해` 다음에 배치하는 것이 좋다.

이유는 다음과 같다.

1. RAG 전체 구조를 먼저 이해한다.
2. 그 다음 RAG에서 사용되는 Knowledge 개념을 이해한다.
3. 이후 Knowledge를 벡터화하기 위한 Embedding 개념을 학습한다.
4. 그 다음 실제 Vector DB 구축과 Open WebUI 연동으로 넘어간다.

추천 파일명은 다음과 같다.

```text
study/step2/step2_1_knowledge_and_rag_data_flow_guide.md
```

추천 메뉴명은 다음과 같다.

```yaml
- Knowledge 개념과 RAG 데이터 흐름 이해: study/step2/step2_1_knowledge_and_rag_data_flow_guide.md
```

---

## 14. 정리

Knowledge는 엄밀한 기술 표준은 아니지만,  
AI와 RAG 분야에서 매우 널리 사용되는 개념이다.

Open WebUI에서 Knowledge는 문서를 등록하고 RAG에 활용하기 위한 기능이다.  
문서를 Knowledge로 등록하면 내부적으로 텍스트 추출, Chunk 분할, Embedding 생성, Vector DB 저장 과정을 거치게 된다.

중요한 점은 Knowledge 등록이 LLM 학습은 아니라는 것이다.  
모델 자체를 바꾸는 것이 아니라, 질문 시점에 관련 문서를 검색해서 LLM에게 참고 자료로 제공하는 방식이다.

AI Data Platform 관점에서는 Knowledge를 다음과 같이 이해하는 것이 좋다.

> Knowledge는 LLM과 Agent가 업무를 수행할 때 참고하는 사내 지식 자산이다.

따라서 Step 2 RAG 구축 단계에서 Knowledge 개념을 명확히 이해해 두면,  
이후 Open WebUI 연동, 실전 사내 문서 RAG, Agent, MCP, AI Data Platform 단계로 확장할 때 전체 구조를 더 쉽게 이해할 수 있다.
