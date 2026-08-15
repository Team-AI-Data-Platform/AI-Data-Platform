# Git 설치 및 GitHub 설정 가이드 - macOS

> AI-Data-Platform 프로젝트를 macOS 환경에서 사용하기 위해 Git을 설치하거나 확인하고, Git 사용자 정보와 GitHub 연결에 필요한 기본 설정을 준비하는 가이드

---

## 1. 문서 작성 목적

이 문서는 **macOS에서 AI-Data-Platform 프로젝트를 처음 시작하는 사용자**를 대상으로 Git 설치와 기본 설정, GitHub 사용을 위한 기초 환경 구성 방법을 설명한다.

AI-Data-Platform 프로젝트의 소스 코드, MkDocs 문서, Python 실습 파일 등은 GitHub Repository를 기준으로 관리한다.

따라서 프로젝트 소스를 내려받고 이후 Pull, Commit, Push 등의 작업을 수행하려면 먼저 로컬 Mac에서 Git을 정상적으로 사용할 수 있어야 한다.

이 문서에서는 다음 범위를 다룬다.

```text
Git 설치 여부 확인
      ↓
필요 시 Git 설치
      ↓
Git 버전 확인
      ↓
Git 사용자 이름 설정
      ↓
Git 사용자 이메일 설정
      ↓
GitHub 인증 방식 이해
      ↓
기본 환경 구성 완료
```

> **중요**
>
> GitHub 프로젝트 참여 요청, Repository 초대 수락, 접근 권한 확인, AI-Data-Platform Repository Clone 등은
> 별도의 **「프로젝트 참여 및 소스 받기」** 가이드에서 설명한다.
>
> 이 문서의 목적은 그 전에 필요한 **macOS의 로컬 Git 환경과 GitHub 사용을 위한 기본 설정을 준비하는 것**이다.

---

## 2. Git과 GitHub의 차이

Git을 처음 사용할 때는 **Git과 GitHub가 서로 다른 역할을 한다는 점**을 먼저 이해하는 것이 좋다.

### 2.1 Git

Git은 파일의 변경 이력을 관리하는 **분산 버전 관리 시스템(Version Control System)** 이다.

대표적으로 다음과 같은 작업에 사용한다.

```text
파일 변경사항 확인
Commit 생성
변경 이력 조회
Branch 관리
원격 Repository와 동기화
```

Git은 개발자의 **로컬 Mac에 설치하여 사용하는 프로그램**이다.

---

### 2.2 GitHub

GitHub는 Git Repository를 원격에서 저장하고 여러 사람이 함께 사용할 수 있도록 제공하는 **Repository 호스팅 및 협업 서비스**이다.

AI-Data-Platform 프로젝트에서는 GitHub를 통해 다음과 같은 자산을 관리한다.

```text
MkDocs 문서
Python 실습 코드
AI / RAG / Agent 학습 자료
프로젝트 설정 파일
Git 변경 이력
```

GitHub 자체를 macOS에 설치하는 것은 아니다.

다만 GitHub를 원격 Repository로 사용하기 위해서는 다음과 같은 준비가 필요할 수 있다.

```text
GitHub 계정
Repository 접근 권한
HTTPS 또는 SSH 인증
```

정리하면 다음과 같다.

| 구분 | Git | GitHub |
|---|---|---|
| 역할 | 버전 관리 도구 | Git Repository 공유 및 협업 서비스 |
| 설치 여부 | Mac에 설치 | 웹 서비스이므로 설치하지 않음 |
| 주요 기능 | Commit, Branch, Merge, Pull, Push | Repository 공유, 권한 관리, 협업 |
| 프로젝트에서의 역할 | 로컬 소스 관리 | 중앙 Repository 제공 |

---

## 3. macOS Git 환경 구성 전체 흐름

macOS에서 Git 환경을 구성하는 권장 순서는 다음과 같다.

```text
1. Git 설치 여부 확인
        ↓
2. 설치되어 있지 않으면 Git 설치
        ↓
3. git --version 확인
        ↓
4. Git 사용자 이름 설정
        ↓
5. Git 사용자 이메일 설정
        ↓
6. Git 설정값 확인
        ↓
7. GitHub 인증 방식 이해
        ↓
8. Git 기본 환경 구성 완료
```

Git 환경이 준비되면 이후 별도의 가이드에서 GitHub 프로젝트 참여 및 Repository Clone을 진행한다.

---

## 4. Git이 이미 설치되어 있는지 먼저 확인

macOS에는 개발 도구 설치 상태에 따라 Git이 이미 사용할 수 있는 경우가 있다.

따라서 바로 설치하기보다 먼저 Terminal에서 다음 명령을 실행한다.

```bash
git --version
```

정상적으로 설치되어 있다면 다음과 비슷한 결과가 출력된다.

```text
git version 2.x.x
```

또는 Apple이 제공하는 Git이 설치된 환경에서는 다음처럼 표시될 수도 있다.

```text
git version 2.x.x (Apple Git-xxx)
```

버전 번호는 macOS 버전과 설치 방식에 따라 다를 수 있으므로 예시와 정확히 같을 필요는 없다.

### Git이 정상적으로 확인되는 경우

Git 버전이 출력되면 기본적으로 Git을 사용할 수 있는 상태이다.

이 경우 반드시 다시 설치할 필요는 없다.

다음 단계인 **Git 사용자 정보 설정**으로 이동할 수 있다.

### Git이 설치되어 있지 않은 경우

Git이 없거나 Xcode Command Line Tools가 설치되어 있지 않은 환경에서는 `git` 명령 실행 시 개발 도구 설치 안내가 표시될 수 있다.

이 경우 다음 절의 설치 방법 중 하나를 선택한다.

---

## 5. macOS에서 Git을 설치하는 방법

macOS에서 Git을 설치하는 대표적인 방법은 다음과 같다.

```text
방법 1. Xcode Command Line Tools 사용
방법 2. Homebrew 사용
방법 3. Git 공식 macOS 설치 방법 확인
```

처음 환경을 구성하는 경우에는 **Xcode Command Line Tools를 통한 설치 또는 이미 Homebrew를 사용 중이라면 Homebrew 설치**가 이해하기 쉽다.

---

## 6. 방법 1 - Xcode Command Line Tools로 Git 설치

Git 공식 문서에서는 macOS에서 Git을 설치하는 가장 쉬운 방법 중 하나로 **Xcode Command Line Tools**를 안내한다.

Terminal에서 다음 명령을 실행한다.

```bash
xcode-select --install
```

설치 안내 창이 표시되면 화면의 절차에 따라 Command Line Tools를 설치한다.

설치가 완료되면 Terminal을 새로 열고 다음 명령으로 확인한다.

```bash
git --version
```

정상적으로 버전이 출력되면 Git을 사용할 수 있다.

### Xcode 전체 설치가 필요한가?

Git만 사용하기 위해 Xcode 전체 IDE를 반드시 설치할 필요는 없다.

`xcode-select --install`을 통해 필요한 Command Line Tools만 설치할 수 있다.

Command Line Tools에는 Git을 포함한 여러 개발 명령줄 도구가 포함된다.

---

## 7. 방법 2 - Homebrew로 Git 설치

이미 Homebrew를 사용하는 개발 환경이라면 Homebrew를 이용해 Git을 설치할 수 있다.

먼저 Homebrew가 설치되어 있는지 확인한다.

```bash
brew --version
```

정상적으로 버전이 출력된다면 다음 명령으로 Git을 설치한다.

```bash
brew install git
```

설치가 완료되면 다음 명령으로 확인한다.

```bash
git --version
```

Homebrew 공식 Formula에서도 Git 설치 명령으로 다음 명령을 제공한다.

```bash
brew install git
```

### Homebrew가 설치되어 있지 않은 경우

Git 하나를 설치하기 위해 반드시 Homebrew부터 설치해야 하는 것은 아니다.

Homebrew를 앞으로 Python이나 기타 개발 도구의 패키지 관리에 활용할 계획이라면 설치를 고려할 수 있지만, Git만 필요한 경우에는 Xcode Command Line Tools 방식으로도 충분하다.

> Homebrew 자체 설치 및 관리 방법은 필요 시 별도의 개발 유틸리티 또는 macOS 환경 구성 가이드에서 다루는 것이 좋다.

---

## 8. 어떤 Git을 사용하고 있는지 확인

Git이 설치된 후 어떤 실행 파일을 사용하고 있는지 확인하려면 다음 명령을 사용할 수 있다.

```bash
which git
```

예를 들어 시스템 Git을 사용하는 경우 다음과 비슷하게 표시될 수 있다.

```text
/usr/bin/git
```

Homebrew를 통해 설치한 Git은 Mac의 CPU와 Homebrew 설치 경로에 따라 다른 위치가 출력될 수 있다.

예를 들어 Apple Silicon Mac에서는 다음과 비슷한 경로가 사용될 수 있다.

```text
/opt/homebrew/bin/git
```

Intel Mac에서는 다음과 비슷한 경로가 사용될 수 있다.

```text
/usr/local/bin/git
```

실제 경로는 설치 환경에 따라 다를 수 있으므로 `which git` 결과를 기준으로 확인한다.

---

## 9. Git 설치 후 Terminal을 다시 실행하는 이유

Git 또는 Homebrew 설치 후 기존 Terminal에서 명령이 바로 인식되지 않는 경우가 있다.

설치 과정에서 PATH 또는 Shell 환경이 변경되었지만 이미 실행 중인 Terminal 세션에는 변경사항이 반영되지 않았을 수 있기 때문이다.

이 경우 다음 순서로 확인한다.

```text
1. 현재 Terminal 종료
2. Terminal 다시 실행
3. git --version 실행
4. which git 실행
```

---

## 10. Git 사용자 정보 설정이 필요한 이유

Git은 Commit을 생성할 때 Commit 작성자의 정보를 함께 기록한다.

대표적으로 다음 정보가 사용된다.

```text
user.name
user.email
```

따라서 Git 설치 후에는 사용자 이름과 이메일을 설정하는 것이 좋다.

---

## 11. Git 사용자 이름 설정

Terminal에서 다음 명령을 실행한다.

```bash
git config --global user.name "사용자 이름"
```

예:

```bash
git config --global user.name "Hong Gil Dong"
```

### `--global`의 의미

`--global` 옵션은 **현재 macOS 사용자 계정에서 사용하는 기본 Git 설정**으로 저장한다는 의미이다.

```text
--global 설정
→ 현재 사용자 계정의 Git Repository에서 기본값으로 사용
```

특정 프로젝트마다 다른 사용자 정보를 사용해야 하는 특별한 이유가 없다면 기본적으로 Global 설정을 사용하면 된다.

---

## 12. Git 사용자 이메일 설정

다음 명령으로 Commit 이메일 주소를 설정한다.

```bash
git config --global user.email "이메일 주소"
```

예:

```bash
git config --global user.email "hong@example.com"
```

GitHub는 Commit에 기록된 이메일을 기준으로 GitHub 계정과 Commit을 연결할 수 있다.

일반적으로 GitHub 계정에 등록되어 있는 이메일을 사용하면 관리하기 편하다.

GitHub에서 실제 이메일 주소를 Commit에 노출하고 싶지 않은 경우 GitHub에서 제공하는 `noreply` 이메일 주소를 사용하는 방법도 있다.

프로젝트나 회사에서 이메일 정책을 별도로 정하고 있다면 해당 정책을 우선한다.

---

## 13. 사용자 설정값 확인

설정한 이름을 확인한다.

```bash
git config --global user.name
```

예:

```text
Hong Gil Dong
```

이메일을 확인한다.

```bash
git config --global user.email
```

예:

```text
hong@example.com
```

두 값이 정상적으로 출력되면 기본 사용자 설정이 완료된 것이다.

---

## 14. 전체 Git 설정 확인

현재 Git 설정을 전체적으로 확인하려면 다음 명령을 사용할 수 있다.

```bash
git config --list
```

출력 결과에는 여러 설정값이 표시될 수 있다.

최소한 다음 값이 포함되어 있는지 확인한다.

```text
user.name=Hong Gil Dong
user.email=hong@example.com
```

---

## 15. 설정값은 어디에 저장되는가

`--global`로 설정한 값은 사용자 단위 Git 설정 파일에 저장된다.

macOS에서는 일반적으로 사용자 홈 디렉터리의 다음 파일에 저장된다.

```text
~/.gitconfig
```

개념적으로 보면 다음과 같다.

```text
macOS 사용자 홈
   │
   └─ .gitconfig
       ├─ user.name
       ├─ user.email
       └─ 기타 Git 설정
```

일반적인 설정 변경은 `.gitconfig`를 직접 수정하기보다 `git config` 명령을 사용하는 것이 안전하다.

---

## 16. Global 설정과 Local 설정의 차이

Git 설정에는 적용 범위가 존재한다.

초기 사용자에게 가장 중요한 것은 Global 설정과 Local 설정이다.

### 16.1 Global 설정

현재 macOS 사용자 계정의 기본 설정이다.

```bash
git config --global user.name "Hong Gil Dong"
```

AI-Data-Platform뿐 아니라 다른 Git Repository에서도 기본값으로 사용할 수 있다.

### 16.2 Local 설정

특정 Repository에만 적용되는 설정이다.

Git Repository 내부에서 다음과 같이 설정한다.

```bash
git config user.name "Hong Gil Dong"
```

`--global` 옵션이 없다는 점에 주의한다.

개념적으로 다음과 같다.

```text
Global
→ 사용자 기본 설정

Local
→ 현재 Repository 전용 설정
```

Local 설정이 존재하면 해당 Repository에서는 Local 값이 우선 적용된다.

처음 환경을 구성하는 경우 특별한 이유가 없다면 Global 설정만으로 충분하다.

---

## 17. 기본 브랜치 이름 설정 - 선택 사항

새 Git Repository를 직접 만들 때 기본 브랜치 이름을 `main`으로 사용하고 싶다면 다음 설정을 사용할 수 있다.

```bash
git config --global init.defaultBranch main
```

이 설정은 이후 새로 실행하는 `git init` Repository의 기본 브랜치 이름에 적용된다.

이미 GitHub에서 Clone한 AI-Data-Platform Repository의 브랜치 이름을 변경하는 명령은 아니다.

따라서 필수 설정은 아니다.

---

## 18. GitHub 사용을 위한 인증 이해

Git 설치와 GitHub 인증은 서로 다른 개념이다.

```text
Git 설치
→ 로컬 Mac에서 Git 명령을 사용할 수 있도록 준비

GitHub 인증
→ GitHub가 현재 사용자를 확인하여 Repository 접근을 허용
```

GitHub Repository에 접근할 때는 Repository 공개 여부와 수행하는 작업에 따라 인증이 필요하다.

특히 Private Repository 또는 Push 작업에서는 사용자의 GitHub 계정과 권한을 확인하는 과정이 필요하다.

---

## 19. GitHub 인증 방식

GitHub Repository를 Git 명령으로 사용할 때 대표적으로 다음 방식이 있다.

```text
HTTPS
SSH
GitHub CLI 기반 인증
```

초기 환경 구성에서는 모든 방식을 한 번에 설정할 필요가 없다.

AI-Data-Platform 프로젝트에서는 실제 Repository에 참여하고 소스를 받는 단계에서 사용할 방식을 선택하면 된다.

---

## 20. HTTPS 방식

GitHub Repository의 HTTPS 주소는 일반적으로 다음 형태이다.

```text
https://github.com/조직명/저장소명.git
```

HTTPS는 처음 사용하는 사용자에게 비교적 이해하기 쉬운 방식이다.

GitHub는 Git 명령줄 인증에서 GitHub 계정 비밀번호를 직접 사용하는 방식을 지원하지 않는다.

따라서 인증이 필요한 HTTPS 작업에서는 Personal Access Token, Git Credential Manager, GitHub CLI 등의 지원 방식이 사용될 수 있다.

> 실제 AI-Data-Platform Repository URL과 인증 절차는  
> **「프로젝트 참여 및 소스 받기」** 가이드에서 설명한다.

---

## 21. macOS Keychain과 GitHub 인증

macOS에서는 Git 자격 증명을 Keychain에 저장하여 사용할 수 있는 `osxkeychain` Credential Helper가 사용될 수 있다.

현재 Credential Helper 설정을 확인하려면 다음 명령을 사용할 수 있다.

```bash
git config --global credential.helper
```

환경에 따라 다음과 같은 값이 출력될 수 있다.

```text
osxkeychain
```

설정이 없다고 해서 Git 자체가 잘못 설치된 것은 아니다.

실제 GitHub 인증 방식에 따라 Credential Helper 구성이 달라질 수 있으므로, 프로젝트 Clone 또는 Push 단계에서 필요한 방식으로 구성한다.

---

## 22. SSH 방식

SSH를 사용하는 경우 Repository 주소는 일반적으로 다음 형태이다.

```text
git@github.com:조직명/저장소명.git
```

SSH 방식은 다음과 같은 준비가 필요하다.

```text
SSH Key 확인
      ↓
필요 시 SSH Key 생성
      ↓
ssh-agent 등록
      ↓
GitHub 계정에 Public Key 등록
      ↓
GitHub 연결 테스트
```

한 번 구성해두면 반복적인 인증 작업이 편리하다는 장점이 있다.

다만 프로젝트에 처음 참여하는 사용자는 HTTPS 방식으로 시작하고 필요 시 SSH를 추가로 구성해도 된다.

---

## 23. GitHub CLI - 선택 사항

GitHub는 `gh`라는 공식 CLI 도구도 제공한다.

GitHub CLI를 사용하면 Terminal에서 GitHub 인증, Repository 관련 작업 등을 수행할 수 있다.

하지만 **Git 자체를 사용하기 위해 GitHub CLI가 필수인 것은 아니다.**

따라서 프로젝트 초기 환경 구성에서는 다음과 같이 구분한다.

```text
Git
→ 필수

GitHub 계정 및 Repository 권한
→ 프로젝트 참여 시 필요

GitHub CLI
→ 선택 사항
```

필요한 경우 개발 유틸리티 또는 GitHub 활용 가이드에서 별도로 다룰 수 있다.

---

## 24. Git 설치 및 GitHub 기본 설정 후 하지 않는 작업

이 문서에서는 다음 작업까지 진행하지 않는다.

```text
AI-Data-Platform 프로젝트 참여 요청
관리자의 GitHub Repository 초대
팀원의 초대 수락
Repository 접근 권한 확인
AI-Data-Platform Repository Clone
git pull
git push
Branch 생성 및 Merge
SourceTree 설치
Python 설치
```

이 작업을 한 문서에 모두 넣으면 환경 구성 가이드가 다시 복잡해질 수 있다.

따라서 다음과 같이 역할을 분리한다.

```text
Git 설치 및 GitHub 설정
        ↓
Python 설치 및 환경 설정
        ↓
프로젝트 참여 및 소스 받기
        ↓
개발 유틸리티
```

---

## 25. 자주 발생하는 문제

### 25.1 `git` 명령 실행 시 개발 도구 설치 안내가 나타남

macOS에서 Git 또는 Command Line Tools가 준비되지 않은 경우 발생할 수 있다.

다음 명령으로 Command Line Tools 설치를 진행한다.

```bash
xcode-select --install
```

설치 완료 후 Terminal을 다시 열고 확인한다.

```bash
git --version
```

---

### 25.2 Git 설치 후 `git --version` 결과가 예상과 다름

macOS에는 Apple이 제공하는 Git과 Homebrew로 설치한 Git이 함께 존재할 수 있다.

다음 명령으로 실제 사용하는 Git 경로를 확인한다.

```bash
which git
```

그리고 버전을 확인한다.

```bash
git --version
```

특별한 이유가 없다면 현재 Git이 정상 동작하는지 먼저 확인하고, 단순히 버전 숫자가 다르다는 이유만으로 설치 환경을 변경할 필요는 없다.

---

### 25.3 Homebrew로 Git을 설치했는데 시스템 Git이 실행됨

다음 명령으로 어떤 Git이 먼저 인식되는지 확인한다.

```bash
which git
```

Homebrew 설치 경로가 Shell의 PATH에서 시스템 Git보다 뒤에 있을 경우 시스템 Git이 먼저 실행될 수 있다.

이 문제는 사용 중인 Shell과 Mac의 CPU 환경에 따라 PATH 설정이 달라질 수 있으므로 무조건 특정 경로를 추가하기보다 현재 Homebrew 환경 설정을 먼저 확인한다.

---

### 25.4 Commit 시 `Author identity unknown` 오류가 발생함

Git 사용자 정보가 설정되지 않은 경우 발생할 수 있다.

다음과 같이 설정한다.

```bash
git config --global user.name "사용자 이름"
git config --global user.email "이메일 주소"
```

설정 후 다시 확인한다.

```bash
git config --global user.name
git config --global user.email
```

---

### 25.5 Git 사용자 이름 또는 이메일을 잘못 설정함

기존 설정 명령을 다시 실행하면 변경할 수 있다.

```bash
git config --global user.name "새 사용자 이름"
git config --global user.email "새 이메일 주소"
```

이 변경은 이후 생성되는 Commit에 적용된다.

이미 만들어진 과거 Commit의 작성자 정보가 자동으로 변경되는 것은 아니다.

---

### 25.6 GitHub 계정 비밀번호로 인증이 되지 않음

GitHub의 Git 명령줄 인증에서는 일반 GitHub 계정 비밀번호를 직접 사용하지 않는다.

Repository 접근 방식에 따라 다음 인증 수단을 사용한다.

```text
HTTPS
→ Token / Credential Helper / GitHub CLI 등

SSH
→ SSH Key
```

실제 프로젝트 인증 방법은 **「프로젝트 참여 및 소스 받기」** 가이드에서 설명한다.

---

### 25.7 `Permission denied` 또는 `Repository not found` 발생

Git 설치 문제라기보다 GitHub Repository 권한 또는 인증 문제일 가능성이 높다.

다음 항목을 확인한다.

```text
GitHub 계정이 맞는가?
프로젝트 초대를 수락했는가?
Repository 접근 권한이 있는가?
사용한 Repository URL이 정확한가?
인증 방식이 정상적으로 설정되어 있는가?
```

이 문제 역시 프로젝트 참여 및 소스 받기 단계에서 상세하게 확인한다.

---

## 26. 설치 및 기본 설정 최종 확인

다음 항목을 순서대로 확인한다.

### 26.1 Git 버전 확인

```bash
git --version
```

Git 버전이 정상적으로 출력되어야 한다.

---

### 26.2 Git 실행 파일 위치 확인

```bash
which git
```

Git 실행 파일 경로가 출력되어야 한다.

---

### 26.3 Git 사용자 이름 확인

```bash
git config --global user.name
```

자신이 설정한 이름이 출력되어야 한다.

---

### 26.4 Git 사용자 이메일 확인

```bash
git config --global user.email
```

자신이 설정한 이메일이 출력되어야 한다.

---

### 26.5 Git 전체 설정 확인

```bash
git config --list
```

최소한 다음 항목이 정상적으로 확인되어야 한다.

```text
user.name=...
user.email=...
```

---

## 27. 완료 체크리스트

macOS의 Git 및 GitHub 기본 환경 구성이 완료되었는지 확인한다.

```text
[완료] git --version 정상 출력
[완료] which git으로 Git 실행 경로 확인
[완료] Git 사용자 이름 설정
[완료] Git 사용자 이메일 설정
[완료] git config --list 설정 확인
[확인] GitHub 계정 준비
[이해] HTTPS / SSH 인증 방식의 차이
```

위 항목이 모두 정상이라면 macOS에서 Git을 사용할 수 있는 기본 환경이 준비된 것이다.

---

## 28. 다음 단계

Git 설치 및 GitHub 기본 설정이 완료되면 다음 단계로 이동한다.

```text
macOS 로컬 환경 세팅

1. Git 설치 및 GitHub 설정
        ↓
2. Python 설치 및 환경 설정
        ↓
3. 프로젝트 참여 및 소스 받기
```

프로젝트가 Private Repository인 경우 Git이 정상적으로 설치되어 있더라도 Repository 접근 권한이 없으면 소스를 받을 수 없다.

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

## 29. 핵심 정리

macOS에서 AI-Data-Platform 프로젝트를 시작하기 위한 Git 환경 구성의 핵심은 다음과 같다.

```text
1. 먼저 git --version으로 기존 Git 설치 여부를 확인한다.
2. Git이 없다면 Xcode Command Line Tools 또는 Homebrew를 이용해 설치한다.
3. user.name과 user.email을 설정한다.
4. Git과 GitHub는 서로 다른 역할을 한다.
5. GitHub Repository 사용을 위해서는 계정, 권한, 인증이 필요할 수 있다.
6. HTTPS와 SSH는 대표적인 GitHub 연결 방식이다.
7. 프로젝트 참여 요청과 Repository Clone은 별도 가이드에서 진행한다.
```

이 문서까지 완료하면 **macOS에서 Git 명령을 사용하고 GitHub Repository에 연결하기 위한 기본 준비가 완료된 상태**이다.

이후 Python 환경을 구성하고 프로젝트 참여 권한을 확인한 뒤 AI-Data-Platform Repository를 내려받으면 된다.

---

## 30. 참고 기준

이 문서는 다음 공식 자료의 내용을 기준으로 작성하였다.

```text
Git 공식 문서
- macOS Git 설치 방법
- Git 기본 설치 및 설정

GitHub Docs
- Git 설정
- Git 사용자 이름 설정
- Commit 이메일 설정
- GitHub 인증 방식
- SSH 연결
- macOS Keychain Credential Helper

Homebrew 공식 문서
- Homebrew macOS 설치 요구사항
- Git Formula 설치 방법
```

설치 방식과 지원 버전은 시간이 지나면서 변경될 수 있으므로 실제 설치 시에는 최신 공식 문서를 함께 확인하는 것을 권장한다.
