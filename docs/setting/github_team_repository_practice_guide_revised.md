# GitHub 팀 저장소 참여 및 실습파일 내려받기 가이드

> AI-Data-Platform 프로젝트에 참여하려는 팀원이 관리자에게 참여 요청을 보내고, GitHub 저장소 초대를 수락한 뒤, 문서와 실습파일을 로컬 환경에서 내려받아 실행하기 위한 가이드

---

## 1. 문서 작성 목적

이 문서는 **AI-Data-Platform 프로젝트의 신규 팀원**이 GitHub 저장소에 참여하고, 저장소에 등록된 MkDocs 문서와 실습파일을 로컬 PC로 내려받아 실행하는 방법을 설명하기 위한 가이드이다.

AI-Data-Platform 프로젝트는 다음 자산을 GitHub 저장소에서 함께 관리한다.

```text
1. MkDocs 기반 프로젝트 문서
2. 단계별 학습 가이드
3. Python 실습 코드
4. RAG 실습용 샘플 문서
5. 프로젝트 설정 파일
```

따라서 신규 팀원이 프로젝트에 참여하려면 먼저 **GitHub 저장소 접근 권한**을 받아야 한다. 특히 저장소가 Private Repository인 경우에는 저장소 주소를 알고 있더라도 권한이 없으면 저장소 내용을 볼 수 없고, Clone 또는 Pull도 수행할 수 없다.

이 문서는 다음 사용자를 대상으로 한다.

```text
1. AI-Data-Platform 프로젝트에 새로 참여하려는 팀원
2. GitHub 저장소 접근 권한을 처음 요청하는 사용자
3. 관리자로부터 GitHub 초대를 받아야 하는 사용자
4. 저장소에서 문서와 실습파일을 내려받아 실행하려는 사용자
5. MkDocs 문서와 labs 실습코드를 함께 확인하려는 사용자
```

---

## 2. MkDocs에 게시판 기능이 있는가?

현재 AI-Data-Platform 프로젝트는 **MkDocs와 GitHub Pages 기반의 정적 문서 사이트**로 운영된다.

MkDocs는 기본적으로 문서를 정적으로 생성해서 보여주는 도구이기 때문에 일반적인 웹 게시판처럼 사용자가 글을 작성하거나 신청서를 남기는 기능은 기본 제공되지 않는다.

물론 GitHub Issues, Discussions, Giscus, 별도 Form 서비스, 댓글 플러그인 등을 연동하면 유사한 접수 기능을 만들 수는 있다. 그러나 현재 프로젝트 운영 방식에서는 신규 참여 요청을 단순하고 명확하게 관리하기 위해 **이메일 접수 방식**을 사용한다.

따라서 프로젝트에 참여하고 싶은 팀원은 먼저 관리자에게 이메일로 참여 요청을 보내고, 관리자는 해당 정보를 기준으로 GitHub 저장소 초대를 발송한다.

---

## 3. 전체 진행 흐름

팀원이 프로젝트에 참여하고 실습파일을 사용하기까지의 전체 흐름은 다음과 같다.

```text
프로젝트 참여 의사 확인
   ↓
관리자에게 참여 요청 메일 발송
   ↓
관리자가 GitHub 계정 확인
   ↓
관리자가 GitHub 저장소 팀원 초대 발송
   ↓
팀원이 GitHub 초대 메일 수락
   ↓
저장소 접근 가능 여부 확인
   ↓
Git 설치 확인
   ↓
저장소 Clone
   ↓
실습 디렉터리 이동
   ↓
Python 가상환경 생성
   ↓
필요 라이브러리 설치
   ↓
실습파일 실행
```

이 과정에서 가장 먼저 필요한 것은 **관리자에게 본인의 GitHub 계정을 정확히 전달하는 것**이다.

관리자는 팀원의 GitHub 계정 또는 GitHub 가입 이메일을 알아야 저장소 초대를 보낼 수 있다. 따라서 참여 희망자는 GitHub 계정을 준비한 뒤, 아래 안내 형식에 맞춰 관리자에게 메일을 보내야 한다.

---

## 4. 프로젝트 참여 요청 방법

AI-Data-Platform 프로젝트에 참여하고 싶은 경우에는 아래 관리자 이메일로 참여 요청을 보낸다.

```text
관리자 이메일: minis24@gmail.com
```

메일 제목은 다음 형식을 사용한다.

```text
[프로젝트명] 프로젝트 참여 희망
```

예시는 다음과 같다.

```text
[AI-Data-Platform] 프로젝트 참여 희망
```

메일 본문에는 아래 정보를 포함한다.

```text
1. 이름
2. 연락처 및 이메일
3. GitHub 계정
4. 간단한 소개말
```

각 항목의 의미는 다음과 같다.

| 항목 | 설명 | 예시 |
|---|---|---|
| 이름 | 참여자의 실제 이름 | 홍길동 |
| 연락처 및 이메일 | 연락 가능한 전화번호 또는 이메일 | 010-0000-0000 / hong@example.com |
| GitHub 계정 | GitHub 사용자 ID 또는 가입 이메일 | honggildong |
| 간단한 소개말 | 프로젝트 참여 목적, 관심 분야, 현재 역할 등 | RAG 실습과 AI Data Platform 구축에 관심이 있습니다. |

---

## 5. 참여 요청 메일 작성 예시

아래 예시를 참고하여 관리자에게 메일을 보낸다.

```text
제목: [AI-Data-Platform] 프로젝트 참여 희망

안녕하세요.
AI-Data-Platform 프로젝트에 참여하고 싶어 메일드립니다.

아래와 같이 참여 요청 정보를 전달드립니다.

1. 이름
   - 홍길동

2. 연락처 및 이메일
   - 연락처: 010-0000-0000
   - 이메일: hong@example.com

3. GitHub 계정
   - GitHub ID: honggildong
   - GitHub 가입 이메일: hong@example.com

4. 간단한 소개말
   - AI Data Platform, RAG, Local LLM, 문서 자동화 실습에 관심이 있습니다.
   - 프로젝트 문서와 실습 코드를 함께 확인하며 학습하고 싶습니다.

확인 후 GitHub 저장소 초대 부탁드립니다.

감사합니다.
```

메일을 보낼 때 GitHub 계정 ID를 잘못 입력하면 관리자가 초대를 보낼 수 없거나, 다른 계정으로 초대가 발송될 수 있다. 따라서 GitHub ID와 가입 이메일을 다시 확인한 뒤 보내는 것이 좋다.

---

## 6. GitHub 계정 준비

팀원이 GitHub 저장소에 참여하려면 GitHub 계정이 필요하다.

아직 GitHub 계정이 없다면 먼저 계정을 생성해야 한다.

```text
1. GitHub 접속
2. Sign up 선택
3. 이메일 주소 입력
4. 사용자명 생성
5. 비밀번호 설정
6. 이메일 인증
```

GitHub 계정을 만들 때는 회사에서 사용하는 이메일을 사용하는 것이 관리 측면에서 좋다. 다만 이미 개인 GitHub 계정을 사용하고 있고, 프로젝트에서 허용한다면 기존 계정을 사용해도 된다.

팀원은 저장소 관리자에게 다음 정보를 전달한다.

```text
GitHub ID
GitHub 가입 이메일
사용자 이름
```

예시는 다음과 같다.

```text
GitHub ID: honggildong
Email: honggildong@example.com
Name: 홍길동
```

---

## 7. 저장소 관리자 작업: 팀원 초대

저장소 관리자는 참여 요청 메일에 포함된 GitHub 계정을 확인한 뒤 GitHub 저장소에 팀원을 초대한다.

관리자 작업 흐름은 다음과 같다.

```text
GitHub 저장소 접속
   ↓
Settings 이동
   ↓
Collaborators 또는 Collaborators and teams 메뉴 선택
   ↓
Add people 선택
   ↓
팀원의 GitHub ID 또는 이메일 입력
   ↓
권한 선택
   ↓
초대 발송
```

권한은 프로젝트 운영 방식에 따라 선택한다.

| 권한 | 설명 | 권장 대상 |
|---|---|---|
| Read | 저장소 조회와 Clone 가능 | 단순 학습자, 문서 확인자 |
| Triage | Issue, Pull Request 관리 일부 가능 | 리뷰 보조자 |
| Write | Push 가능 | 실습코드와 문서 작성자 |
| Maintain | 저장소 관리 일부 가능 | 프로젝트 리더, 운영 담당자 |
| Admin | 전체 설정 변경 가능 | 저장소 관리자 |

AI-Data-Platform 프로젝트에서 팀원이 문서와 실습파일을 수정하고 Pull Request 또는 Push까지 수행해야 한다면 `Write` 권한이 필요하다.

단순히 문서를 보고 실습파일을 내려받아 실행만 한다면 `Read` 권한으로도 충분하다.

---

## 8. 팀원 작업: 초대 수락

관리자가 초대하면 팀원에게 GitHub 초대 메일이 발송된다.

팀원은 다음 순서로 초대를 수락한다.

```text
1. GitHub 초대 메일 확인
2. View invitation 선택
3. GitHub 로그인
4. Accept invitation 선택
5. 저장소 접근 가능 여부 확인
```

초대를 수락하지 않으면 저장소 접근 권한이 활성화되지 않는다.

따라서 관리자가 초대했다고 하더라도 팀원이 반드시 초대 수락을 완료해야 한다.

---

## 9. 저장소 접근 확인

초대를 수락한 뒤 팀원은 브라우저에서 저장소에 접속해 접근 여부를 확인한다.

확인해야 할 항목은 다음과 같다.

```text
1. 저장소 메인 화면이 열리는가?
2. README.md 파일이 보이는가?
3. docs 디렉터리가 보이는가?
4. labs 디렉터리가 보이는가?
5. Code 버튼이 보이는가?
```

Private Repository에서 권한이 없으면 보통 다음과 같은 문제가 발생한다.

```text
404 Not Found
Repository not found
Authentication failed
Permission denied
```

이 경우에는 저장소 관리자에게 초대 수락 상태와 권한 설정을 다시 확인해달라고 요청해야 한다.

---

## 10. 로컬 PC에 Git 설치 확인

실습파일을 내려받으려면 로컬 PC에 Git이 설치되어 있어야 한다.

터미널에서 다음 명령을 실행한다.

```bash
git --version
```

정상적으로 설치되어 있으면 다음과 비슷한 결과가 나온다.

```bash
git version 2.45.0
```

Git이 설치되어 있지 않다면 운영체제에 맞게 설치한다.

```text
macOS: Homebrew 또는 Xcode Command Line Tools 사용
Windows: Git for Windows 설치
Linux: apt, yum, dnf 등 패키지 매니저 사용
```

macOS에서 Homebrew를 사용하는 경우 예시는 다음과 같다.

```bash
brew install git
```

Windows에서는 Git for Windows를 설치한 뒤 Git Bash, PowerShell, Windows Terminal 중 편한 도구를 사용하면 된다.

---

## 11. 저장소 Clone 방식 선택

GitHub 저장소를 로컬 PC로 내려받는 방법은 크게 두 가지가 있다.

```text
1. HTTPS 방식
2. SSH 방식
```

초기 학습 단계에서는 HTTPS 방식이 가장 단순하다.

```bash
git clone https://github.com/조직명/저장소명.git
```

SSH 방식은 SSH Key를 등록해야 하지만, 한 번 설정해두면 인증이 편하다.

```bash
git clone git@github.com:조직명/저장소명.git
```

처음 참여하는 팀원에게는 HTTPS 방식을 먼저 권장한다. 이후 GitHub 인증이나 Push 작업이 많아지면 SSH 방식을 설정해도 된다.

---

## 12. 저장소 Clone 실행

팀원은 작업할 디렉터리로 이동한 뒤 저장소를 Clone한다.

예시는 다음과 같다.

```bash
cd ~/projects
git clone https://github.com/Team-AI-Data-Platform/AI-Data-Platform.git
```

Clone이 완료되면 프로젝트 디렉터리로 이동한다.

```bash
cd AI-Data-Platform
```

현재 브랜치를 확인한다.

```bash
git branch
```

일반적으로 기본 브랜치는 `main`이다.

```bash
* main
```

---

## 13. 저장소 디렉터리 구조 확인

Clone 후 다음 구조가 있는지 확인한다.

```text
AI-Data-Platform/

├─ docs/
│  ├─ index.md
│  ├─ roadmap/
│  ├─ setting/
│  └─ study/
│
├─ labs/
│  └─ rag/
│
├─ mkdocs.yml
├─ README.md
└─ .gitignore
```

`docs` 디렉터리는 MkDocs 문서가 저장되는 위치이다.

`labs` 디렉터리는 Python 실습 코드가 저장되는 위치이다.

`mkdocs.yml`은 MkDocs 사이트의 목차와 설정을 관리하는 파일이다.

---

## 14. 최신 소스 내려받기

이미 Clone한 저장소가 있다면 실습 전에 최신 내용을 내려받는 것이 좋다.

```bash
git pull origin main
```

정상적으로 최신화되면 다음과 비슷한 메시지가 나온다.

```text
Already up to date.
```

또는 변경된 파일이 내려받아진다.

```text
Updating 123abcd..456efgh
Fast-forward
```

만약 로컬에서 수정한 파일과 원격 저장소의 변경이 충돌하면 Git 충돌 해결이 필요하다. 실습을 처음 진행하는 팀원은 충돌이 발생하면 임의로 처리하지 말고 프로젝트 담당자에게 문의하는 것이 안전하다.

---

## 15. Step2-5A 실습파일 위치

Step2-5A 실습파일은 다음 위치에 둔다.

```text
labs/rag/
```

권장 파일 구성은 다음과 같다.

```text
labs/rag/

├─ README.md
├─ requirements.txt
├─ step2_5_config.py
├─ step2_5_utils.py
├─ 09_extract_pdf.py
├─ 10_extract_pptx.py
├─ 11_extract_docx.py
├─ 12_extract_xlsx.py
├─ 13_build_enterprise_chunks.py
├─ 14_insert_enterprise_docs_to_chroma.py
├─ 15_enterprise_rag_search.py
│
├─ enterprise_docs/
│  ├─ pdf/
│  ├─ pptx/
│  ├─ docx/
│  ├─ xlsx/
│  ├─ md/
│  └─ txt/
│
├─ extracted_text/
├─ enterprise_chunks/
└─ chroma_db/
```

각 파일의 역할은 다음과 같다.

| 파일명 | 역할 |
|---|---|
| README.md | 실습파일 사용 방법 설명 |
| requirements.txt | Python 라이브러리 목록 |
| step2_5_config.py | 공통 경로와 설정값 관리 |
| step2_5_utils.py | 공통 유틸리티 함수 |
| 09_extract_pdf.py | PDF 텍스트 추출 |
| 10_extract_pptx.py | PPTX 슬라이드 텍스트 추출 |
| 11_extract_docx.py | DOCX 텍스트 추출 |
| 12_extract_xlsx.py | XLSX 문서 데이터 추출 |
| 13_build_enterprise_chunks.py | Chunk 생성 |
| 14_insert_enterprise_docs_to_chroma.py | ChromaDB 저장 |
| 15_enterprise_rag_search.py | RAG 검색 및 답변 생성 |

---

## 16. Python 가상환경 생성

프로젝트 루트 또는 `labs/rag` 디렉터리에서 Python 가상환경을 생성한다.

권장 위치는 프로젝트 루트이다.

```bash
cd AI-Data-Platform
python -m venv .venv
```

가상환경을 활성화한다.

macOS 또는 Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
.venv\Scripts\activate.bat
```

가상환경이 활성화되면 터미널 앞에 다음처럼 표시된다.

```bash
(.venv)
```

가상환경을 사용하는 이유는 프로젝트별로 Python 라이브러리 버전을 독립적으로 관리하기 위해서이다.

---

## 17. Python 라이브러리 설치

Step2-5A 실습파일 위치로 이동한다.

```bash
cd labs/rag
```

필요 라이브러리를 설치한다.

```bash
pip install -r requirements.txt
```

설치되는 주요 라이브러리는 다음과 같다.

| 라이브러리 | 역할 |
|---|---|
| pypdf | PDF 텍스트 추출 |
| python-pptx | PPTX 슬라이드 텍스트 추출 |
| python-docx | Word 문서 텍스트 추출 |
| openpyxl | Excel 문서 데이터 추출 |
| chromadb | Vector DB |
| sentence-transformers | Embedding 모델 |
| requests | Ollama API 호출 |

설치가 완료되면 다음 명령으로 확인할 수 있다.

```bash
pip list
```

---

## 18. 실습 문서 배치

실습 대상 문서는 문서 유형에 따라 다음 폴더에 넣는다.

```text
enterprise_docs/pdf/
enterprise_docs/pptx/
enterprise_docs/docx/
enterprise_docs/xlsx/
enterprise_docs/md/
enterprise_docs/txt/
```

예시는 다음과 같다.

```text
enterprise_docs/pdf/sample_rfp.pdf
enterprise_docs/pptx/sample_proposal.pptx
enterprise_docs/docx/sample_design.docx
enterprise_docs/xlsx/sample_requirements.xlsx
enterprise_docs/md/sample_manual.md
enterprise_docs/txt/sample_checklist.txt
```

실제 사내 문서를 사용할 경우에는 반드시 보안에 유의해야 한다.

GitHub에 올리는 실습 문서는 민감정보가 제거된 샘플 문서여야 한다.

---

## 19. Step2-5A 실습 실행 순서

실습은 다음 순서로 실행한다.

```bash
python 09_extract_pdf.py
python 10_extract_pptx.py
python 11_extract_docx.py
python 12_extract_xlsx.py
python 13_build_enterprise_chunks.py
python 14_insert_enterprise_docs_to_chroma.py
python 15_enterprise_rag_search.py "전자금융 장애 대응 절차를 알려줘"
```

각 단계의 의미는 다음과 같다.

```text
09~12: 문서 유형별 텍스트 추출
13: 추출 텍스트를 Chunk로 분리
14: Chunk를 Embedding하여 ChromaDB 저장
15: 질문을 입력하여 관련 문서 검색 및 답변 생성
```

처음에는 포함된 샘플 Markdown 또는 TXT 문서만으로도 13번 이후 실습이 가능하다.

PDF, PPTX, DOCX, XLSX 문서를 추가하면 09~12번 스크립트의 결과도 확인할 수 있다.

---

## 20. 생성 결과 확인

실습을 실행하면 다음 디렉터리에 결과가 생성된다.

```text
extracted_text/
enterprise_chunks/
chroma_db/
```

`extracted_text`에는 문서에서 추출한 텍스트가 JSONL 형태로 저장된다.

```text
extracted_text/pdf_extracted.jsonl
extracted_text/pptx_extracted.jsonl
extracted_text/docx_extracted.jsonl
extracted_text/xlsx_extracted.jsonl
```

`enterprise_chunks`에는 검색용 Chunk가 저장된다.

```text
enterprise_chunks/enterprise_chunks.jsonl
```

`chroma_db`에는 ChromaDB 데이터가 저장된다.

```text
chroma_db/
```

이 결과물들은 실습 실행 중 생성되는 데이터이므로 일반적으로 GitHub에 올리지 않는다.

---

## 21. Ollama 실행 확인

`15_enterprise_rag_search.py`는 Ollama가 실행 중이면 Local LLM으로 답변을 생성한다.

Ollama 서버를 실행한다.

```bash
ollama serve
```

사용할 모델을 내려받는다.

```bash
ollama pull llama3.1:8b
```

다른 터미널에서 RAG 검색을 실행한다.

```bash
python 15_enterprise_rag_search.py "전자금융 장애 발생 시 초기 확인 항목은?"
```

Ollama가 실행 중이 아니더라도 검색 결과는 출력되도록 구성할 수 있다. 다만 자연어 답변 생성은 Ollama가 실행 중이어야 한다.

---

## 22. MkDocs 문서 로컬 확인

문서 사이트를 로컬에서 확인하려면 프로젝트 루트로 이동한다.

```bash
cd AI-Data-Platform
```

MkDocs 관련 라이브러리가 설치되어 있어야 한다.

```bash
pip install mkdocs mkdocs-material pymdown-extensions
```

로컬 서버를 실행한다.

```bash
mkdocs serve
```

브라우저에서 다음 주소를 연다.

```text
http://127.0.0.1:8000
```

문서 목차에서 `Setting`, `Study`, `Step2 RAG` 항목이 정상적으로 보이는지 확인한다.

---

## 23. SourceTree로 내려받는 경우

Git 명령어가 익숙하지 않은 팀원은 SourceTree를 사용할 수 있다.

SourceTree 사용 흐름은 다음과 같다.

```text
SourceTree 실행
   ↓
Clone 선택
   ↓
GitHub 저장소 URL 입력
   ↓
로컬 저장 위치 선택
   ↓
Clone 실행
   ↓
파일 확인
```

SourceTree에서 Clone이 실패하는 경우는 대부분 다음 원인이다.

```text
1. GitHub 초대를 수락하지 않음
2. 저장소 접근 권한이 없음
3. GitHub 인증이 되지 않음
4. 저장소 URL이 잘못됨
5. 회사 네트워크 또는 프록시 제한
```

이 경우 먼저 브라우저에서 GitHub 저장소가 열리는지 확인해야 한다.

---

## 24. 자주 발생하는 문제

### 24.1 참여 요청 메일을 보냈는데 초대 메일이 오지 않음

원인:

```text
GitHub 계정 정보가 잘못되었거나 관리자가 아직 초대를 발송하지 않음
```

확인:

```text
1. 보낸 메일의 GitHub ID 확인
2. GitHub 가입 이메일 확인
3. 스팸 메일함 확인
4. 관리자에게 초대 발송 여부 확인
```

### 24.2 Repository not found

원인:

```text
저장소 주소가 잘못되었거나 접근 권한이 없음
```

확인:

```text
1. 저장소 URL 확인
2. GitHub 초대 수락 여부 확인
3. 저장소 권한 확인
```

### 24.3 Authentication failed

원인:

```text
GitHub 인증 실패
```

해결:

```text
1. GitHub 로그인 상태 확인
2. HTTPS 사용 시 Personal Access Token 필요 여부 확인
3. SSH 사용 시 SSH Key 등록 여부 확인
```

### 24.4 pip install 실패

원인:

```text
Python 버전 문제
네트워크 문제
가상환경 미활성화
패키지 충돌
```

해결:

```bash
python --version
pip --version
pip install --upgrade pip
pip install -r requirements.txt
```

### 24.5 ChromaDB 컬렉션을 찾을 수 없음

원인:

```text
14_insert_enterprise_docs_to_chroma.py를 실행하지 않음
```

해결:

```bash
python 13_build_enterprise_chunks.py
python 14_insert_enterprise_docs_to_chroma.py
```

### 24.6 Ollama 호출 실패

원인:

```text
Ollama 서버 미실행
모델 미설치
포트 충돌
```

해결:

```bash
ollama serve
ollama pull llama3.1:8b
```

---

## 25. GitHub에 올리면 안 되는 파일

다음 파일과 디렉터리는 GitHub에 올리지 않는 것이 좋다.

```text
site/
.venv/
venv/
__pycache__/
*.pyc
labs/rag/chroma_db/*
labs/rag/extracted_text/*
labs/rag/enterprise_chunks/*
.DS_Store
.vscode/
.idea/
```

실습 결과물은 사용자가 로컬에서 다시 생성할 수 있으므로 저장소에 올리지 않는다.

다만 폴더 구조 유지를 위해 `.gitkeep` 파일은 유지한다.

```text
labs/rag/chroma_db/.gitkeep
labs/rag/extracted_text/.gitkeep
labs/rag/enterprise_chunks/.gitkeep
```

---

## 26. 권장 .gitignore 설정

AI-Data-Platform 프로젝트에서는 다음 `.gitignore` 구성을 권장한다.

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
# Virtual Environment
# =========================

.venv/
venv/

# =========================
# Environment
# =========================

.env

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
# VSCode
# =========================

.vscode/

# =========================
# IntelliJ
# =========================

.idea/
*.iml
```

---

## 27. 목차 등록 예시

이 문서를 MkDocs 목차에 추가하려면 `mkdocs.yml`의 `Setting` 아래에 다음 항목을 추가한다.

```yaml
- Setting:
    - MkDocs 문서 사이트 구축 가이드: setting/mkdocs_github_pages_guide.md
    - MkDocs 문서 사이트 구축 가이드(windows): setting/mkdocs_github_pages_guide_windows.md
    - MkDocs 문서 Deploy 가이드: setting/mkdocs_github_pages_guide_deploy.md
    - Mac Mini 기반 AI LAB 구축 가이드: setting/macmini_ai_lab_guide.md
    - SourceTree 기반 GitHub 사용 가이드: setting/sourcetree_github_usage_guide.md
    - GitHub 팀 저장소 참여 및 실습파일 실행 가이드: setting/github_team_repository_practice_guide.md
```

문서 파일은 다음 위치에 저장한다.

```text
docs/setting/github_team_repository_practice_guide.md
```

---

## 28. 최종 정리

이 문서의 핵심은 팀원이 AI-Data-Platform 프로젝트에 참여 요청을 보내고, GitHub 저장소 초대를 수락한 뒤, 프로젝트 문서와 실습코드를 로컬 환경에서 확인하고 실행할 수 있도록 돕는 것이다.

전체 흐름은 다음과 같다.

```text
1. GitHub 계정 준비
2. 관리자에게 참여 요청 메일 발송
3. 관리자가 GitHub 저장소 초대 발송
4. 팀원이 GitHub 초대 수락
5. 저장소 접근 확인
6. Git 설치 확인
7. 저장소 Clone
8. 최신 소스 Pull
9. 실습 디렉터리 이동
10. 가상환경 생성
11. requirements.txt 설치
12. 실습파일 실행
13. MkDocs 문서 확인
```

현재 MkDocs 문서 사이트에는 게시판 기능이 없으므로, 신규 참여 요청은 이메일로 접수한다.

```text
관리자 이메일: minis24@gmail.com
메일 제목: [프로젝트명] 프로젝트 참여 희망
필수 내용: 이름, 연락처 및 이메일, GitHub 계정, 간단한 소개말
```

이 과정을 완료하면 팀원은 AI-Data-Platform 저장소의 문서와 실습코드를 동일한 환경에서 확인하고 실행할 수 있다.
