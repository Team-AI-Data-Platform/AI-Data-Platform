# 개발 장비 구성 참고 가이드

> 이 문서는 AI Data Platform 학습 및 실습을 진행할 때 사용할 개발 장비의 구성 원칙과 권장 사양을 정리한 참고 가이드이다.  
> 특정 장비 한 대를 표준으로 강제하기보다는, 팀원 각자가 보유한 **Windows 노트북, MacBook, Mac Mini 등 다양한 장비에서 동일한 프로젝트를 수행할 수 있도록 기준을 제공하는 것**을 목적으로 한다.

---

## 1. 개요

AI Data Platform 프로젝트는 다음과 같은 학습과 실습을 단계적으로 진행한다.

```text
Local LLM
   ↓
RAG
   ↓
AI Agent
   ↓
AI Data Platform
   ↓
AI Serving Platform
```

각 단계에서 필요한 컴퓨팅 자원은 조금씩 다르다.

예를 들어 Git, Python, MkDocs와 같은 기본 개발환경은 일반적인 개발 노트북에서도 충분히 사용할 수 있지만, Local LLM을 직접 실행하거나 여러 AI 서비스를 동시에 구동하려면 상대적으로 많은 메모리가 필요하다.

따라서 본 프로젝트에서는 다음 원칙으로 개발 장비를 구성한다.

```text
팀원별 로컬 개발환경 구성
        ↓
Windows / macOS 환경 지원
        ↓
Git Repository를 통한 동일 소스 관리
        ↓
필요 시 고사양 장비를 AI LAB 서버로 활용
```

---

## 2. 개발 장비 구성 기본 원칙

본 프로젝트에서는 특정 운영체제나 특정 장비를 필수 조건으로 지정하지 않는다.

팀원은 자신이 사용하는 장비에 맞게 로컬 개발환경을 구성할 수 있다.

대표적인 구성은 다음과 같다.

| 구분 | 예시 | 활용 |
|---|---|---|
| Windows 노트북 | 일반 업무용/개발용 노트북 | Python, RAG, Agent 실습 |
| MacBook | MacBook Air / Pro | Python, Local LLM, RAG, Agent 실습 |
| Mac Mini | Apple Silicon 기반 Mac Mini | 개인 개발환경 또는 공용 AI LAB |
| 고사양 데스크톱 | Windows + NVIDIA GPU | Local LLM, GPU 기반 AI 실습 |

프로젝트 소스와 문서는 Git Repository를 통해 공유하므로, 운영체제가 다르더라도 동일한 프로젝트 구조와 학습 과정을 유지할 수 있다.

---

## 3. 운영체제별 환경 구성

본 프로젝트에서는 Windows와 macOS 환경을 모두 지원한다.

### 3.1 Windows

Windows 환경에서는 일반적으로 다음 도구를 설치한다.

```text
Git
 ↓
Python
 ↓
Python 가상환경(.venv)
 ↓
MkDocs
 ↓
AI 학습 및 실습 패키지
```

Windows 관련 상세 설치 방법은 별도의 가이드를 참고한다.

```text
프로젝트 환경 구성
 └─ 로컬 환경(Windows) 세팅하기
      ├─ Git 설치 및 기본 설정
      ├─ Python 설치 및 환경 설정
      └─ MkDocs 설치 가이드
```

---

### 3.2 macOS

macOS 환경에서도 기본적인 구성 방식은 Windows와 동일하다.

```text
Git
 ↓
Python
 ↓
Python 가상환경(.venv)
 ↓
MkDocs
 ↓
AI 학습 및 실습 패키지
```

다만 명령어, PATH 설정, Python 설치 방식, 가상환경 활성화 방법 등 일부 절차는 Windows와 다르다.

macOS 관련 상세 설치 방법은 별도의 가이드를 참고한다.

```text
프로젝트 환경 구성
 └─ 로컬 환경(macOS) 세팅하기
      ├─ Git 설치 및 GitHub 설정
      ├─ Python 설치 및 환경 설정
      └─ MkDocs 설치 가이드
```

---

## 4. 학습 단계별 장비 요구 수준

AI Data Platform 학습 과정은 단계가 진행될수록 필요한 시스템 자원이 증가한다.

### 4.1 기본 개발 및 문서 작성

대상 작업:

- Git
- Python
- VS Code 등 IDE
- MkDocs
- Markdown 문서 작성
- 기본 Python 실습

이 단계에서는 높은 사양이 필요하지 않다.

| 항목 | 권장 수준 |
|---|---|
| CPU | 일반적인 최신 멀티코어 CPU |
| Memory | 16GB 이상 권장 |
| Storage | SSD 256GB 이상 |
| GPU | 필수 아님 |

---

### 4.2 RAG 실습

대상 작업:

- 문서 Parsing
- Chunking
- Embedding
- Vector DB
- 문서 검색
- LLM 연동

RAG 자체는 반드시 고성능 GPU가 필요한 작업은 아니다.

다만 PDF, PPTX, DOCX 등의 문서를 많이 처리하거나 여러 서비스를 동시에 실행할 경우 메모리 사용량이 증가한다.

| 항목 | 권장 수준 |
|---|---|
| CPU | 6 Core 이상 권장 |
| Memory | 16GB 이상, 24GB 이상 권장 |
| Storage | SSD 512GB 이상 권장 |
| GPU | 필수 아님 |

---

### 4.3 Local LLM 실습

Local LLM을 직접 실행하는 경우에는 메모리가 가장 중요한 요소 중 하나이다.

모델 크기가 커질수록 더 많은 메모리가 필요하다.

대략적인 학습 기준은 다음과 같이 볼 수 있다.

| 모델 규모 | 권장 활용 |
|---|---|
| 3B ~ 4B | 기본 실습, 저사양 장비 |
| 7B ~ 8B | 일반적인 Local LLM 학습 |
| 12B ~ 14B | RAG 및 Agent 실습 |
| 30B 이상 | 고사양 장비에서 선택적으로 활용 |

> 실제 메모리 사용량은 모델의 Quantization 방식, Context Window, 동시 실행 프로그램 등에 따라 달라질 수 있다.

학습 목적에서는 반드시 가장 큰 모델을 사용할 필요는 없다.

본 프로젝트에서는 **8B ~ 14B 수준의 모델을 중심으로 학습하는 방식**이 현실적이다.

---

### 4.4 AI Agent 실습

AI Agent 단계에서는 다음 구성요소를 동시에 실행할 수 있다.

```text
Agent Application
      +
Local LLM
      +
Vector DB
      +
Embedding Model
      +
External Tool / API
```

따라서 단순한 LLM 실행보다 메모리 여유가 있는 장비가 편리하다.

| 항목 | 권장 수준 |
|---|---|
| Memory | 24GB 이상 권장 |
| Storage | SSD 512GB 이상 권장 |
| GPU | Local LLM 사용 방식에 따라 선택 |

외부 LLM API를 사용하는 경우 로컬 장비의 요구 사양은 낮아질 수 있다.

---

## 5. 메모리 기준 참고

AI 학습환경에서는 CPU 성능도 중요하지만, Local LLM을 실행할 경우 특히 메모리 용량이 중요하다.

개발 장비를 선택할 때 다음과 같이 참고할 수 있다.

### 16GB

적합한 작업:

- Python 학습
- MkDocs
- 일반 개발
- API 기반 LLM 실습
- 기본 RAG
- 소형 Local LLM

제약:

- Local LLM과 Vector DB 등 여러 서비스를 동시에 실행할 때 메모리가 부족할 수 있음
- 12B 이상의 모델을 활용할 경우 제약이 커질 수 있음

---

### 24GB

적합한 작업:

- Python / RAG
- Local LLM 7B ~ 8B
- Agent 실습
- Ollama + Vector DB 동시 실행

AI 학습용 노트북 환경으로 비교적 균형이 좋은 수준이다.

---

### 32GB 이상

적합한 작업:

- Local LLM 8B ~ 14B
- RAG
- AI Agent
- Open WebUI
- Vector DB
- Docker 기반 서비스
- 여러 AI 구성요소 동시 실행

AI Data Platform 전체 학습 과정을 하나의 장비에서 진행하려는 경우 가장 여유로운 구성이 된다.

---

## 6. Windows 장비 구성 참고

Windows 노트북이나 데스크톱을 사용할 경우 CPU 기반으로도 대부분의 기본 학습을 진행할 수 있다.

NVIDIA GPU가 있는 장비라면 CUDA를 지원하는 AI Framework와 Local LLM을 활용할 때 추가적인 성능 향상을 기대할 수 있다.

다만 본 프로젝트의 초기 학습 과정에서는 GPU 사용을 필수 조건으로 두지 않는다.

초기에는 다음 환경을 우선 구성한다.

```text
Windows
  ↓
Git
  ↓
Python
  ↓
.venv
  ↓
MkDocs
  ↓
RAG / Agent 개발환경
```

Local LLM은 장비 사양에 따라 Ollama 등의 도구를 추가로 구성한다.

---

## 7. macOS 장비 구성 참고

Apple Silicon 기반 Mac은 CPU와 GPU가 Unified Memory를 공유하는 구조를 사용한다.

따라서 Local LLM을 실행할 때 장비의 전체 Unified Memory 용량이 중요한 기준이 된다.

예를 들어 다음과 같은 Apple Silicon 장비를 활용할 수 있다.

```text
MacBook Air
MacBook Pro
Mac Mini
```

macOS에서는 Ollama와 같은 Local LLM 실행 환경을 비교적 간단하게 구성할 수 있으며, Python 기반 RAG 및 Agent 실습도 동일하게 진행할 수 있다.

특히 24GB 또는 32GB 이상의 Unified Memory를 가진 장비는 AI 학습용 개발환경으로 활용하기에 여유가 있다.

---

## 8. Mac Mini 활용 참고

Mac Mini는 반드시 필요한 장비는 아니다.

기본적으로는 팀원 각자의 Windows 노트북이나 MacBook에서 개별 개발환경을 구성한다.

```text
팀원 A
Windows Notebook

팀원 B
MacBook

팀원 C
Mac Mini
```

하지만 고사양 Mac Mini가 별도로 존재하는 경우 필요에 따라 공용 AI LAB 형태로 활용할 수도 있다.

예를 들어 다음과 같은 서비스를 Mac Mini에 구성할 수 있다.

```text
Mac Mini
 ├─ Ollama
 ├─ Open WebUI
 ├─ Vector DB
 ├─ MinIO
 └─ AI Agent Service
```

팀원들은 브라우저 또는 API를 통해 공용 AI 환경에 접근할 수 있다.

```text
             +---------------------+
             |      Mac Mini       |
             |     AI LAB Server   |
             +----------+----------+
                        |
                  Wi-Fi / LAN
                        |
        +---------------+---------------+
        |               |               |
   Windows Notebook   MacBook       Other Client
```

이 방식은 다음과 같은 상황에서 유용하다.

- 팀원 PC의 사양이 서로 다른 경우
- 대용량 모델을 한 곳에서 관리하고 싶은 경우
- Ollama 모델 다운로드를 중복하고 싶지 않은 경우
- Open WebUI 등 공용 AI 서비스를 운영하고 싶은 경우
- 동일한 RAG / Agent 실습환경을 공유하고 싶은 경우

따라서 Mac Mini는 **기본 개발환경이 아니라 선택적인 공용 AI LAB 장비**로 이해하는 것이 적절하다.

---

## 9. 로컬 개발환경과 공용 AI LAB의 차이

두 환경은 목적이 다르다.

| 구분 | 로컬 개발환경 | 공용 AI LAB |
|---|---|---|
| 사용자 | 개별 팀원 | 여러 팀원 |
| 장비 | Windows / MacBook / Mac Mini | 고사양 Mac Mini 또는 서버 |
| Python 개발 | O | O |
| MkDocs | O | 선택 |
| Local LLM | 장비 사양에 따라 | O |
| Open WebUI | 선택 | O |
| Vector DB | 로컬 실습 | 공용 구성 가능 |
| Agent 개발 | O | 공용 서비스 가능 |
| 목적 | 개인 개발 및 실습 | 공용 AI 환경 |

본 프로젝트에서는 **로컬 개발환경을 기본으로 하고, 공용 AI LAB은 필요에 따라 선택적으로 구성**한다.

---

## 10. 저장공간 참고

AI 학습에서는 Python 소스 자체보다 AI 모델과 문서 데이터가 많은 저장공간을 사용할 수 있다.

주요 저장 대상은 다음과 같다.

```text
Python 패키지
Docker Image
Ollama Model
Embedding Model
Vector DB 데이터
PDF / PPTX / DOCX
실습 데이터
```

특히 Local LLM 모델은 하나의 모델이 수 GB 이상의 공간을 사용할 수 있다.

따라서 AI 학습을 지속적으로 진행할 장비라면 최소 512GB 이상의 SSD를 권장하며, 여러 모델과 데이터를 장기간 보관한다면 1TB 이상도 고려할 수 있다.

---

## 11. 권장 장비 구성 예시

### 기본 개발형

```text
Memory : 16GB
SSD    : 512GB
GPU    : 선택

활용
- Python
- Git
- MkDocs
- 기본 RAG
- API 기반 LLM
```

---

### AI 학습 균형형

```text
Memory : 24GB 이상
SSD    : 512GB ~ 1TB

활용
- Local LLM 7B ~ 8B
- RAG
- AI Agent
- Vector DB
- Ollama
```

---

### AI LAB 활용형

```text
Memory : 32GB 이상
SSD    : 1TB 권장

활용
- Local LLM 8B ~ 14B
- Open WebUI
- RAG
- Vector DB
- AI Agent
- Docker 서비스
- 여러 구성요소 동시 실행
```

---

## 12. 개발환경 구성 권장 흐름

팀원이 프로젝트에 참여할 때는 장비 종류와 관계없이 다음 순서로 환경을 구성한다.

```text
1. 개발 장비 준비
       ↓
2. 운영체제 확인
       ↓
3. Git 설치
       ↓
4. Python 설치
       ↓
5. Python 가상환경 구성
       ↓
6. MkDocs 설치
       ↓
7. 프로젝트 소스 내려받기
       ↓
8. AI 학습 단계별 환경 구성
```

운영체제별 상세 설치 방법은 `프로젝트 환경 구성`의 각 가이드를 참고한다.

---

## 13. 장비 선택 시 고려사항

개발 장비를 선택하거나 업그레이드할 때 단순히 CPU 성능만 비교하기보다는 다음 항목을 함께 고려하는 것이 좋다.

### 메모리

Local LLM 실행 가능 모델 크기와 동시에 실행할 수 있는 서비스 수에 영향을 준다.

### 저장공간

AI 모델, Docker Image, Vector DB, 문서 데이터가 지속적으로 누적된다.

### 휴대성

개인 노트북으로 활용하는 경우 성능뿐 아니라 무게와 배터리도 중요하다.

### GPU

대규모 AI 모델 학습이나 GPU 기반 Framework를 직접 사용할 계획이라면 중요하지만, 본 프로젝트의 기본 학습 과정에서는 필수 조건은 아니다.

### 운영체제

Windows와 macOS 모두 사용할 수 있으며, 프로젝트에서는 운영체제별 설치 가이드를 별도로 제공한다.

---

## 14. 정리

본 프로젝트의 개발환경은 특정 장비에 종속되지 않는다.

핵심 원칙은 다음과 같다.

```text
Windows / macOS 모두 지원

        +

팀원별 로컬 개발환경 구성

        +

Git을 통한 동일 프로젝트 관리

        +

필요 시 고사양 장비를 공용 AI LAB으로 활용
```

따라서 Mac Mini는 필수 개발환경이 아니라 여러 선택지 중 하나이며, Windows 노트북이나 MacBook에서도 동일한 학습과 실습을 진행할 수 있다.

장비 선택 시에는 현재 학습 단계와 목적에 맞춰 적절한 사양을 선택하는 것이 중요하다.

특히 Local LLM, RAG, AI Agent를 하나의 장비에서 함께 실습하려면 **메모리와 저장공간에 여유가 있는 장비**가 유리하다.
