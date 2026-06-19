# Step2-5 보완. 실전 사내 문서 RAG 구축과 Open WebUI 적용 범위 정리

> Step2-5 실습을 `Python 기반 RAG 내부 파이프라인`과 `Open WebUI 기반 Knowledge 활용`로 구분하여 이해하기 위한 보완 문서

---

## 1. 문서 작성 목적

이 문서는 AI-Data-Platform 프로젝트의 **Step2-5. 실전 사내 문서 RAG 구축** 가이드에 추가하기 위한 보완 문서이다.

기존 Step2-5 가이드에서는 PDF, PPTX, DOCX, XLSX 같은 실제 사내 문서를 Python으로 파싱하고, Chunk를 만들고, Embedding 후 ChromaDB에 저장한 뒤 RAG 검색과 답변을 수행하는 구조를 설명했다.

그런데 Step2-4에서 이미 Open WebUI를 구축했기 때문에, Step2-5에서도 Open WebUI를 사용하는 것이 맞는지에 대한 의문이 생길 수 있다.

결론부터 말하면, **Step2-5에서는 Open WebUI를 사용할 수도 있고, 사용하지 않을 수도 있다.**

다만 두 방식의 목적이 다르다.

```text
1. Python 기반 실습
   - RAG 내부 동작 구조를 이해하기 위한 실습
   - 문서 파싱, Chunking, Embedding, Vector DB 저장 과정을 직접 구현

2. Open WebUI 기반 실습
   - 실제 사용자가 웹 화면에서 문서를 업로드하고 질의응답하는 구조 확인
   - Knowledge 기능을 이용하여 사내 문서 기반 RAG 사용 경험을 검증
```

따라서 Step2-5는 하나의 실습으로만 보기보다, 다음 두 단계로 나누어 이해하는 것이 더 적절하다.

```text
Step2-5A. Python 기반 사내 문서 RAG 파이프라인 구축
Step2-5B. Open WebUI 기반 사내 문서 Knowledge 활용
```

---

## 2. 왜 혼동이 생기는가?

Step2 전체 흐름은 다음과 같다.

```text
Step2-1. RAG 개요 및 아키텍처 이해
        ↓
Step2-2. Vector DB 구축 및 문서 적재
        ↓
Step2-3. Python RAG 질의응답 구현
        ↓
Step2-4. Open WebUI 연동
        ↓
Step2-5. 실전 사내 문서 RAG 구축
```

이 흐름만 보면 Step2-4에서 Open WebUI를 이미 사용했으므로, Step2-5에서도 당연히 Open WebUI를 중심으로 실습해야 할 것처럼 보인다.

하지만 실제 기업형 RAG를 만들 때는 Open WebUI만으로 모든 문서 처리를 해결하기 어렵다.

특히 사내 문서는 단순한 텍스트 파일이 아니라 다음과 같은 복잡한 문서가 많다.

```text
PDF 제안서
PPTX 발표자료
DOCX 설계서
XLSX 요구사항 목록
HWP 공공기관 문서
스캔 PDF
이미지 기반 문서
아키텍처 다이어그램
업무 흐름도
표 중심 문서
```

이러한 문서는 단순 업로드만으로 좋은 RAG 품질을 보장하기 어렵다. 문서 유형별로 텍스트를 어떻게 추출할지, 표를 어떻게 문장화할지, 슬라이드 번호와 페이지 번호를 어떻게 Metadata로 남길지, OCR이 필요한 문서는 어떻게 처리할지 등을 별도로 설계해야 한다.

그래서 Step2-5에서는 Open WebUI 사용 여부보다 먼저 **기업 문서가 RAG에 들어가기 전 어떤 전처리 과정을 거쳐야 하는지**를 이해하는 것이 중요하다.

---

## 3. Step2-5의 올바른 구성 방향

Step2-5는 다음과 같이 두 영역으로 나누는 것이 좋다.

```text
Step2-5A. Enterprise Document Ingestion Pipeline

사내 문서
  ↓
Python Parser
  ↓
Text Extraction
  ↓
Metadata 생성
  ↓
Chunking
  ↓
Embedding
  ↓
ChromaDB 저장
  ↓
Python RAG 검색
```

```text
Step2-5B. Open WebUI Enterprise Knowledge

사내 문서
  ↓
Open WebUI Knowledge 등록
  ↓
문서 업로드
  ↓
Embedding / Vector 저장
  ↓
Chat 화면에서 질의응답
  ↓
출처 확인
```

두 방식은 서로 대체 관계가 아니라 보완 관계이다.

Python 기반 실습은 내부 구조를 이해하기 위한 것이고, Open WebUI 기반 실습은 사용자가 실제로 문서 기반 질의응답을 체험하기 위한 것이다.

---

## 4. Step2-5A. Python 기반 사내 문서 RAG 파이프라인

Step2-5A는 RAG의 내부 처리 과정을 직접 구현하는 실습이다.

기존 가이드에서 제시한 다음 파일들이 이 영역에 해당한다.

| 파일명 | 역할 |
|---|---|
| `09_extract_pdf.py` | PDF 문서에서 페이지별 텍스트를 추출한다. |
| `10_extract_pptx.py` | PPTX 문서에서 슬라이드별 텍스트를 추출한다. |
| `11_extract_docx.py` | DOCX 문서에서 제목과 문단 텍스트를 추출한다. |
| `12_extract_xlsx.py` | XLSX 문서에서 Sheet와 Row 데이터를 추출한다. |
| `13_build_enterprise_chunks.py` | 추출된 텍스트를 Chunk 단위로 정리한다. |
| `14_insert_enterprise_docs_to_chroma.py` | Chunk를 Embedding하여 ChromaDB에 저장한다. |
| `15_enterprise_rag_search.py` | 사내 문서 기반 RAG 검색과 답변 생성을 수행한다. |

이 실습의 핵심은 Open WebUI 화면을 사용하는 것이 아니라, RAG가 내부적으로 어떤 절차로 동작하는지를 직접 확인하는 것이다.

실행 흐름은 다음과 같다.

```text
1. enterprise_docs 디렉터리에 실습 문서를 넣는다.
2. 문서 유형별 추출 스크립트를 실행한다.
3. extracted_text 디렉터리에 추출 결과가 생성되는지 확인한다.
4. 추출 텍스트를 Chunk로 변환한다.
5. Chunk를 Embedding하여 ChromaDB에 저장한다.
6. 질문을 입력하여 관련 Chunk가 검색되는지 확인한다.
7. 검색된 Context를 LLM에 전달하여 답변을 생성한다.
```

이 단계에서 학습해야 할 핵심 개념은 다음과 같다.

```text
문서 Parser
텍스트 추출
Metadata
Chunking
Embedding
Vector DB
Similarity Search
RAG Prompt
LLM Answer Generation
```

즉, Step2-5A는 **RAG 엔진의 내부 동작 원리를 이해하기 위한 개발자 관점 실습**이다.

---

## 5. Step2-5B. Open WebUI 기반 사내 문서 Knowledge 활용

Step2-5B는 Open WebUI의 Knowledge 기능을 이용하여 실제 사용자 관점에서 사내 문서 기반 RAG를 테스트하는 실습이다.

Open WebUI에서는 사용자가 웹 화면에서 문서를 업로드하고, 해당 문서를 Knowledge로 등록한 뒤, Chat 화면에서 문서 기반 질의응답을 수행할 수 있다.

흐름은 다음과 같다.

```text
1. Open WebUI 접속
2. Knowledge 메뉴 이동
3. 신규 Knowledge 생성
4. PDF, DOCX, TXT, MD 등 문서 업로드
5. Embedding 처리 확인
6. Chat 화면에서 Knowledge 선택
7. 문서 기반 질문 입력
8. 답변과 출처 확인
```

Open WebUI 기반 실습의 장점은 다음과 같다.

```text
사용자 화면에서 바로 테스트할 수 있다.
문서 업로드 절차가 단순하다.
별도 Python 코드를 작성하지 않아도 된다.
모델 선택과 대화 테스트가 쉽다.
팀원 교육용으로 직관적이다.
```

반면 한계도 있다.

```text
복잡한 PPTX 구조를 완벽히 해석하기 어렵다.
XLSX 표 데이터를 업무 의미에 맞게 문장화하기 어렵다.
HWP 문서는 별도 변환이 필요할 수 있다.
스캔 PDF는 OCR 품질에 따라 결과가 달라진다.
페이지, 슬라이드, 시트, 행 단위 Metadata를 세밀하게 통제하기 어렵다.
기업 보안 정책과 권한 제어는 별도 설계가 필요하다.
```

따라서 Open WebUI는 실무형 RAG의 최종 사용자 화면으로는 매우 유용하지만, 복잡한 기업 문서 전처리까지 모두 해결하는 도구로 보면 안 된다.

---

## 6. Python RAG와 Open WebUI RAG의 차이

두 방식의 차이를 정리하면 다음과 같다.

| 구분 | Python 기반 RAG | Open WebUI 기반 RAG |
|---|---|---|
| 주 목적 | 내부 구조 학습 및 커스텀 파이프라인 구현 | 웹 화면 기반 문서 질의응답 사용 |
| 사용자 | 개발자, 아키텍트, RAG 엔지니어 | 일반 사용자, 현업 담당자, 교육 대상자 |
| 문서 처리 | 직접 Parser 구현 | Open WebUI 기본 처리 기능 활용 |
| Metadata 제어 | 세밀한 제어 가능 | 제한적 |
| Chunking 제어 | 직접 설계 가능 | 기본 설정 중심 |
| Embedding 저장소 | 직접 ChromaDB 등 구성 | Open WebUI 내부 설정 사용 |
| PPT/XLSX 복잡 문서 | 커스텀 처리 가능 | 제한적일 수 있음 |
| 운영 확장성 | API, 배치, 권한 제어 확장 가능 | 빠른 PoC와 교육에 유리 |
| 학습 효과 | RAG 원리 이해에 좋음 | 사용 경험 이해에 좋음 |

정리하면 다음과 같다.

```text
Python 기반 RAG는 만드는 방법을 배우는 실습이다.
Open WebUI 기반 RAG는 사용하는 방법을 배우는 실습이다.
```

---

## 7. 실무에서는 어떤 방식이 더 적합한가?

실무에서는 두 방식을 함께 사용하는 것이 가장 현실적이다.

초기 PoC나 교육 단계에서는 Open WebUI를 사용하면 빠르게 결과를 확인할 수 있다.

```text
문서 업로드
질문 입력
답변 확인
출처 확인
```

이 과정이 단순하기 때문에 팀원들이 RAG의 사용 경험을 빠르게 이해할 수 있다.

하지만 실제 프로젝트 문서, 제안서, 업무 매뉴얼, 요구사항 정의서, 아키텍처 문서 등을 대상으로 품질 높은 RAG를 만들려면 Python 기반 전처리 파이프라인이 필요하다.

예를 들어 다음과 같은 요구가 있다면 Open WebUI 기본 기능만으로는 부족할 수 있다.

```text
PPTX의 슬라이드 번호를 반드시 출처로 표시해야 한다.
Excel의 각 Row를 업무 요구사항 단위로 검색해야 한다.
PDF의 페이지 번호를 정확하게 Metadata로 남겨야 한다.
스캔 PDF를 OCR 처리한 뒤 검색해야 한다.
아키텍처 다이어그램을 Vision LLM으로 설명 텍스트화해야 한다.
문서 보안 등급별로 사용자 검색 권한을 제어해야 한다.
```

이 경우에는 다음 구조가 더 적합하다.

```text
사내 문서 원본
  ↓
Python 전처리 파이프라인
  ↓
정제된 텍스트 / Metadata / Chunk
  ↓
Vector DB 저장
  ↓
RAG API 또는 Open WebUI 연동
```

즉, Open WebUI를 최종 사용자 인터페이스로 사용하더라도, 그 앞단의 문서 전처리는 별도로 구성하는 것이 실무적으로 더 안정적이다.

---

## 8. AI-Data-Platform 학습 로드맵 관점의 권장 구조

AI-Data-Platform 프로젝트에서는 Step2-5를 다음과 같이 확장하는 것을 권장한다.

```text
Step2-5. 실전 사내 문서 RAG 구축

├─ Step2-5A. Python 기반 Enterprise Document Ingestion
│  ├─ PDF Parser
│  ├─ PPTX Parser
│  ├─ DOCX Parser
│  ├─ XLSX Parser
│  ├─ Chunk Builder
│  ├─ ChromaDB Insert
│  └─ RAG Search
│
└─ Step2-5B. Open WebUI 기반 Enterprise Knowledge
   ├─ Knowledge 생성
   ├─ 문서 업로드
   ├─ Embedding 처리 확인
   ├─ Chat 질의응답
   ├─ 출처 확인
   └─ 한계 및 보완점 정리
```

이렇게 나누면 학습 흐름이 명확해진다.

```text
Step2-5A에서는 RAG 내부 구조를 이해한다.
Step2-5B에서는 사용자가 RAG를 어떻게 사용하는지 이해한다.
```

개발자와 아키텍트에게는 Step2-5A가 중요하고, 현업 사용자와 교육 대상자에게는 Step2-5B가 더 직관적이다.

---

## 9. Step2-5A 실습 완료 기준

Step2-5A는 다음 조건을 만족하면 완료로 판단한다.

```text
1. PDF, PPTX, DOCX, XLSX 중 최소 1개 이상의 문서를 준비했다.
2. 문서 유형별 추출 스크립트를 실행했다.
3. extracted_text 디렉터리에 추출 결과가 생성되었다.
4. 추출 텍스트가 Chunk 단위로 변환되었다.
5. Chunk Metadata에 파일명, 문서 유형, 페이지 또는 슬라이드 정보가 포함되었다.
6. Chunk가 Embedding되어 ChromaDB에 저장되었다.
7. 사용자 질문으로 관련 문서 Chunk가 검색되었다.
8. 검색 결과를 기반으로 LLM 답변이 생성되었다.
9. 답변의 근거 문서 출처를 확인할 수 있었다.
```

Step2-5A의 핵심 완료 기준은 다음이다.

```text
문서가 RAG 내부 파이프라인을 거쳐 검색 가능한 지식 Chunk로 변환되었는가?
```

---

## 10. Step2-5B 실습 완료 기준

Step2-5B는 다음 조건을 만족하면 완료로 판단한다.

```text
1. Open WebUI에 접속할 수 있다.
2. Knowledge 메뉴에서 신규 Knowledge를 생성했다.
3. 실습 문서를 업로드했다.
4. 문서 Embedding 처리가 완료되었다.
5. Chat 화면에서 해당 Knowledge를 선택했다.
6. 문서 기반 질문을 입력했다.
7. 답변이 문서 내용을 기반으로 생성되었다.
8. 답변의 출처 또는 참조 문서를 확인했다.
9. Open WebUI 기본 문서 처리의 장점과 한계를 정리했다.
```

Step2-5B의 핵심 완료 기준은 다음이다.

```text
사용자가 웹 화면에서 사내 문서 기반 질의응답을 수행할 수 있는가?
```

---

## 11. Open WebUI를 사용할 때 주의할 점

Open WebUI는 빠르게 RAG를 체험하기에 좋은 도구이지만, 기업 RAG 전체를 대체하는 플랫폼으로 보기에는 주의가 필요하다.

특히 다음 사항을 확인해야 한다.

```text
문서 업로드 가능한 파일 형식
문서별 텍스트 추출 품질
Embedding 모델 설정
Vector DB 저장 위치
Knowledge별 접근 권한
사용자별 권한 제어
대화 로그 저장 여부
민감정보 포함 여부
외부 모델 사용 여부
사내망 또는 로컬망 운영 가능 여부
```

사내 문서에는 고객 정보, 제안 전략, 시스템 구성도, 내부 인력 정보, 보안 정책 등이 포함될 수 있다. 따라서 Open WebUI에 문서를 업로드하기 전에는 반드시 보안 정책을 확인해야 한다.

Public GitHub에 실습 문서를 올릴 경우에는 반드시 샘플 문서 또는 비식별화 문서만 사용해야 한다.

---

## 12. Step2-5 문서에 추가할 권장 설명

기존 Step2-5 문서에는 다음 내용을 추가하는 것이 좋다.

```text
Step2-5는 Open WebUI만 사용하는 실습이 아니다.
실전 사내 문서 RAG를 이해하려면 Python 기반 문서 전처리 파이프라인과 Open WebUI 기반 Knowledge 활용을 함께 이해해야 한다.

Python 기반 실습은 문서가 어떻게 Parser, Chunking, Embedding, Vector DB 저장 과정을 거치는지 확인하는 개발자 관점 실습이다.

Open WebUI 기반 실습은 사용자가 웹 화면에서 문서를 업로드하고 질문하는 사용자 관점 실습이다.

따라서 Step2-5는 Step2-5A와 Step2-5B로 분리하여 학습하는 것이 좋다.
```

---

## 13. 최종 정리

Step2-5에서 Open WebUI를 사용하는 것이 맞는지에 대한 답은 다음과 같다.

```text
맞다. Open WebUI를 사용할 수 있다.
하지만 Open WebUI만으로 Step2-5를 끝내면 실전 사내 문서 RAG의 내부 구조를 충분히 이해하기 어렵다.
```

따라서 Step2-5는 다음처럼 정리하는 것이 가장 좋다.

```text
Step2-5A. Python 기반 사내 문서 RAG 파이프라인 구축
- 문서 유형별 Parser 구현
- 텍스트 추출
- Metadata 생성
- Chunking
- Embedding
- ChromaDB 저장
- RAG 검색 및 답변 생성

Step2-5B. Open WebUI 기반 사내 문서 Knowledge 활용
- Knowledge 생성
- 문서 업로드
- Chat 질의응답
- 출처 확인
- 기본 기능의 한계 분석
```

AI-Data-Platform 프로젝트 관점에서는 두 단계를 모두 수행하는 것이 가장 바람직하다.

Python 기반 실습을 통해 RAG 내부 구조를 이해하고, Open WebUI 실습을 통해 사용자가 실제로 문서 기반 질의응답을 어떻게 사용하는지 확인할 수 있기 때문이다.

최종적으로 Step2-5의 핵심 메시지는 다음과 같다.

```text
실전 사내 문서 RAG는 Open WebUI 사용법만의 문제가 아니라,
문서를 어떻게 추출하고, 정제하고, Chunking하고, Metadata를 설계하고,
검색 가능한 지식으로 변환할 것인가의 문제이다.

Open WebUI는 그 결과를 사용자가 쉽게 활용하도록 도와주는 인터페이스이며,
Python 기반 전처리 파이프라인은 RAG 품질을 결정하는 핵심 기반이다.
```
