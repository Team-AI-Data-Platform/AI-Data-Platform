# Git 설치 및 기본 설정 가이드 - Windows

> AI-Data-Platform 프로젝트를 Windows PC에서 사용하기 위해 Git을 설치하고, 기본 사용자 정보를 설정한 뒤 정상적으로 사용할 수 있는 상태까지 준비하는 가이드

---

## 1. 문서 작성 목적

이 문서는 **Windows PC에서 AI-Data-Platform 프로젝트를 처음 시작하는 사용자**를 대상으로 Git 설치와 기본 설정 방법을 설명한다.

AI-Data-Platform 프로젝트의 소스 코드, MkDocs 문서, Python 실습 파일 등은 GitHub Repository를 기준으로 관리한다.  
따라서 프로젝트 소스를 내려받고 이후 변경사항을 Pull, Commit, Push하려면 먼저 로컬 PC에서 Git을 사용할 수 있어야 한다.

이 문서에서는 다음 범위만 다룬다.

```text
Git 이해
   ↓
Windows에 Git 설치
   ↓
Git 설치 확인
   ↓
Git 사용자 정보 설정
   ↓
Git 기본 설정 확인
   ↓
Git 사용 준비 완료
```

> **중요**
>
> GitHub 프로젝트 참여 요청, Repository 초대 수락, 접근 권한 확인, Repository Clone 등은  
> 별도의 **「프로젝트 참여 및 소스 받기」** 가이드에서 설명한다.
>
> 이 문서의 목적은 그 전에 필요한 **로컬 Git 환경을 준비하는 것**이다.

---

## 2. Git과 GitHub의 차이

Git을 처음 사용할 때 가장 먼저 구분해야 하는 것이 **Git과 GitHub는 서로 다른 것**이라는 점이다.

### 2.1 Git

Git은 소스 코드와 문서의 변경 이력을 관리하는 **분산 버전 관리 시스템(Version Control System)** 이다.

예를 들어 다음과 같은 작업을 수행한다.

```text
파일 변경사항 확인
Commit 생성
변경 이력 조회
Branch 관리
원격 Repository와 변경사항 동기화
```

Git은 개발자의 **로컬 PC에 설치하는 프로그램**이다.

---

### 2.2 GitHub

GitHub는 Git Repository를 인터넷을 통해 저장하고 여러 사람이 함께 사용할 수 있도록 제공하는 **원격 Repository 서비스**이다.

AI-Data-Platform 프로젝트에서는 GitHub를 통해 다음 자산을 공유한다.

```text
MkDocs 문서
Python 실습 코드
AI / RAG / Agent 학습 자료
프로젝트 설정 파일
Git 변경 이력
```

GitHub 자체를 Windows에 설치하는 것은 아니다.

정리하면 다음과 같다.

| 구분 | Git | GitHub |
|---|---|---|
| 역할 | 버전 관리 도구 | Git Repository 공유 서비스 |
| 설치 여부 | 로컬 PC에 설치 | 웹 서비스이므로 설치하지 않음 |
| 주요 기능 | Commit, Branch, Merge, Pull, Push | Repository 공유, 권한 관리, 협업 |
| AI-Data-Platform에서의 역할 | 로컬 소스 관리 | 중앙 Repository 제공 |

따라서 이 문서의 정확한 목적은 **Git을 설치하고 GitHub Repository를 사용할 수 있는 로컬 환경을 준비하는 것**이다.

---

## 3. Windows Git 환경 구성 전체 흐름

Windows에서 Git 환경을 처음 구성하는 순서는 다음과 같다.

```text
1. 기존 Git 설치 여부 확인
        ↓
2. Git for Windows 설치
        ↓
3. PowerShell 또는 Terminal 다시 실행
        ↓
4. git --version 확인
        ↓
5. Git 사용자 이름 설정
        ↓
6. Git 사용자 이메일 설정
        ↓
7. Git 설정값 확인
        ↓
8. Git 기본 환경 구성 완료
```

Git 설치가 완료되면 이후 별도의 가이드에서 GitHub 프로젝트 참여 및 Repository Clone을 진행한다.

---

## 4. Git이 이미 설치되어 있는지 먼저 확인

새로 설치하기 전에 Git이 이미 설치되어 있는지 확인한다.

Windows PowerShell 또는 Windows Terminal을 실행한다.

다음 명령을 입력한다.

```powershell
git --version
```

Git이 설치되어 있다면 다음과 비슷한 결과가 출력된다.

```text
git version 2.x.x.windows.x
```

예를 들어 다음처럼 표시될 수 있다.

```text
git version 2.55.0.windows.1
```

버전 번호는 설치 시점에 따라 달라질 수 있으므로 예시와 정확히 같을 필요는 없다.

### Git이 설치되어 있는 경우

정상적으로 버전이 출력되면 Git을 다시 설치할 필요가 없다.

다음 단계인 **Git 사용자 정보 설정**으로 이동하면 된다.

### Git이 설치되어 있지 않은 경우

다음과 같은 메시지가 나오면 Git이 설치되어 있지 않거나 PATH가 정상적으로 설정되지 않은 상태일 수 있다.

```text
'git'은(는) 내부 또는 외부 명령, 실행할 수 있는 프로그램,
또는 배치 파일이 아닙니다.
```

PowerShell에서는 다음과 비슷하게 표시될 수도 있다.

```text
git : 'git'이라는 용어가 cmdlet, 함수, 스크립트 파일 또는
실행할 수 있는 프로그램 이름으로 인식되지 않습니다.
```

이 경우 Git을 설치한다.

---

## 5. Git for Windows 설치

Windows에서는 **Git for Windows**를 사용하는 것이 가장 일반적이다.

Git 공식 사이트의 Windows 설치 페이지에서 설치 프로그램을 내려받아 설치한다.

현재 공식 Git 사이트는 x64 및 ARM64용 Git for Windows 설치 파일을 제공하며, `winget`을 이용한 설치 방법도 제공한다.

### 5.1 방법 1 - 공식 설치 프로그램 사용

처음 설치하는 사용자는 **Git 공식 Windows Installer를 사용하는 방법을 권장**한다.

전체 흐름은 다음과 같다.

```text
Git 공식 사이트 접속
      ↓
Windows용 Git 다운로드
      ↓
설치 프로그램 실행
      ↓
설치 옵션 확인
      ↓
설치 완료
      ↓
PowerShell 재실행
```

설치 프로그램에는 여러 옵션이 표시된다.

Git을 처음 사용하는 경우 특별한 이유가 없다면 **대부분 기본값을 유지하여 설치해도 된다.**

다만 다음 항목의 의미는 알아두는 것이 좋다.

---

### 5.2 Git 사용 경로(PATH) 관련 옵션

Git 설치 중 명령 프롬프트, PowerShell 및 다른 프로그램에서 Git을 사용할 수 있도록 하는 PATH 관련 선택 화면이 나타날 수 있다.

일반적인 개발 환경에서는 다음 형태의 옵션이 적합하다.

```text
Git from the command line and also from 3rd-party software
```

이 설정을 사용하면 PowerShell, Windows Terminal, IDE 등의 프로그램에서 `git` 명령을 사용할 수 있다.

설치 프로그램 버전에 따라 화면 문구는 달라질 수 있다.

---

### 5.3 기본 편집기 선택

Git은 Commit 메시지 작성 등의 작업에서 텍스트 편집기를 사용할 수 있다.

설치 과정에서 기본 편집기를 선택하는 화면이 나타날 수 있다.

다음과 같은 편집기를 선택할 수 있다.

```text
Vim
Visual Studio Code
Notepad++
기타 설치된 Editor
```

Git 초보자라면 평소 사용하는 편집기가 있다면 해당 편집기를 선택하는 것이 편하다.

특별한 편집기를 선택하지 않더라도 Git 사용에는 문제가 없다.

---

### 5.4 기타 설치 옵션

Git for Windows 설치 프로그램에는 다음과 같은 설정이 추가로 표시될 수 있다.

```text
HTTPS 관련 설정
Line Ending 처리 방식
Terminal Emulator
Git Credential Manager
파일 시스템 옵션
```

처음 프로젝트 환경을 구성하는 경우에는 특별한 프로젝트 정책이 없다면 **기본 설정을 유지하는 것을 권장**한다.

AI-Data-Platform 프로젝트에서 별도의 Git 정책이 정해지는 경우 해당 정책에 맞추어 변경한다.

---

## 6. winget으로 설치하는 방법

Windows Package Manager인 `winget`을 사용하는 경우 PowerShell에서 Git을 설치할 수도 있다.

```powershell
winget install --id Git.Git -e --source winget
```

명령의 의미는 다음과 같다.

```text
winget install
→ 프로그램 설치

--id Git.Git
→ Git 패키지를 지정

-e
→ 패키지 ID를 정확히 일치시켜 검색

--source winget
→ winget Repository에서 설치
```

명령줄 설치에 익숙하지 않다면 공식 설치 프로그램 방식을 사용해도 된다.

---

## 7. 설치 후 Terminal을 다시 실행해야 하는 이유

Git 설치가 끝난 뒤 기존에 열려 있던 PowerShell에서 바로 다음 명령을 실행하면 Git을 찾지 못하는 경우가 있다.

```powershell
git --version
```

Git 설치 프로그램이 Windows PATH를 변경했지만 **이미 실행 중인 PowerShell에는 변경된 PATH가 즉시 반영되지 않을 수 있기 때문**이다.

따라서 Git 설치 후에는 다음 순서를 권장한다.

```text
1. 현재 PowerShell 종료
2. PowerShell 또는 Windows Terminal 다시 실행
3. git --version 실행
```

---

## 8. Git 설치 확인

새 PowerShell을 실행하고 다음 명령을 입력한다.

```powershell
git --version
```

정상적인 경우 다음과 비슷한 결과가 출력된다.

```text
git version 2.x.x.windows.x
```

이 결과가 출력되면 Git 프로그램 설치와 PATH 설정이 정상적으로 완료된 것이다.

---

## 9. Git 사용자 정보 설정이 필요한 이유

Git을 설치했다고 바로 모든 설정이 끝나는 것은 아니다.

Git은 Commit을 생성할 때 다음 정보를 Commit 이력에 기록한다.

```text
누가 Commit을 작성했는가?
어떤 이메일을 사용하는가?
```

따라서 처음 Git을 설치한 후에는 일반적으로 사용자 이름과 이메일을 설정한다.

대표적인 설정은 다음 두 가지이다.

```text
user.name
user.email
```

---

## 10. Git 사용자 이름 설정

다음 명령으로 Git 사용자 이름을 설정한다.

```powershell
git config --global user.name "사용자 이름"
```

예:

```powershell
git config --global user.name "Hong Gil Dong"
```

### `--global`의 의미

`--global`은 현재 Windows 사용자 계정에서 사용하는 Git의 기본 설정으로 저장한다는 의미이다.

```text
--global 설정
→ 현재 PC 사용자 계정의 모든 Git Repository에서 기본으로 사용
```

프로젝트마다 다른 이름을 사용해야 하는 특별한 경우가 아니라면 기본적으로 `--global` 설정을 사용하면 된다.

---

## 11. Git 사용자 이메일 설정

다음 명령으로 이메일을 설정한다.

```powershell
git config --global user.email "이메일 주소"
```

예:

```powershell
git config --global user.email "hong@example.com"
```

GitHub에서 Commit 작성자를 정상적으로 연결하려면 일반적으로 **GitHub 계정에 등록된 이메일 주소를 사용하는 것이 편리**하다.

다만 조직 또는 프로젝트의 이메일 사용 정책이 별도로 있다면 해당 정책을 우선한다.

---

## 12. 사용자 설정값 확인

설정한 사용자 이름을 확인한다.

```powershell
git config --global user.name
```

예:

```text
Hong Gil Dong
```

이메일을 확인한다.

```powershell
git config --global user.email
```

예:

```text
hong@example.com
```

두 값이 정상적으로 출력되면 기본 사용자 설정이 완료된 것이다.

---

## 13. 전체 Git 설정 확인

현재 적용된 Git 설정을 전체적으로 확인하려면 다음 명령을 사용할 수 있다.

```powershell
git config --list
```

출력 결과에는 여러 설정값이 표시될 수 있다.

그중 다음 항목이 있는지 확인한다.

```text
user.name=Hong Gil Dong
user.email=hong@example.com
```

설치 환경에 따라 Git Credential Manager, Line Ending 등 다른 설정값들도 함께 표시될 수 있다.

---

## 14. 설정값이 어디에 저장되는가

`--global` 옵션으로 설정한 Git 정보는 사용자 단위 Git 설정 파일에 저장된다.

Windows에서는 일반적으로 사용자 홈 디렉터리의 `.gitconfig` 파일에 저장된다.

개념적으로 다음과 같다.

```text
Windows 사용자 계정
   │
   └─ .gitconfig
        ├─ user.name
        ├─ user.email
        └─ 기타 Git 설정
```

직접 파일을 수정하기보다는 `git config` 명령을 사용하여 설정하는 것을 권장한다.

---

## 15. Global 설정과 Local 설정의 차이

Git 설정에는 여러 범위가 있다.

초기 사용자에게 가장 중요한 것은 다음 두 가지이다.

### 15.1 Global 설정

현재 PC 사용자 계정에서 기본적으로 사용하는 설정이다.

```powershell
git config --global user.name "Hong Gil Dong"
```

AI-Data-Platform 외의 다른 Git Repository에도 기본적으로 적용된다.

---

### 15.2 Local 설정

특정 Git Repository에만 적용되는 설정이다.

프로젝트 Repository 안에서 다음처럼 설정한다.

```powershell
git config user.name "Hong Gil Dong"
```

`--global`이 없다는 점에 주의한다.

Local 설정은 Global 설정보다 우선 적용된다.

```text
Global
→ 사용자 기본 설정

Local
→ 현재 Repository 전용 설정
```

처음 프로젝트 환경을 구성할 때는 특별한 이유가 없다면 Global 설정만으로 충분하다.

---

## 16. 기본 브랜치 이름 설정 - 선택 사항

새로운 Git Repository를 직접 생성할 때 기본 브랜치 이름을 `main`으로 사용하고 싶다면 다음 설정을 사용할 수 있다.

```powershell
git config --global init.defaultBranch main
```

이 설정은 **새로 `git init`을 수행하는 Repository의 기본 브랜치 이름**에 영향을 준다.

이미 GitHub에서 Clone한 AI-Data-Platform Repository의 기존 브랜치 이름을 변경하는 설정은 아니다.

따라서 이 항목은 필수 설정은 아니다.

---

## 17. GitHub 인증에 대한 기본 이해

Git 설치와 GitHub 인증은 서로 다른 단계이다.

```text
Git 설치
→ 로컬 PC에서 Git 명령을 사용할 수 있게 함

GitHub 인증
→ 원격 GitHub Repository에 접근할 사용자인지 확인
```

GitHub Repository를 HTTPS 방식으로 Clone하거나 Push할 때 인증이 필요할 수 있다.

현재 GitHub는 Git 명령줄 작업에서 계정 비밀번호를 이용한 Git 인증을 지원하지 않으며, Git Credential Manager, Personal Access Token, SSH 등의 방식을 사용할 수 있다.

Windows용 Git을 설치하면 Git Credential Manager를 함께 사용할 수 있는 환경이 구성되는 경우가 일반적이다.

Git Credential Manager를 사용하면 GitHub 인증 과정에서 웹 브라우저를 통해 로그인하고 인증 정보를 Windows Credential Manager에 안전하게 저장하여 이후 HTTPS 연결에 사용할 수 있다.

> GitHub Repository 실제 인증과 Clone 과정은  
> **「프로젝트 참여 및 소스 받기」** 가이드에서 단계별로 설명한다.

---

## 18. HTTPS와 SSH 방식 이해

GitHub Repository에 연결하는 대표적인 방법은 HTTPS와 SSH이다.

### HTTPS

형태:

```text
https://github.com/조직명/저장소명.git
```

특징:

```text
처음 사용하기 쉬움
Git Credential Manager와 함께 사용 가능
브라우저 기반 인증을 사용할 수 있음
```

처음 프로젝트에 참여하는 팀원에게는 HTTPS 방식이 이해하기 쉽다.

---

### SSH

형태:

```text
git@github.com:조직명/저장소명.git
```

특징:

```text
SSH Key 생성 필요
GitHub 계정에 Public Key 등록 필요
한 번 구성하면 반복적인 인증 작업이 편리함
```

SSH는 Git 사용에 익숙해진 후 필요에 따라 구성해도 된다.

---

## 19. Git 설치 후 현재 단계에서 하지 않는 작업

이 문서에서는 다음 작업을 진행하지 않는다.

```text
GitHub Repository 참여 요청
GitHub 저장소 초대 수락
Repository 접근 권한 확인
AI-Data-Platform Repository Clone
git pull
git push
Branch 작업
SourceTree 설치
Python 설치
```

이 작업들을 한 문서에 모두 포함하면 환경 구성 문서가 너무 길어지고 필요한 내용을 찾기 어려워질 수 있다.

따라서 역할별로 문서를 분리한다.

```text
Git 설치 및 기본 설정
        ↓
프로젝트 참여 및 소스 받기
        ↓
SourceTree 등 개발 유틸리티
```

---

## 20. 자주 발생하는 문제

### 20.1 `git` 명령을 찾을 수 없음

증상:

```text
git 명령을 찾을 수 없습니다.
```

또는:

```text
'git' is not recognized ...
```

확인 순서:

```text
1. Git 설치가 완료되었는지 확인
2. PowerShell을 종료했다가 다시 실행
3. git --version 재실행
4. 계속 실패하면 Git을 다시 설치하면서 PATH 관련 옵션 확인
```

---

### 20.2 Git을 설치했는데 이전 PowerShell에서는 동작하지 않음

원인:

```text
기존 PowerShell 프로세스에 변경된 PATH가 반영되지 않음
```

해결:

```text
PowerShell 또는 Windows Terminal을 완전히 종료한 뒤 다시 실행
```

---

### 20.3 Commit 시 사용자 이름 또는 이메일 오류

다음과 비슷한 메시지가 표시될 수 있다.

```text
Author identity unknown
```

이 경우 사용자 정보를 설정한다.

```powershell
git config --global user.name "사용자 이름"
git config --global user.email "이메일 주소"
```

설정 후 확인한다.

```powershell
git config --global user.name
git config --global user.email
```

---

### 20.4 잘못된 사용자 정보를 설정함

기존 명령을 다시 실행하면 새로운 값으로 변경된다.

```powershell
git config --global user.name "새 사용자 이름"
git config --global user.email "새 이메일 주소"
```

이 설정은 이후 생성되는 Commit에 적용된다.

이미 생성된 과거 Commit의 작성자 정보가 자동으로 변경되는 것은 아니다.

---

### 20.5 GitHub 비밀번호를 입력했는데 인증되지 않음

GitHub의 Git 명령줄 인증에서는 일반 GitHub 계정 비밀번호를 사용하지 않는다.

HTTPS 연결에서는 Git Credential Manager 또는 Personal Access Token 등을 사용할 수 있고, SSH 연결에서는 SSH Key를 사용한다.

실제 프로젝트 연결 방법은 **「프로젝트 참여 및 소스 받기」** 가이드를 참고한다.

---

## 21. 설치 및 기본 설정 최종 확인

다음 항목을 순서대로 확인한다.

### 21.1 Git 버전

```powershell
git --version
```

정상:

```text
git version 2.x.x.windows.x
```

---

### 21.2 Git 사용자 이름

```powershell
git config --global user.name
```

자신이 설정한 사용자 이름이 출력되어야 한다.

---

### 21.3 Git 사용자 이메일

```powershell
git config --global user.email
```

자신이 설정한 이메일이 출력되어야 한다.

---

### 21.4 전체 설정

```powershell
git config --list
```

최소한 다음 값이 정상적으로 확인되어야 한다.

```text
user.name=...
user.email=...
```

---

## 22. 완료 체크리스트

Git 설치 및 기본 설정이 완료되었는지 다음 항목을 확인한다.

```text
[완료] Git for Windows 설치
[완료] git --version 정상 출력
[완료] Git 사용자 이름 설정
[완료] Git 사용자 이메일 설정
[완료] git config --list에서 설정값 확인
```

위 항목이 모두 정상이라면 Windows의 Git 기본 환경 구성이 완료된 것이다.

---

## 23. 다음 단계

Git 설치 및 기본 설정이 완료되면 다음 단계로 이동한다.

```text
Windows 로컬 환경 세팅

1. Git 설치 및 기본 설정
        ↓
2. Python 설치 및 환경 설정
        ↓
3. 프로젝트 참여 및 소스 받기
```

프로젝트가 Private Repository인 경우 Git이 설치되어 있더라도 GitHub Repository 접근 권한이 없으면 소스를 Clone할 수 없다.

따라서 이후 **「프로젝트 참여 및 소스 받기」** 가이드에서 다음 과정을 진행한다.

```text
GitHub 계정 확인
      ↓
프로젝트 참여 요청
      ↓
관리자 초대
      ↓
초대 수락
      ↓
Repository 접근 확인
      ↓
AI-Data-Platform Clone
      ↓
최신 소스 확인
```

---

## 24. 핵심 정리

Windows에서 AI-Data-Platform 프로젝트를 시작하기 위한 Git 환경 구성의 핵심은 다음과 같다.

```text
1. Git은 로컬 PC에 설치하는 버전 관리 도구이다.
2. GitHub는 Git Repository를 공유하는 원격 서비스이다.
3. 먼저 Git for Windows를 설치한다.
4. git --version으로 설치 상태를 확인한다.
5. user.name과 user.email을 기본 설정한다.
6. GitHub 프로젝트 참여와 Repository Clone은 별도 단계에서 진행한다.
```

이 문서까지 완료하면 **Windows PC에서 Git 명령을 사용할 수 있는 기본 환경이 준비된 상태**이다.

다음으로 Python 개발 환경을 구성하거나, 프로젝트 참여 권한이 이미 준비되어 있다면 「프로젝트 참여 및 소스 받기」 가이드를 진행한다.
