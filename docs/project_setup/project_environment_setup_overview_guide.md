# 프로젝트 환경 구성 가이드

## 1. 개요

이 문서는 **AI-Data-Platform 프로젝트를 새로운 PC에서 처음 시작하거나, 기존 개발 환경을 다시 구성할 때 필요한 전체 절차를 안내하는 시작 문서**이다.

프로젝트를 정상적으로 사용하려면 단순히 Git 저장소의 소스를 내려받는 것만으로는 충분하지 않다.  
Git과 GitHub를 사용할 수 있는 환경을 준비하고, Python을 설치한 뒤 프로젝트별 가상환경을 구성해야 한다.

또한 운영체제에 따라 설치 방법과 명령어가 다르므로, 이 가이드에서는 전체 흐름을 먼저 이해한 뒤 **Windows 또는 macOS 환경에 맞는 상세 가이드**를 선택하여 진행하도록 구성한다.

> 이 문서는 개별 프로그램의 세부 설치 방법을 모두 설명하는 문서가 아니다.  
> 프로젝트 환경 구성의 **전체 흐름과 구성 항목을 안내하는 인덱스 역할**을 하며, 실제 설치 및 설정 방법은 운영체제별 상세 가이드에서 다룬다.

---

## 2. 프로젝트 환경 구성 목적

AI-Data-Platform 프로젝트의 소스와 학습 자료는 GitHub Repository를 기준으로 관리한다.

따라서 새로운 PC에서 프로젝트를 시작하려면 다음 환경이 기본적으로 준비되어 있어야 한다.

```text
Git / GitHub
    ↓
프로젝트 Repository Clone
    ↓
Python
    ↓
Python 가상환경(.venv)
    ↓
Python 패키지 관리(pip)
    ↓
프로젝트 개발 및 실습 준비
```

추가적으로 Git 작업을 보다 편리하게 수행하기 위해 SourceTree와 같은 GUI 기반 개발 유틸리티를 사용할 수 있다.

---

## 3. 환경 구성 범위

프로젝트 환경 구성은 크게 다음 세 영역으로 구분한다.

```text
프로젝트 환경 구성
│
├─ 로컬 개발 환경
│   ├─ Git / GitHub
│   └─ Python
│
├─ 개발 유틸리티
│   └─ SourceTree
│
└─ 프로젝트별 추가 환경
    ├─ MkDocs
    ├─ Local LLM
    ├─ RAG
    └─ AI Agent
```

여기서 중요한 점은 **모든 프로그램을 처음부터 한꺼번에 설치하지 않는 것**이다.

Git과 Python은 프로젝트의 기본 로컬 환경으로 구성하고, MkDocs나 Ollama와 같은 프로그램은 실제 해당 기능을 사용할 때 관련 가이드에서 추가로 설치한다.

---

## 4. 기본 로컬 개발 환경

### 4.1 Git / GitHub

Git은 프로젝트 소스의 버전을 관리하기 위한 형상관리 도구이다.

GitHub는 Git Repository를 원격에서 공유하고 협업하기 위해 사용하는 서비스이다.

AI-Data-Platform 프로젝트에서는 GitHub Repository를 기준으로 프로젝트 소스와 문서를 관리하므로, 가장 먼저 Git을 사용할 수 있는 환경이 필요하다.

주요 구성 내용은 다음과 같다.

- Git 설치
- Git 설치 여부 및 버전 확인
- Git 사용자 정보 설정
- GitHub 계정 및 Repository 접근 확인
- 프로젝트 Repository Clone
- 프로젝트 소스 최신화(Pull)
- 기본적인 Commit / Push 작업 확인

> Git은 로컬 PC에 설치하는 프로그램이고, GitHub는 원격 Repository를 제공하는 서비스이다.  
> 따라서 정확한 표현은 **"Git 설치 및 GitHub 설정"**이다.

---

### 4.2 Python

AI-Data-Platform의 여러 실습은 Python을 기반으로 작성되어 있다.

RAG, LLM 호출, AI Agent 등의 실습을 진행하려면 Python 실행 환경이 필요하므로 프로젝트 초기 환경 구성 단계에서 Python을 설치한다.

주요 구성 내용은 다음과 같다.

- Python 설치
- Python 버전 확인
- pip 확인
- 프로젝트 가상환경 생성
- 가상환경 활성화
- pip 업데이트
- Python 실행 환경 정상 여부 확인

---

### 4.3 Python 가상환경(.venv)

Python 프로젝트에서는 PC 전체에 라이브러리를 설치하기보다 **프로젝트별 가상환경을 만들어 사용하는 것을 권장**한다.

예를 들어 AI-Data-Platform 프로젝트의 루트 디렉터리에 다음과 같이 `.venv`를 생성할 수 있다.

```text
AI-Data-Platform
│
├─ .venv
├─ docs
├─ labs
├─ mkdocs.yml
└─ ...
```

`.venv`는 해당 프로젝트에서 사용하는 Python과 Python 라이브러리를 다른 프로젝트와 분리하여 관리하기 위한 공간이다.

이를 통해 다음과 같은 문제를 줄일 수 있다.

- 프로젝트마다 서로 다른 라이브러리 버전을 사용할 수 있음
- 시스템 Python 환경을 불필요하게 변경하지 않음
- 다른 Python 프로젝트와 라이브러리 충돌을 줄일 수 있음
- 개발 PC가 변경되어도 프로젝트 환경을 다시 구성하기 쉬움

> Windows에서 생성한 `.venv`와 macOS에서 생성한 `.venv`는 서로 호환되지 않는다.  
> Git Repository에 기존 `.venv`가 있더라도 다른 운영체제에서 그대로 사용하지 말고 새로 생성하는 것이 원칙이다.

---

## 5. 운영체제별 환경 구성

Git과 Python의 기본 개념은 동일하지만 실제 설치 방법과 명령어는 Windows와 macOS에서 차이가 있다.

따라서 프로젝트 환경 구성 문서는 운영체제를 기준으로 구분한다.

### 5.1 Windows

Windows 사용자는 다음 순서로 환경을 구성한다.

```text
Windows PC
    │
    ├─ Git 설치 및 GitHub 설정
    │     ↓
    │   Repository Clone
    │
    └─ Python 설치 및 환경 설정
          ↓
        .venv 생성
          ↓
        PowerShell에서 가상환경 활성화
          ↓
        pip 확인 및 업데이트
```

Windows에서는 특히 다음 사항을 확인해야 한다.

- Git for Windows 설치 여부
- `git` 명령어 PATH 인식 여부
- Python 설치 및 PATH 인식 여부
- PowerShell에서 Python 가상환경 활성화
- PowerShell ExecutionPolicy에 의한 `Activate.ps1` 실행 오류

예를 들어 PowerShell의 스크립트 실행 정책으로 가상환경 활성화가 차단될 수 있다.

이 경우 상세 Windows Python 환경 구성 가이드에서 안전한 범위의 해결 방법을 안내한다.

---

### 5.2 macOS

macOS 사용자는 다음 순서로 환경을 구성한다.

```text
macOS
   │
   ├─ Git 설치 및 GitHub 설정
   │     ↓
   │   Repository Clone
   │
   └─ Python 설치 및 환경 설정
         ↓
       .venv 생성
         ↓
       Terminal에서 가상환경 활성화
         ↓
       pip 확인 및 업데이트
```

macOS에서는 다음 사항을 중심으로 확인한다.

- Git 설치 및 버전 확인
- GitHub Repository 접근
- Python 설치 및 버전 확인
- `python3` / `pip3` 명령어 확인
- `.venv` 가상환경 생성
- Terminal에서 가상환경 활성화

---

## 6. 개발 유틸리티

### 6.1 SourceTree

Git은 명령어만으로도 충분히 사용할 수 있지만, Git 작업 상태를 시각적으로 확인하고 Commit, Pull, Push, Branch 등의 작업을 보다 편리하게 수행하기 위해 SourceTree를 사용할 수 있다.

SourceTree는 **필수 개발 환경이 아니라 편의성을 높이기 위한 개발 유틸리티**로 분류한다.

```text
Git
 └─ 프로젝트 형상관리의 필수 도구

SourceTree
 └─ Git을 편리하게 사용하기 위한 GUI 유틸리티
```

따라서 Git 설치와 Repository Clone이 정상적으로 가능한 상태를 먼저 만든 후 SourceTree를 추가로 설치하는 것이 좋다.

---

## 7. 프로젝트 기본 환경과 추가 환경의 구분

프로젝트 환경을 처음 구성할 때 모든 프로그램을 설치할 필요는 없다.

### 기본 환경

프로젝트를 내려받고 Python 기반 실습을 준비하기 위한 기본 환경이다.

| 구분 | 구성 요소 | 용도 |
|---|---|---|
| 형상관리 | Git | 프로젝트 소스 버전 관리 |
| 원격 Repository | GitHub | 프로젝트 공유 및 협업 |
| 개발 언어 | Python | AI/RAG/Agent 실습 실행 |
| Python 환경 | venv | 프로젝트별 Python 환경 분리 |
| 패키지 관리 | pip | Python 라이브러리 설치 및 관리 |

### 개발 편의 도구

| 구분 | 구성 요소 | 용도 |
|---|---|---|
| Git GUI | SourceTree | Git 작업을 GUI로 수행 |

### 프로젝트 기능별 추가 환경

다음 항목은 프로젝트 기본 환경 구성에서 설치하지 않고, 해당 기능을 학습하거나 사용할 때 관련 가이드에서 설치한다.

| 구성 요소 | 사용 영역 | 비고 |
|---|---|---|
| MkDocs | 문서 관리 | MkDocs 문서 관리 가이드에서 구성 |
| Material for MkDocs | 문서 관리 | MkDocs 테마 |
| Ollama | Local LLM | AI Lab - Local LLM 단계 |
| Open WebUI | Local LLM | AI Lab - Local LLM 단계 |
| ChromaDB / Vector DB | RAG | AI Lab - RAG 단계 |
| LangChain / LangGraph | AI Agent | AI Agent 학습 단계 |
| Qdrant / MinIO 등 | AI Data Platform | 플랫폼 확장 단계 |

이렇게 영역을 분리하면 프로젝트 환경 구성 문서가 불필요하게 복잡해지는 것을 방지할 수 있다.

---

## 8. 권장 환경 구성 순서

새로운 PC에서 AI-Data-Platform 프로젝트를 시작할 때는 다음 순서를 권장한다.

### Step 1. 운영체제 확인

현재 사용하는 개발 PC의 운영체제를 확인한다.

```text
Windows
또는
macOS
```

운영체제에 맞는 상세 가이드를 선택한다.

---

### Step 2. Git 설치 및 확인

Git을 설치하고 정상적으로 사용할 수 있는지 확인한다.

```bash
git --version
```

정상적으로 Git 버전이 출력되는지 확인한다.

---

### Step 3. GitHub Repository 접근 확인

GitHub 프로젝트에 접근할 수 있는지 확인하고 Repository를 Clone한다.

```bash
git clone <Repository URL>
```

Clone이 완료되면 프로젝트 폴더로 이동한다.

```bash
cd AI-Data-Platform
```

---

### Step 4. Python 설치 및 확인

Python을 설치하고 버전을 확인한다.

```bash
python --version
```

운영체제와 설치 방식에 따라 다음 명령을 사용할 수도 있다.

```bash
python3 --version
```

---

### Step 5. Python 가상환경 구성

프로젝트 루트에서 `.venv` 가상환경을 생성한다.

```bash
python -m venv .venv
```

운영체제에 따라 가상환경 활성화 방법이 다르므로 상세 가이드를 참고한다.

---

### Step 6. pip 확인 및 업데이트

가상환경이 활성화된 상태에서 pip를 확인한다.

```bash
python -m pip --version
```

필요한 경우 pip를 업데이트한다.

```bash
python -m pip install --upgrade pip
```

---

### Step 7. 기본 개발 환경 구성 완료

다음 항목이 모두 정상이라면 프로젝트 기본 환경 구성이 완료된 것이다.

```text
[완료] Git 명령어 사용 가능
[완료] GitHub Repository Clone 완료
[완료] Python 실행 가능
[완료] Python 가상환경 생성 완료
[완료] 가상환경 활성화 가능
[완료] pip 사용 가능
```

이후 필요한 작업에 따라 MkDocs, Local LLM, RAG, AI Agent 등의 환경을 추가로 구성한다.

---

## 9. 환경 구성 완료 후 다음 단계

기본 환경 구성이 끝난 후에는 목적에 따라 다음 가이드를 진행한다.

```text
프로젝트 기본 환경 구성 완료
          │
          ├─ 문서 작성/관리
          │     └─ MkDocs 문서 관리
          │
          ├─ Local LLM 실습
          │     └─ Ollama / Open WebUI
          │
          ├─ RAG 실습
          │     └─ Vector DB / Embedding / Retrieval
          │
          └─ AI Agent 실습
                └─ LangChain / LangGraph / MCP
```

프로젝트의 모든 환경을 한 번에 구성하는 것이 아니라, **기본 환경을 먼저 안정적으로 구성하고 학습 단계에 따라 필요한 환경을 추가하는 방식**을 권장한다.

---

## 10. 프로젝트 환경 구성 메뉴 구조

MkDocs Navigation에서는 다음과 같은 구조로 운영하는 것을 권장한다.

```yaml
- 프로젝트 환경 구성:
    - 환경 구성 개요:
        # 이 문서

    - 로컬 환경(Windows) 세팅하기:
        - Git 설치 및 GitHub 설정:
        - Python 설치 및 환경 설정:

    - 로컬 환경(macOS) 세팅하기:
        - Git 설치 및 GitHub 설정:
        - Python 설치 및 환경 설정:

    - 개발 유틸리티:
        - SourceTree 설치 및 사용:
```

각 문서는 역할을 명확하게 분리한다.

| 문서 | 역할 |
|---|---|
| 환경 구성 개요 | 전체 환경 구성 순서와 문서 위치 안내 |
| Windows - Git/GitHub | Windows에서 Git 설치부터 Repository Clone까지 |
| Windows - Python | Windows에서 Python, venv, pip 환경 구성 |
| macOS - Git/GitHub | macOS에서 Git 설치부터 Repository Clone까지 |
| macOS - Python | macOS에서 Python, venv, pip 환경 구성 |
| SourceTree | Git 작업 편의를 위한 GUI 도구 설치 및 사용 |

---

## 11. 문서 운영 원칙

프로젝트 환경 구성 문서는 다음 원칙으로 관리한다.

### 11.1 환경 구성과 학습 내용을 분리한다

Python 설치 방법과 Python 문법 학습은 서로 다른 목적의 문서이다.

```text
Python 설치 및 환경 설정
→ 개발 환경 구성

Python 핵심 가이드
→ Python 기초 학습
```

따라서 Python 문법, 자료구조, 함수 등의 학습 내용은 프로젝트 환경 구성 메뉴에 포함하지 않는다.

---

### 11.2 운영체제별 절차는 별도 문서로 제공한다

Windows와 macOS는 Git/Python의 개념은 동일하지만 설치와 환경 설정 방법에 차이가 있다.

하나의 문서에서 계속 Windows/macOS 절차를 번갈아 설명하기보다, 사용자가 자신의 운영체제에 해당하는 문서 하나만 처음부터 끝까지 따라갈 수 있도록 분리한다.

---

### 11.3 필수 환경과 편의 도구를 구분한다

Git과 Python은 프로젝트 기본 환경이지만 SourceTree는 필수 프로그램이 아니다.

따라서 다음과 같이 구분한다.

```text
로컬 개발 환경
→ 프로젝트 실행에 필요한 기본 환경

개발 유틸리티
→ 개발 작업을 보다 편리하게 하기 위한 선택 도구
```

---

### 11.4 기능별 설치는 해당 학습 가이드에서 관리한다

MkDocs, Ollama, Open WebUI, LangChain, LangGraph 등의 설치 방법을 프로젝트 환경 구성 문서에 모두 포함하지 않는다.

해당 프로그램을 실제로 사용하는 학습 단계 또는 기능별 가이드에서 설치와 설정을 설명한다.

이 원칙을 유지하면 Navigation이 복잡해지는 것을 방지하고, 오랜만에 프로젝트에 접속한 경우에도 필요한 문서를 쉽게 찾을 수 있다.

---

## 12. 최종 정리

AI-Data-Platform 프로젝트의 기본 환경 구성은 다음 세 가지 관점으로 이해하면 된다.

```text
1. 프로젝트 소스를 관리하기 위한 환경
   → Git / GitHub

2. 프로젝트의 Python 코드를 실행하기 위한 환경
   → Python / venv / pip

3. 개발 작업을 편리하게 하기 위한 도구
   → SourceTree
```

기본 환경 구성이 완료된 이후 MkDocs, Local LLM, RAG, AI Agent 등의 환경은 각 학습 단계에서 필요한 시점에 추가로 구성한다.

따라서 새로운 PC에서 프로젝트를 다시 시작할 때는 먼저 **프로젝트 환경 구성 → 환경 구성 개요**를 확인한 후, 자신의 운영체제에 맞는 **Windows 또는 macOS 로컬 환경 세팅 가이드**를 순서대로 진행하면 된다.
