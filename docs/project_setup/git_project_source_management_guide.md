# Git 제외 파일(.gitignore) 설정 가이드

> 이 문서는 AI-Data-Platform 프로젝트에서 **Git으로 관리하지 않아야 할 파일과 디렉터리를 `.gitignore`로 설정하는 방법**을 설명한다.  
> Git 명령어 전반과 Branch, Commit, Push/Pull 등의 학습은 `기초 학습 > Git 핵심 가이드`에서 다루며, 본 문서에서는 프로젝트 환경 구성에 필요한 **Git 제외 파일 관리**에 집중한다.

---

## 1. 문서 작성 목적

프로젝트를 개발하다 보면 소스 코드와 문서 외에도 다양한 파일이 자동으로 생성된다.

예를 들면 다음과 같다.

```text
Python 가상환경
Python Cache
MkDocs 빌드 결과
IDE 설정 파일
로그 파일
환경변수 파일
RAG 실행 결과
Vector DB 데이터
운영체제 임시 파일
```

이러한 파일을 모두 GitHub Repository에 올리면 다음과 같은 문제가 발생할 수 있다.

```text
불필요한 파일 증가
        ↓
Repository 용량 증가
        ↓
팀원별 환경 파일 충돌
        ↓
변경 파일이 지나치게 많아짐
        ↓
민감정보가 Repository에 포함될 위험
```

따라서 Git에서 관리해야 하는 파일과 관리하지 않아야 하는 파일을 구분해야 한다.

`.gitignore`는 이러한 **Git 관리 제외 대상을 정의하는 설정 파일**이다.

---

## 2. `.gitignore`란?

`.gitignore`는 Git이 새로운 파일이나 디렉터리를 추적할 때 **관리 대상에서 제외할 경로 패턴을 정의하는 파일**이다.

일반적으로 프로젝트 루트 디렉터리에 위치한다.

```text
AI-Data-Platform/
│
├─ .git/
├─ .gitignore
├─ docs/
├─ labs/
├─ mkdocs.yml
└─ README.md
```

예를 들어 `.gitignore`에 다음 내용을 작성할 수 있다.

```gitignore
.venv/
site/
__pycache__/
*.pyc
.env
```

이 설정은 다음 파일과 디렉터리를 Git 관리 대상에서 제외한다.

```text
.venv/
→ Python 가상환경

site/
→ MkDocs 빌드 결과

__pycache__/
*.pyc
→ Python Cache

.env
→ 환경변수 및 Secret 설정 파일
```

---

## 3. 왜 `.gitignore`가 필요한가?

Git Repository에는 일반적으로 **프로젝트를 구성하는 원본 자산**을 저장한다.

예:

```text
Git으로 관리

Python Source
Markdown 문서
mkdocs.yml
requirements.txt
설정 파일
공개 가능한 샘플 데이터
```

반면 다시 생성할 수 있거나 사용자 PC마다 달라지는 파일은 Git에서 제외하는 것이 좋다.

```text
Git에서 제외

Python 가상환경
Cache
Log
MkDocs 빌드 결과
IDE 개인 설정
RAG 생성 결과
Vector DB 데이터
Local LLM 모델
Secret / API Key
```

핵심 원칙은 다음과 같다.

> **소스와 프로젝트 설정은 Git으로 관리하고, 재생성 가능한 실행 결과와 개인 개발환경 파일은 Git에서 제외한다.**

---

## 4. `.gitignore` 기본 문법

### 4.1 특정 파일 제외

```gitignore
.env
```

`.env` 파일을 제외한다.

---

### 4.2 특정 디렉터리 제외

```gitignore
.venv/
```

`.venv` 디렉터리 전체를 제외한다.

---

### 4.3 특정 확장자 제외

```gitignore
*.log
```

확장자가 `.log`인 모든 파일을 제외한다.

예:

```text
application.log
error.log
server.log
```

---

### 4.4 특정 이름의 디렉터리 제외

```gitignore
__pycache__/
```

Python 실행 중 생성되는 `__pycache__` 디렉터리를 제외한다.

---

### 4.5 예외 파일 포함

`!`를 사용하면 제외 규칙 안에서 특정 파일만 다시 Git 관리 대상으로 허용할 수 있다.

예:

```gitignore
labs/rag/chroma_db/*
!labs/rag/chroma_db/.gitkeep
```

의미:

```text
chroma_db/ 내부 파일
→ 모두 제외

.gitkeep
→ 예외적으로 Git 관리
```

---

## 5. Python 가상환경 제외

Python 가상환경은 프로젝트마다 다시 생성할 수 있으므로 Git Repository에 올리지 않는다.

대표적인 가상환경 디렉터리는 다음과 같다.

```text
.venv/
venv/
```

`.gitignore`에 다음과 같이 설정한다.

```gitignore
# Python Virtual Environment
.venv/
venv/
```

가상환경에는 설치된 Python 패키지들이 포함되므로 파일 개수가 매우 많을 수 있다.

```text
.venv/
├─ Scripts/ 또는 bin/
├─ Lib/ 또는 lib/
└─ site-packages/
```

팀원은 Repository에서 가상환경 자체를 내려받는 것이 아니라 자신의 PC에서 새로 생성한다.

```bash
python -m venv .venv
```

---

## 6. Python Cache 파일 제외

Python 프로그램을 실행하면 다음과 같은 Cache 파일이 생성될 수 있다.

```text
__pycache__/
*.pyc
*.pyo
```

이 파일들은 Python이 실행 과정에서 자동으로 생성하며 프로젝트 원본 소스가 아니다.

다음과 같이 제외한다.

```gitignore
# Python Cache
__pycache__/
*.pyc
*.pyo
```

---

## 7. MkDocs 빌드 결과 제외

MkDocs에서 다음 명령을 실행하면 정적 웹사이트 결과물이 생성된다.

```bash
mkdocs build
```

기본적으로 다음 디렉터리가 생성된다.

```text
site/
```

구조 예:

```text
site/
├─ index.html
├─ assets/
├─ search/
└─ ...
```

`site/`는 `docs/`와 `mkdocs.yml`을 기반으로 다시 생성할 수 있는 결과물이므로 일반적으로 Git Source Branch에서는 관리하지 않는다.

```gitignore
# MkDocs Build
site/
```

> GitHub Pages 배포 과정에서 `gh-pages` Branch에 생성되는 배포 결과와 프로젝트 Source Branch의 `site/` 디렉터리는 구분해서 이해한다.

---

## 8. 환경변수 및 Secret 파일 제외

AI 프로젝트에서는 API Key, Token, 비밀번호 등이 환경변수 파일에 저장될 수 있다.

예:

```text
.env
.env.local
.env.dev
```

이 파일들은 GitHub에 올라가지 않도록 해야 한다.

```gitignore
# Environment / Secret
.env
.env.*
```

예를 들어 다음과 같은 내용이 `.env`에 들어갈 수 있다.

```text
OPENAI_API_KEY=...
DATABASE_PASSWORD=...
API_TOKEN=...
```

이러한 값은 Repository에 Commit하지 않는다.

> API Key나 비밀번호 등 실제 Secret이 이미 GitHub에 Push된 경우 `.gitignore`에 추가하는 것만으로는 보안 문제가 해결되지 않는다. 해당 Credential을 즉시 폐기하거나 재발급해야 한다.

---

## 9. 로그 파일 제외

애플리케이션이나 실습을 실행하면서 로그 파일이 생성될 수 있다.

```text
application.log
server.log
error.log
```

다음 설정으로 `.log` 파일을 제외할 수 있다.

```gitignore
# Log
*.log
```

---

## 10. Jupyter 및 테스트 Cache 제외

Jupyter Notebook이나 pytest를 사용할 경우 다음 디렉터리가 자동 생성될 수 있다.

```text
.ipynb_checkpoints/
.pytest_cache/
```

다음과 같이 제외한다.

```gitignore
# Jupyter
.ipynb_checkpoints/

# pytest
.pytest_cache/
```

---

## 11. RAG 생성 데이터 제외

AI-Data-Platform의 RAG 실습에서는 실행 과정에서 여러 중간 결과가 생성될 수 있다.

예:

```text
문서
 ↓
Text Extraction
 ↓
extracted_text/
 ↓
Chunking
 ↓
enterprise_chunks/
 ↓
Embedding
 ↓
chroma_db/
```

이 파일들은 실습 코드에서 다시 생성할 수 있는 결과 데이터이다.

대표적으로 다음 디렉터리를 Git에서 제외한다.

```text
labs/rag/chroma_db/
labs/rag/extracted_text/
labs/rag/enterprise_chunks/
```

권장 설정:

```gitignore
# RAG Generated Data

labs/rag/chroma_db/*
!labs/rag/chroma_db/.gitkeep

labs/rag/extracted_text/*
!labs/rag/extracted_text/.gitkeep

labs/rag/enterprise_chunks/*
!labs/rag/enterprise_chunks/.gitkeep
```

이렇게 하면 실행 결과는 제외하면서 디렉터리 구조는 유지할 수 있다.

---

## 12. `.gitkeep`이란?

Git은 기본적으로 **비어 있는 디렉터리 자체를 관리하지 않는다.**

예를 들어 다음 디렉터리가 비어 있다고 가정한다.

```text
labs/rag/chroma_db/
```

빈 디렉터리만 존재하면 Git Repository에 해당 폴더가 유지되지 않는다.

그래서 빈 파일 하나를 두어 폴더를 유지하는 방법을 많이 사용한다.

```text
labs/rag/chroma_db/.gitkeep
```

`.gitkeep`은 Git에서 특별히 예약된 기능은 아니다.

단순히 **빈 디렉터리를 Git Repository에 유지하기 위해 관례적으로 사용하는 파일명**이다.

예:

```text
labs/rag/chroma_db/
└─ .gitkeep
```

`.gitignore`에서는 다음과 같이 설정한다.

```gitignore
labs/rag/chroma_db/*
!labs/rag/chroma_db/.gitkeep
```

---

## 13. Local LLM 모델은 Git에 올리지 않는다

Ollama와 같은 Local LLM 실행 도구에서 다운로드하는 모델은 Repository에서 관리하지 않는다.

LLM 모델은 수 GB에서 수십 GB 이상의 용량을 사용할 수 있다.

```text
Git Repository
→ 소스 / 문서 / 설정

Local AI Environment
→ Ollama Model / Cache / Vector DB
```

Repository에는 모델 Binary 대신 필요한 모델명과 설치 방법을 문서로 기록한다.

예:

```bash
ollama pull gemma3:4b
```

각 팀원은 자신의 로컬 환경에서 모델을 다운로드한다.

---

## 14. 운영체제별 임시 파일 제외

### macOS

macOS에서는 Finder가 다음 파일을 자동 생성할 수 있다.

```text
.DS_Store
```

제외:

```gitignore
# macOS
.DS_Store
```

---

### Windows

Windows에서는 다음과 같은 시스템 파일이 생성될 수 있다.

```text
Thumbs.db
Desktop.ini
```

제외:

```gitignore
# Windows
Thumbs.db
Desktop.ini
```

---

## 15. IDE 설정 파일 제외

IDE의 프로젝트 설정은 사용자별로 달라질 수 있다.

### VS Code

```text
.vscode/
```

### IntelliJ IDEA / PyCharm

```text
.idea/
*.iml
```

필요에 따라 다음과 같이 제외할 수 있다.

```gitignore
# VS Code
.vscode/

# IntelliJ / PyCharm
.idea/
*.iml
```

> 프로젝트에서 공통으로 공유해야 하는 VS Code 설정이나 Extension 추천 파일 등이 있다면 `.vscode/` 전체를 제외하기보다 필요한 파일만 선택적으로 관리하는 방식을 사용할 수도 있다.

---

## 16. AI-Data-Platform 권장 `.gitignore`

현재 프로젝트 환경을 기준으로 다음과 같이 구성할 수 있다.

```gitignore
# =========================
# MkDocs
# =========================

site/

# =========================
# Python
# =========================

__pycache__/
*.pyc
*.pyo

# =========================
# Python Virtual Environment
# =========================

.venv/
venv/

# =========================
# Environment / Secret
# =========================

.env
.env.*

# =========================
# Logs
# =========================

*.log

# =========================
# Jupyter
# =========================

.ipynb_checkpoints/

# =========================
# pytest
# =========================

.pytest_cache/

# =========================
# RAG Generated Data
# =========================

labs/rag/chroma_db/*
!labs/rag/chroma_db/.gitkeep

labs/rag/extracted_text/*
!labs/rag/extracted_text/.gitkeep

labs/rag/enterprise_chunks/*
!labs/rag/enterprise_chunks/.gitkeep

# =========================
# macOS
# =========================

.DS_Store

# =========================
# Windows
# =========================

Thumbs.db
Desktop.ini

# =========================
# VS Code
# =========================

.vscode/

# =========================
# IntelliJ / PyCharm
# =========================

.idea/
*.iml
```

프로젝트 구조가 변경되거나 새로운 도구를 추가할 경우 `.gitignore`도 함께 검토한다.

---

## 17. `.gitignore` 설정 확인

`.gitignore`를 작성한 뒤 Git에서 제외 규칙이 적용되고 있는지 확인할 수 있다.

다음 명령을 실행한다.

```bash
git status
```

예를 들어 `.venv/`가 `.gitignore`에 정상적으로 등록되어 있다면 가상환경 내부의 수많은 파일이 `Untracked files`에 나타나지 않아야 한다.

특정 파일이나 디렉터리가 어떤 ignore 규칙에 의해 제외되는지 확인하려면 다음 명령을 사용할 수 있다.

```bash
git check-ignore -v <파일경로>
```

예:

```bash
git check-ignore -v .venv/
```

예상되는 형태:

```text
.gitignore:15:.venv/    .venv/
```

이는 `.gitignore`의 해당 규칙에 의해 `.venv/`가 제외되었다는 의미이다.

---

## 18. `.gitignore`인데 파일이 계속 표시되는 경우

`.gitignore`는 기본적으로 **아직 Git에서 추적하지 않는 파일에 적용**된다.

이미 Git에 Commit되어 추적 중인 파일은 `.gitignore`에 추가해도 계속 관리된다.

예를 들어 `.env`가 이미 Git 관리 대상이라고 가정한다.

`.gitignore`에 다음을 추가한다.

```gitignore
.env
```

하지만 이미 추적 중이라면 Git 상태에서 계속 나타날 수 있다.

이 경우 Git 추적 대상에서만 제거해야 한다.

```bash
git rm --cached .env
```

이 명령은 로컬 `.env` 파일을 삭제하지 않고 Git의 추적 대상에서 제거한다.

그 다음 변경 사항을 Commit한다.

```bash
git commit -m "Stop tracking .env file"
```

---

## 19. 이미 추적 중인 디렉터리를 제외하는 경우

디렉터리가 이미 Git 관리 대상이라면 `-r` 옵션을 사용한다.

예:

```bash
git rm -r --cached .venv
```

그 다음 Commit한다.

```bash
git commit -m "Stop tracking virtual environment"
```

> `git rm --cached`와 실제 파일 삭제 명령을 혼동하지 않도록 주의한다.  
> 실행 전 `git status`를 확인하고 중요한 파일은 별도로 백업하는 것이 좋다.

---

## 20. 실제로 Git이 추적 중인 파일 확인

Git에서 현재 추적하고 있는 파일은 다음 명령으로 확인할 수 있다.

```bash
git ls-files
```

특정 파일을 찾으려면 운영체제에 따라 다음과 같이 사용할 수 있다.

### macOS / Linux

```bash
git ls-files | grep ".env"
```

### Windows PowerShell

```powershell
git ls-files | Select-String ".env"
```

결과가 출력된다면 해당 파일은 현재 Git 관리 대상이다.

---

## 21. 실습 문서와 데이터 보안

RAG 실습에서는 다음과 같은 문서를 사용할 수 있다.

```text
PDF
PPTX
DOCX
XLSX
Markdown
TXT
```

실제 업무 문서를 사용하는 경우 다음 정보가 포함되어 있지 않은지 확인한다.

- 개인정보
- 고객정보
- 회사 내부정보
- 계약 및 재무정보
- 비밀번호
- API Key
- 시스템 접속정보
- 외부 공개가 허용되지 않은 문서

Repository에는 가능한 한 **공개 가능한 샘플 데이터 또는 비식별화된 실습 자료**만 등록한다.

`.gitignore`는 실수 방지에 도움이 되지만, 보안 정책을 대신하는 것은 아니다.

---

## 22. `.gitignore` 수정 시 권장 절차

새로운 개발 도구나 실습 환경을 추가하면서 자동 생성 파일이 늘어났다면 다음 순서로 확인한다.

```text
새로운 파일/디렉터리 생성
        ↓
git status 확인
        ↓
Git 관리가 필요한 파일인지 판단
        ↓
불필요하면 .gitignore 추가
        ↓
git status 다시 확인
        ↓
필요한 파일만 Commit
```

예:

```bash
git status
```

`.venv/`가 표시된다면:

```gitignore
.venv/
```

추가 후 다시:

```bash
git status
```

를 확인한다.

---

## 23. Git에서 관리할 파일과 제외할 파일

### Git 관리 권장

```text
docs/**/*.md
labs/**/*.py
mkdocs.yml
README.md
requirements.txt
.gitignore
공개 가능한 Sample Data
```

### Git 제외 권장

```text
.venv/
site/
__pycache__/
*.pyc
.env
*.log
Vector DB 실행 데이터
RAG 중간 생성 데이터
Local LLM Model
OS 임시 파일
개인 IDE 설정
```

이를 표로 정리하면 다음과 같다.

| 항목 | Git 관리 | 이유 |
|---|---|---|
| Python 소스 | O | 프로젝트 핵심 자산 |
| Markdown 문서 | O | 프로젝트 문서 원본 |
| `mkdocs.yml` | O | 문서 사이트 설정 |
| `requirements.txt` | O | 패키지 재현에 필요 |
| `.gitignore` | O | 팀 공통 제외 규칙 |
| `.venv/` | X | 로컬에서 재생성 가능 |
| `site/` | X | MkDocs로 재생성 가능 |
| `.env` | X | Secret 포함 가능 |
| `__pycache__/` | X | 자동 생성 Cache |
| Vector DB 결과 | X | 실습에서 재생성 가능 |
| Ollama 모델 | X | 대용량 Local 모델 |

---

## 24. 프로젝트 초기 구성 시 체크리스트

프로젝트를 처음 Clone하거나 새 개발환경을 구성한 뒤 다음을 확인한다.

- [ ] 프로젝트 루트에 `.gitignore`가 존재한다.
- [ ] `.venv/`가 제외되어 있다.
- [ ] Python Cache가 제외되어 있다.
- [ ] MkDocs `site/`가 제외되어 있다.
- [ ] `.env`가 제외되어 있다.
- [ ] 로그 파일이 제외되어 있다.
- [ ] RAG 생성 데이터가 제외되어 있다.
- [ ] macOS / Windows 임시 파일이 제외되어 있다.
- [ ] IDE 개인 설정 제외 여부를 확인했다.
- [ ] `git status`에 불필요한 파일이 나타나지 않는다.
- [ ] 실제 업무용 민감 문서가 Git 대상에 포함되지 않았다.

---

## 25. 최종 정리

`.gitignore`의 목적은 단순히 Git 상태 화면을 깨끗하게 만드는 것이 아니다.

프로젝트에서 **실제로 공유해야 할 자산과 로컬에서만 필요한 파일을 구분하는 기준**이다.

AI-Data-Platform에서는 다음 원칙을 기본으로 한다.

```text
Git Repository

문서
Python 소스
설정
패키지 목록
공개 가능한 샘플 데이터
        ↓
팀원과 공유
```

반면 다음 항목은 로컬 개발환경에서 관리한다.

```text
.venv
Cache
Log
MkDocs site
Vector DB
RAG 생성 결과
Local LLM Model
Secret
        ↓
Git에서 제외
```

핵심적으로 다음 항목은 반드시 기억한다.

```gitignore
.venv/
site/
__pycache__/
*.pyc
.env
*.log
```

그리고 RAG 실습 결과 역시 필요에 따라 제외한다.

```gitignore
labs/rag/chroma_db/*
labs/rag/extracted_text/*
labs/rag/enterprise_chunks/*
```

`.gitignore`를 적절하게 관리하면 Repository의 불필요한 용량 증가와 팀원 간 환경 파일 충돌을 줄이고, API Key나 환경설정과 같은 민감정보가 실수로 GitHub에 등록되는 위험도 줄일 수 있다.
