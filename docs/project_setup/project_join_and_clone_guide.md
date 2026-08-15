# 프로젝트 참여 및 소스 받기 가이드

> 이 문서는 **AI-Data-Platform 프로젝트에 새로 참여하는 팀원**이 프로젝트 참여를 요청하고, GitHub 저장소 초대를 수락한 뒤, 프로젝트 소스를 로컬 PC로 내려받는 방법을 설명한다.  
> 본 가이드에서는 **프로젝트 참여 → GitHub 권한 확인 → 저장소 Clone → 최신 소스 Pull**까지를 다룬다.  
> Python, MkDocs, Ollama 등의 상세 설치 및 환경 설정은 운영체제별 별도 가이드를 참고한다.

---

## 1. 문서 작성 목적

AI-Data-Platform 프로젝트의 문서와 실습 코드는 GitHub Repository에서 통합 관리한다.

저장소에는 다음과 같은 프로젝트 자산이 포함될 수 있다.

```text
AI-Data-Platform Repository

├─ MkDocs 기반 프로젝트 문서
├─ AI 학습 가이드
├─ Python 실습 코드
├─ RAG / Agent 실습 코드
├─ 실습용 샘플 문서
└─ 프로젝트 설정 파일
```

따라서 신규 팀원이 프로젝트에 참여하려면 먼저 GitHub 저장소에 접근할 수 있는 권한을 받아야 한다.

특히 저장소가 **Private Repository**인 경우 저장소 주소를 알고 있더라도 접근 권한이 없으면 내용을 조회하거나 Clone할 수 없다.

본 문서의 목표는 다음과 같다.

```text
프로젝트 참여 요청
        ↓
GitHub 저장소 초대
        ↓
초대 수락
        ↓
저장소 접근 확인
        ↓
프로젝트 Clone
        ↓
최신 소스 확인
        ↓
로컬 환경 구성 단계로 이동
```

---

## 2. 대상 독자

이 문서는 다음 사용자를 대상으로 한다.

- AI-Data-Platform 프로젝트에 새로 참여하는 팀원
- GitHub 저장소 접근 권한을 처음 요청하는 사용자
- 관리자로부터 GitHub 초대를 받아야 하는 사용자
- 프로젝트 문서와 실습 코드를 로컬 PC로 내려받으려는 사용자
- GitHub Repository를 처음 Clone하는 사용자

---

## 3. 전체 진행 흐름

프로젝트 참여부터 로컬 소스 확보까지의 전체 흐름은 다음과 같다.

```text
GitHub 계정 준비
       ↓
프로젝트 참여 요청
       ↓
관리자가 GitHub 계정 확인
       ↓
GitHub 저장소 초대 발송
       ↓
팀원이 초대 수락
       ↓
저장소 접근 가능 여부 확인
       ↓
Git 설치 여부 확인
       ↓
저장소 Clone
       ↓
프로젝트 구조 확인
       ↓
최신 소스 Pull 방법 확인
       ↓
운영체제별 로컬 환경 구성
```

> 메뉴상으로는 `프로젝트 참여 및 소스 받기`가 운영체제별 로컬 환경 구성보다 앞에 위치한다.  
> 다만 실제 `git clone` 명령을 사용하려면 Git이 설치되어 있어야 한다.  
> Git이 설치되어 있지 않은 경우 운영체제별 **Git 설치 가이드**를 먼저 진행한 뒤 다시 본 문서로 돌아온다.

---

## 4. GitHub 계정 준비

프로젝트에 참여하려면 GitHub 계정이 필요하다.

GitHub 계정이 없다면 먼저 GitHub에서 계정을 생성한다.

일반적인 가입 흐름은 다음과 같다.

```text
GitHub 접속
   ↓
Sign up
   ↓
이메일 입력
   ↓
사용자명 생성
   ↓
비밀번호 설정
   ↓
이메일 인증
   ↓
GitHub 계정 생성 완료
```

이미 개인 또는 회사 GitHub 계정을 사용하고 있다면 프로젝트 운영 정책에 따라 기존 계정을 사용할 수 있다.

프로젝트 참여 요청 전에 다음 정보를 확인해 둔다.

```text
GitHub ID
GitHub 가입 이메일
사용자 이름
```

예시:

```text
GitHub ID : honggildong
Email     : hong@example.com
Name      : 홍길동
```

GitHub ID를 잘못 전달하면 관리자가 다른 계정을 초대하거나 초대를 정상적으로 발송하지 못할 수 있으므로 정확하게 확인한다.

---

## 5. 프로젝트 참여 요청

AI-Data-Platform 프로젝트에 참여하려는 팀원은 프로젝트 관리자에게 참여를 요청한다.

현재 프로젝트에서는 별도의 가입 게시판을 운영하지 않고 **이메일을 통해 참여 요청을 접수**하는 방식으로 관리한다.

관리자 이메일:

```text
minis24@gmail.com
```

메일 제목은 다음 형식을 권장한다.

```text
[AI-Data-Platform] 프로젝트 참여 희망
```

메일 본문에는 다음 정보를 포함한다.

```text
1. 이름
2. 연락처 및 이메일
3. GitHub 계정
4. 간단한 소개말
```

---

## 6. 프로젝트 참여 요청 메일 예시

다음 형식을 참고하여 참여 요청 메일을 작성한다.

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
   - Local LLM, RAG, AI Agent 및 AI Data Platform 학습에 관심이 있습니다.
   - 프로젝트 문서와 실습 코드를 기반으로 함께 학습하고 싶습니다.

확인 후 GitHub 저장소 초대 부탁드립니다.

감사합니다.
```

참여 요청 메일을 보내기 전에 GitHub ID와 이메일 주소를 다시 확인한다.

---

## 7. 저장소 관리자 작업 - 팀원 초대

관리자는 참여 요청에 포함된 GitHub 계정을 확인한 뒤 프로젝트 Repository에 팀원을 초대한다.

일반적인 흐름은 다음과 같다.

```text
GitHub Repository 접속
        ↓
Settings
        ↓
Collaborators / Collaborators and teams
        ↓
Add people
        ↓
GitHub ID 또는 이메일 검색
        ↓
권한 설정
        ↓
Invitation 발송
```

GitHub 조직 또는 Repository 설정에 따라 메뉴 명칭과 권한 관리 방식은 일부 다를 수 있다.

---

## 8. Repository 권한 이해

팀원에게 부여하는 권한은 프로젝트에서 수행할 역할에 따라 달라질 수 있다.

대표적인 권한은 다음과 같다.

| 권한 | 주요 용도 |
|---|---|
| Read | 저장소 조회 및 Clone |
| Triage | Issue 및 Pull Request 관리 보조 |
| Write | 소스 및 문서 Push |
| Maintain | Repository 운영 관리 |
| Admin | 전체 Repository 설정 관리 |

프로젝트 문서와 실습 코드를 단순 조회하고 내려받는 목적이라면 Read 권한으로 시작할 수 있다.

팀원이 문서나 실습 코드를 직접 수정하여 Repository에 반영해야 한다면 프로젝트 운영 정책에 따라 Write 이상의 권한이 필요할 수 있다.

---

## 9. 팀원 작업 - GitHub 초대 수락

관리자가 저장소 초대를 발송하면 팀원은 GitHub에서 초대를 확인한다.

일반적인 흐름은 다음과 같다.

```text
GitHub 초대 확인
      ↓
GitHub 로그인
      ↓
Invitation 확인
      ↓
Accept invitation
      ↓
Repository 접근
```

초대 메일이 발송된 경우 이메일의 초대 링크를 통해 이동할 수도 있다.

> 관리자가 초대를 발송했더라도 팀원이 초대를 수락하지 않으면 저장소 접근 권한이 정상적으로 활성화되지 않을 수 있다.

---

## 10. 저장소 접근 확인

초대를 수락한 뒤 브라우저에서 AI-Data-Platform 저장소에 접속한다.

다음 항목을 확인한다.

```text
1. Repository 메인 화면이 정상적으로 열리는가?
2. README.md가 보이는가?
3. docs/ 디렉터리가 보이는가?
4. labs/ 디렉터리가 보이는가?
5. Code 버튼을 사용할 수 있는가?
```

정상적으로 보인다면 Repository 접근 권한이 부여된 상태이다.

접근 권한에 문제가 있는 경우 다음과 같은 메시지를 볼 수 있다.

```text
404 Not Found
Repository not found
Permission denied
Authentication failed
```

이 경우 다음 사항을 확인한다.

```text
GitHub 로그인 계정
GitHub 초대 수락 여부
Repository 접근 권한
Repository 주소
```

---

## 11. Git 설치 여부 확인

프로젝트 소스를 Clone하려면 로컬 PC에 Git이 설치되어 있어야 한다.

터미널 또는 PowerShell에서 다음 명령을 실행한다.

```bash
git --version
```

정상적으로 설치되어 있으면 다음과 비슷하게 표시된다.

```text
git version 2.x.x
```

Git이 설치되어 있지 않다면 본 문서에서 Git 설치를 진행하지 않고 운영체제별 별도 가이드를 참고한다.

### Windows

```text
프로젝트 환경 구성
 └─ 로컬 환경(Windows) 세팅하기
      └─ Git 설치 및 기본 설정
```

### macOS

```text
프로젝트 환경 구성
 └─ 로컬 환경(macOS) 세팅하기
      └─ Git 설치 및 GitHub 설정
```

Git 설치를 완료한 뒤 다시 본 문서의 Clone 단계로 돌아온다.

---

## 12. Clone이란?

`Clone`은 GitHub의 원격 Repository를 자신의 로컬 PC로 처음 내려받는 작업이다.

```text
GitHub Repository
       ↓
    git clone
       ↓
Local PC
```

Clone을 수행하면 Repository의 파일뿐 아니라 Git이 프로젝트의 변경 이력을 관리하는 데 필요한 정보도 함께 생성된다.

예를 들어 다음과 같은 프로젝트가 생성된다.

```text
AI-Data-Platform/
├─ .git/
├─ docs/
├─ labs/
├─ mkdocs.yml
├─ README.md
└─ .gitignore
```

`.git` 디렉터리는 Git이 Repository의 상태와 이력을 관리하기 위해 사용하는 영역이다.

---

## 13. HTTPS와 SSH 방식

GitHub Repository를 Clone하는 대표적인 방식은 다음 두 가지이다.

```text
HTTPS
SSH
```

### HTTPS

예:

```text
https://github.com/Team-AI-Data-Platform/AI-Data-Platform.git
```

Clone 명령:

```bash
git clone https://github.com/Team-AI-Data-Platform/AI-Data-Platform.git
```

처음 프로젝트에 참여하는 경우 비교적 이해하기 쉬운 방식이다.

### SSH

예:

```text
git@github.com:Team-AI-Data-Platform/AI-Data-Platform.git
```

Clone 명령:

```bash
git clone git@github.com:Team-AI-Data-Platform/AI-Data-Platform.git
```

SSH 방식은 사전에 GitHub 계정에 SSH Key를 등록해야 한다.

본 프로젝트의 기본 가이드에서는 HTTPS 방식을 중심으로 설명한다.

---

## 14. 작업 디렉터리 준비

소스 코드를 저장할 상위 디렉터리를 준비한다.

### Windows 예시

```powershell
C:\projects
```

해당 디렉터리가 없다면 생성할 수 있다.

```powershell
mkdir C:\projects
```

이동한다.

```powershell
cd C:\projects
```

### macOS 예시

```bash
~/projects
```

디렉터리를 생성한다.

```bash
mkdir -p ~/projects
```

이동한다.

```bash
cd ~/projects
```

---

## 15. Repository Clone

프로젝트 Repository를 Clone한다.

```bash
git clone https://github.com/Team-AI-Data-Platform/AI-Data-Platform.git
```

정상적으로 진행되면 Git이 프로젝트 파일을 내려받는다.

완료 후 프로젝트 디렉터리로 이동한다.

### Windows PowerShell

```powershell
cd C:\projects\AI-Data-Platform
```

### macOS

```bash
cd ~/projects/AI-Data-Platform
```

---

## 16. Clone 후 Repository 확인

프로젝트 디렉터리에서 Git 상태를 확인한다.

```bash
git status
```

정상적인 경우 현재 브랜치와 Working Tree 상태가 표시된다.

현재 브랜치도 확인한다.

```bash
git branch
```

예:

```text
* main
```

원격 Repository 연결 정보는 다음 명령으로 확인한다.

```bash
git remote -v
```

예:

```text
origin  https://github.com/Team-AI-Data-Platform/AI-Data-Platform.git (fetch)
origin  https://github.com/Team-AI-Data-Platform/AI-Data-Platform.git (push)
```

---

## 17. 프로젝트 디렉터리 구조 확인

Clone 후 프로젝트의 기본 구조를 확인한다.

프로젝트가 진행되면서 디렉터리 구조는 변경될 수 있지만 대표적인 구조는 다음과 같다.

```text
AI-Data-Platform/
│
├─ docs/
│  ├─ project_setup/
│  ├─ roadmap/
│  ├─ setting/
│  └─ study/
│
├─ labs/
│
├─ mkdocs.yml
├─ README.md
└─ .gitignore
```

주요 항목의 역할은 다음과 같다.

| 항목 | 역할 |
|---|---|
| `docs/` | MkDocs 문서 원본 |
| `docs/project_setup/` | 프로젝트 환경 구성 가이드 |
| `docs/study/` | AI 학습 가이드 |
| `labs/` | Python 및 AI 실습 코드 |
| `mkdocs.yml` | MkDocs 사이트 설정 및 메뉴 구성 |
| `README.md` | Repository 기본 안내 |
| `.gitignore` | Git 관리 제외 대상 정의 |

---

## 18. Clone과 Pull의 차이

신규 팀원이 자주 혼동하는 개념이 `Clone`과 `Pull`이다.

### Clone

Repository를 처음 로컬 PC로 내려받을 때 사용한다.

```bash
git clone <repository-url>
```

보통 **최초 1회** 실행한다.

### Pull

이미 Clone되어 있는 프로젝트에서 GitHub의 최신 변경 내용을 내려받을 때 사용한다.

```bash
git pull
```

또는 브랜치를 명시할 수 있다.

```bash
git pull origin main
```

정리하면 다음과 같다.

```text
처음 프로젝트를 받을 때
→ git clone

이미 프로젝트가 있는 상태에서 최신화할 때
→ git pull
```

---

## 19. 최신 소스 내려받기

프로젝트를 이미 Clone한 뒤 다른 팀원이 문서나 소스를 변경했다면 작업을 시작하기 전에 최신 내용을 내려받는 습관이 좋다.

프로젝트 루트에서 실행한다.

```bash
git pull origin main
```

변경 사항이 없다면 다음과 비슷하게 표시될 수 있다.

```text
Already up to date.
```

새로운 변경 사항이 있다면 해당 파일들이 로컬로 내려온다.

> 로컬에서 이미 수정한 파일이 있는 상태에서 Pull하면 충돌(Conflict)이 발생할 수 있다.  
> Git 사용이 익숙하지 않은 경우 임의로 파일을 삭제하거나 덮어쓰기보다 프로젝트 담당자와 확인한 뒤 처리한다.

---

## 20. GitHub HTTPS 인증 참고

Private Repository를 HTTPS 방식으로 Clone하거나 Push하는 경우 GitHub 인증이 필요할 수 있다.

Windows에서는 Git for Windows에 포함된 Git Credential Manager 등을 통해 브라우저 기반 인증이 진행될 수 있다.

인증 화면이 나타난다면 프로젝트 권한을 부여받은 **올바른 GitHub 계정**으로 로그인한다.

현재 Repository 주소는 다음 명령으로 확인할 수 있다.

```bash
git remote -v
```

GitHub 계정 인증과 Repository 접근 권한은 서로 다른 개념이다.

```text
GitHub 로그인 성공
        +
Repository 접근 권한 존재
        ↓
Private Repository 사용 가능
```

---

## 21. 자주 발생하는 문제

### 21.1 초대 메일이 오지 않는 경우

확인 사항:

```text
GitHub ID가 정확한가?
GitHub 가입 이메일이 정확한가?
스팸 메일함에 들어가 있지 않은가?
관리자가 실제 초대를 발송했는가?
```

필요하면 관리자에게 초대 상태를 확인한다.

---

### 21.2 Repository가 보이지 않는 경우

다음 사항을 확인한다.

```text
현재 로그인한 GitHub 계정
초대 수락 여부
Repository 권한
Repository URL
```

Private Repository는 권한이 없는 계정으로 접근하면 정상적으로 표시되지 않을 수 있다.

---

### 21.3 `Repository not found`

가능한 원인:

```text
Repository URL 오류
GitHub 로그인 계정 오류
Repository 접근 권한 없음
초대 미수락
```

먼저 브라우저에서 해당 GitHub 계정으로 Repository가 정상적으로 열리는지 확인한다.

---

### 21.4 `Authentication failed`

Git 인증 정보 또는 로그인 계정에 문제가 있을 수 있다.

확인한다.

```bash
git remote -v
```

Windows에서 Git Credential Manager를 사용하는 경우 현재 GitHub 인증 계정을 확인하거나 다시 로그인해야 할 수 있다.

---

### 21.5 `git` 명령을 찾을 수 없음

예:

```text
git: command not found
```

또는 Windows에서:

```text
'git'은(는) 내부 또는 외부 명령...
```

Git이 설치되지 않았거나 PATH에 정상적으로 등록되지 않은 상태일 수 있다.

운영체제별 Git 설치 가이드를 진행한 후 다시 확인한다.

```bash
git --version
```

---

### 21.6 Clone할 폴더가 이미 존재하는 경우

예:

```text
fatal: destination path 'AI-Data-Platform' already exists
```

이미 해당 디렉터리가 존재한다는 의미이다.

기존 프로젝트가 이미 Clone되어 있는 경우 다시 Clone하지 않고 프로젝트 디렉터리로 이동하여 Pull한다.

```bash
cd AI-Data-Platform
git pull origin main
```

기존 디렉터리가 Git 프로젝트인지 확실하지 않다면 임의로 삭제하지 말고 내용을 먼저 확인한다.

---

## 22. SourceTree를 사용하는 경우

Git 명령어가 익숙하지 않은 사용자는 SourceTree와 같은 GUI 도구를 사용할 수도 있다.

SourceTree를 통한 Clone의 기본 흐름은 다음과 같다.

```text
SourceTree 실행
      ↓
Clone 선택
      ↓
Repository URL 입력
      ↓
로컬 저장 위치 지정
      ↓
Clone 실행
```

다만 SourceTree 설치 및 상세 사용 방법은 본 문서에서 다루지 않는다.

별도의 `개발 유틸리티 > SourceTree 설치 및 사용` 가이드에서 관리하는 것을 권장한다.

---

## 23. 소스를 받은 뒤 다음 단계

Repository Clone이 완료되었다면 프로젝트 참여 및 소스 받기 단계는 완료된 것이다.

이후 자신의 운영체제에 맞게 로컬 개발환경을 구성한다.

### Windows 사용자

```text
프로젝트 환경 구성
 └─ 로컬 환경(Windows) 세팅하기
      ├─ Git 설치 및 기본 설정
      ├─ Python 설치 및 환경 설정
      ├─ MkDocs 설치 가이드
      └─ Ollama 설치 및 기본 설정
```

### macOS 사용자

```text
프로젝트 환경 구성
 └─ 로컬 환경(macOS) 세팅하기
      ├─ Git 설치 및 GitHub 설정
      ├─ Python 설치 및 환경 설정
      ├─ MkDocs 설치 가이드
      └─ Ollama 설치 및 기본 설정
```

이미 Git 설치를 먼저 진행했다면 Git 항목은 확인만 하고 다음 단계로 진행하면 된다.

---

## 24. 완료 체크리스트

다음 항목이 모두 확인되면 프로젝트 참여 및 소스 받기가 완료된 것이다.

- [ ] GitHub 계정 준비 완료
- [ ] 프로젝트 참여 요청 완료
- [ ] 관리자 GitHub Repository 초대 완료
- [ ] GitHub 초대 수락 완료
- [ ] 브라우저에서 Repository 접근 확인
- [ ] Git 설치 확인
- [ ] AI-Data-Platform Repository Clone 완료
- [ ] 프로젝트 디렉터리 이동 완료
- [ ] `git status` 정상 실행
- [ ] `git remote -v` 원격 저장소 확인
- [ ] `git pull origin main` 사용 방법 확인

---

## 25. 최종 정리

프로젝트 신규 참여자가 기억해야 할 핵심 흐름은 다음과 같다.

```text
GitHub 계정 준비
       ↓
프로젝트 참여 요청
       ↓
관리자 초대
       ↓
초대 수락
       ↓
Repository 접근 확인
       ↓
Git 설치 확인
       ↓
git clone
       ↓
프로젝트 확인
       ↓
git pull
       ↓
운영체제별 로컬 환경 구성
```

핵심 Git 명령어는 다음과 같다.

```bash
git --version
```

```bash
git clone https://github.com/Team-AI-Data-Platform/AI-Data-Platform.git
```

```bash
git status
```

```bash
git remote -v
```

```bash
git pull origin main
```

본 가이드는 **프로젝트 참여와 소스 확보까지**를 담당한다.

Python 가상환경, MkDocs, Ollama, RAG 및 AI Agent 실습은 각각의 전용 가이드에서 이어서 진행한다.
