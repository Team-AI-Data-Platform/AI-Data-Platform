# Git 핵심 가이드

> 이 문서는 Git을 처음 접하는 사용자가 **Git의 핵심 개념과 기본 명령어를 이해하고, 실제 프로젝트에서 소스를 안전하게 관리할 수 있도록** 정리한 기초 학습 가이드이다.  
> 단순히 명령어를 나열하기보다 `왜 사용하는지`, `각 명령이 Git의 어느 영역에 영향을 주는지`, `팀 프로젝트에서는 어떤 순서로 사용하는지`를 중심으로 설명한다.

---

## 1. Git이란?

Git은 소스 코드와 문서의 변경 이력을 관리하는 **분산 버전 관리 시스템(Distributed Version Control System)** 이다.

개발을 하다 보면 파일이 계속 변경된다.

예를 들어 하나의 Python 파일을 다음처럼 수정한다고 가정한다.

```text
app.py
  ↓
기능 추가
  ↓
버그 수정
  ↓
리팩토링
  ↓
새로운 기능 추가
```

파일을 단순히 저장하기만 하면 이전 상태를 추적하기 어렵다.

Git을 사용하면 변경 내용을 하나의 이력으로 관리할 수 있다.

```text
Version 1
   ↓
Version 2
   ↓
Version 3
   ↓
Version 4
```

필요한 경우 과거 변경 내용을 확인하거나 특정 시점으로 돌아갈 수도 있다.

---

## 2. Git을 사용하는 이유

Git의 주요 목적은 다음과 같다.

### 변경 이력 관리

누가, 언제, 어떤 파일을 수정했는지 기록할 수 있다.

### 이전 버전 확인

프로젝트의 과거 상태와 현재 상태를 비교할 수 있다.

### 팀 협업

여러 명이 동일한 프로젝트를 함께 개발할 수 있다.

### 작업 분리

Branch를 사용하여 새로운 기능이나 실험 작업을 기존 소스와 분리할 수 있다.

### 장애 복구

문제가 발생한 변경 사항을 추적하고 이전 상태를 참고할 수 있다.

---

## 3. Git과 GitHub의 차이

처음 Git을 공부할 때 가장 많이 혼동하는 부분이다.

Git과 GitHub는 같은 것이 아니다.

```text
Git
→ 내 PC에서 소스의 변경 이력을 관리하는 도구

GitHub
→ Git Repository를 인터넷에서 저장하고 공유하는 서비스
```

구조로 보면 다음과 같다.

```text
개발자 PC
   │
   │ Git
   ▼
Local Repository
   │
   │ push / pull
   ▼
GitHub
Remote Repository
```

Git만으로도 로컬 PC에서 버전 관리를 할 수 있다.

GitHub를 함께 사용하면 다른 개발자와 Repository를 공유할 수 있다.

---

## 4. Repository란?

Repository는 Git이 관리하는 프로젝트 저장소이다.

일반적인 프로젝트 폴더를 Git Repository로 만들면 Git이 파일의 변경 이력을 관리하기 시작한다.

```text
AI-Data-Platform/
├─ docs/
├─ labs/
├─ mkdocs.yml
├─ README.md
└─ .git/
```

여기서 `.git/` 디렉터리는 Git Repository의 핵심 영역이다.

Git은 이 디렉터리에 다음과 같은 정보를 관리한다.

- Commit 이력
- Branch 정보
- Remote Repository 정보
- 파일 추적 상태
- Git 설정 정보

> `.git/` 디렉터리를 임의로 삭제하면 해당 프로젝트는 더 이상 기존 Git Repository로 동작하지 않는다.

---

## 5. Local Repository와 Remote Repository

Git 프로젝트에서는 두 종류의 Repository를 이해하는 것이 중요하다.

### Local Repository

현재 사용자의 PC에 존재하는 Repository이다.

예:

```text
C:\projects\AI-Data-Platform
```

macOS에서는 다음과 같은 형태가 될 수 있다.

```text
~/projects/AI-Data-Platform
```

### Remote Repository

GitHub처럼 네트워크에 존재하는 원격 Repository이다.

```text
Local Repository
      │
      │ git push
      ▼
Remote Repository
      │
      │ git pull
      ▼
Local Repository
```

팀 프로젝트에서는 일반적으로 GitHub Repository를 Remote Repository로 사용한다.

---

## 6. Git의 핵심 작업 영역

Git을 이해할 때 가장 중요한 개념 중 하나이다.

Git에는 크게 다음 세 영역이 있다.

```text
Working Directory
       ↓
    git add
       ↓
Staging Area
       ↓
  git commit
       ↓
Local Repository
```

GitHub까지 포함하면 다음과 같다.

```text
Working Directory
       ↓
    git add
       ↓
Staging Area
       ↓
  git commit
       ↓
Local Repository
       ↓
   git push
       ↓
Remote Repository
```

---

## 7. Working Directory란?

Working Directory는 실제로 파일을 만들고 수정하는 프로젝트 폴더이다.

예:

```text
AI-Data-Platform/
├─ docs/
├─ labs/
├─ mkdocs.yml
└─ README.md
```

사용자가 `README.md`를 수정했다면 그 변경은 우선 Working Directory에 존재한다.

아직 Commit된 것은 아니다.

---

## 8. Staging Area란?

Staging Area는 **다음 Commit에 포함할 변경 사항을 선택해 놓는 영역**이다.

예를 들어 다음 세 파일을 수정했다고 가정한다.

```text
README.md
mkdocs.yml
test.py
```

이 중 `README.md`와 `mkdocs.yml`만 Commit하고 싶다면 다음과 같이 선택할 수 있다.

```bash
git add README.md
git add mkdocs.yml
```

그러면 두 파일만 Staging Area에 올라간다.

```text
Working Directory
├─ README.md  ─────┐
├─ mkdocs.yml ─────┼──→ Staging Area
└─ test.py          │
                    └─ test.py는 아직 제외
```

---

## 9. Commit이란?

Commit은 Staging Area에 준비된 변경 내용을 **하나의 변경 이력으로 저장하는 작업**이다.

예:

```bash
git commit -m "Add project setup guide"
```

Commit은 일종의 프로젝트 저장 지점이라고 이해하면 쉽다.

```text
Commit A
   ↓
Commit B
   ↓
Commit C
   ↓
Commit D
```

각 Commit에는 다음 정보가 포함된다.

- 변경된 파일
- 변경 내용
- 작성자
- 작성 시간
- Commit 메시지
- 고유 Commit ID

---

## 10. Git 기본 흐름 한 번에 이해하기

다음 흐름을 먼저 기억하면 Git의 기본 구조를 이해하기 쉽다.

```text
파일 수정
   ↓
git status
   ↓
git add
   ↓
git commit
   ↓
git push
```

팀 프로젝트에서는 작업 시작 전에 `pull`이 추가된다.

```text
git pull
   ↓
파일 수정
   ↓
git status
   ↓
git add
   ↓
git commit
   ↓
git push
```

---

# Part 1. Git 기본 명령어

---

## 11. `git --version`

Git 설치 여부와 버전을 확인한다.

```bash
git --version
```

예:

```text
git version 2.x.x
```

Git 명령을 사용할 수 없다면 Git 설치 또는 PATH 설정을 확인해야 한다.

---

## 12. `git status`

현재 Repository의 상태를 확인한다.

```bash
git status
```

Git을 사용할 때 가장 자주 사용하는 명령어 중 하나이다.

다음 정보를 확인할 수 있다.

- 현재 Branch
- 수정된 파일
- 새 파일
- 삭제된 파일
- Staging Area에 올라간 파일
- 아직 Stage되지 않은 파일

정상적인 예:

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

`working tree clean`은 현재 Commit하지 않은 변경 사항이 없다는 의미이다.

---

## 13. `git add`

변경된 파일을 Staging Area에 추가한다.

특정 파일:

```bash
git add README.md
```

여러 파일:

```bash
git add README.md mkdocs.yml
```

현재 디렉터리의 변경 사항 전체:

```bash
git add .
```

`git add .`는 편리하지만, 원하지 않는 파일까지 Stage할 수 있다.

따라서 먼저 다음 명령을 실행하는 습관이 좋다.

```bash
git status
```

---

## 14. `git commit`

Staging Area의 내용을 Local Repository에 저장한다.

```bash
git commit -m "Add Git study guide"
```

`-m`은 Commit 메시지를 명령어에서 바로 지정하는 옵션이다.

좋은 Commit 메시지:

```text
Add Git core guide
Update Python setup document
Fix MkDocs navigation
Add Ollama Windows setup guide
```

좋지 않은 예:

```text
update
test
aaa
수정
```

Commit 메시지만 보고도 어떤 작업인지 이해할 수 있도록 작성하는 것이 좋다.

---

## 15. `git log`

Commit 이력을 확인한다.

```bash
git log
```

간단한 형태:

```bash
git log --oneline
```

예:

```text
9d31abc Add Git core guide
72af251 Update project navigation
13bc482 Add Ollama setup guide
```

앞의 값은 Commit ID의 축약형이다.

---

## 16. `git diff`

아직 Stage하지 않은 변경 내용을 확인한다.

```bash
git diff
```

특정 파일:

```bash
git diff mkdocs.yml
```

Commit하기 전에 실제 수정 내용을 다시 확인할 때 유용하다.

Stage된 변경 사항은 다음 명령으로 확인한다.

```bash
git diff --staged
```

---

# Part 2. GitHub와 소스 주고받기

---

## 17. `git clone`

Remote Repository를 로컬 PC에 처음 내려받는다.

```bash
git clone https://github.com/Team-AI-Data-Platform/AI-Data-Platform.git
```

구조:

```text
GitHub Repository
       ↓
    git clone
       ↓
Local Repository 생성
```

`clone`은 일반적으로 프로젝트를 처음 받을 때 한 번 사용한다.

---

## 18. `git remote`

현재 Local Repository와 연결된 Remote Repository 정보를 확인한다.

```bash
git remote -v
```

예:

```text
origin  https://github.com/Team-AI-Data-Platform/AI-Data-Platform.git (fetch)
origin  https://github.com/Team-AI-Data-Platform/AI-Data-Platform.git (push)
```

여기서 `origin`은 기본 Remote Repository 이름으로 많이 사용된다.

---

## 19. `git pull`

Remote Repository의 최신 변경 사항을 Local Repository로 가져온다.

```bash
git pull
```

또는:

```bash
git pull origin main
```

구조:

```text
GitHub
   ↓
git pull
   ↓
내 PC
```

작업을 시작하기 전에 팀원의 최신 변경 사항을 받기 위해 자주 사용한다.

---

## 20. `git push`

Local Repository의 Commit을 Remote Repository에 올린다.

```bash
git push
```

또는:

```bash
git push origin main
```

구조:

```text
내 PC
   ↓
git push
   ↓
GitHub
```

주의할 점은 **파일을 수정했다고 바로 Push되는 것은 아니라는 것**이다.

```text
파일 수정
   ↓
git add
   ↓
git commit
   ↓
git push
```

이 순서가 필요하다.

---

## 21. Clone과 Pull의 차이

처음 Git을 학습할 때 많이 헷갈리는 부분이다.

### Clone

프로젝트 자체가 로컬에 없을 때 처음 내려받는다.

```bash
git clone <repository-url>
```

### Pull

이미 Clone되어 있는 프로젝트의 최신 내용을 받는다.

```bash
git pull
```

한 문장으로 정리하면 다음과 같다.

```text
Clone
→ 처음 한 번 프로젝트 전체를 받는다.

Pull
→ 기존 프로젝트를 최신 상태로 갱신한다.
```

---

## 22. Fetch와 Pull의 차이

`git fetch`도 Remote Repository의 정보를 가져온다.

```bash
git fetch
```

차이는 Remote 변경 사항을 현재 Branch에 바로 반영하느냐이다.

```text
git fetch
→ Remote의 변경 정보를 가져옴
→ 현재 작업 파일에는 바로 합치지 않음

git pull
→ Remote의 변경 정보를 가져옴
→ 현재 Branch에 반영
```

Git을 처음 사용할 때는 보통 `git pull`을 먼저 익히면 된다.

---

# Part 3. Branch 이해하기

---

## 23. Branch란?

Branch는 하나의 Repository에서 작업 흐름을 분리하는 기능이다.

예를 들어 운영 중인 `main` Branch에서 새로운 기능을 바로 개발하면 작업 중 오류가 기존 코드에 영향을 줄 수 있다.

그래서 새로운 Branch를 만들 수 있다.

```text
main
 │
 ├──────── feature/login
 │
 └──────── feature/rag
```

각 Branch에서는 독립적으로 작업한 뒤 필요할 때 다시 합칠 수 있다.

---

## 24. 현재 Branch 확인

```bash
git branch
```

예:

```text
* main
```

`*` 표시는 현재 사용 중인 Branch를 의미한다.

---

## 25. 새 Branch 생성

새 Branch를 생성하면서 이동한다.

```bash
git switch -c feature/git-guide
```

의미:

```text
git switch
→ Branch 이동

-c
→ 새로운 Branch 생성

feature/git-guide
→ 생성할 Branch 이름
```

---

## 26. Branch 이동

기존 Branch로 이동한다.

```bash
git switch main
```

다시 작업 Branch로 이동:

```bash
git switch feature/git-guide
```

---

## 27. Branch를 사용하는 이유

Branch를 사용하면 다음과 같은 장점이 있다.

```text
main
→ 안정된 소스

feature/rag
→ RAG 기능 개발

feature/agent
→ Agent 기능 개발

docs/update
→ 문서 수정
```

여러 작업을 서로 분리할 수 있기 때문에 팀 협업에서 매우 중요하다.

---

# Part 4. Conflict 이해하기

---

## 28. Conflict란?

여러 사용자가 같은 파일의 같은 부분을 서로 다르게 수정하면 Git이 어떤 내용을 유지해야 할지 자동으로 결정하지 못할 수 있다.

이를 Conflict라고 한다.

예:

```text
사용자 A
mkdocs.yml 20번째 줄 수정
        ↓
Push

사용자 B
mkdocs.yml 같은 부분 수정
        ↓
Pull
        ↓
Conflict
```

---

## 29. Conflict 표시

Conflict가 발생하면 파일에 다음과 같은 표시가 나타날 수 있다.

```text
<<<<<<< HEAD

내가 수정한 내용

=======

Remote Repository에서 내려온 내용

>>>>>>> origin/main
```

Git은 어느 내용을 사용할지 개발자에게 결정하도록 맡긴다.

---

## 30. Conflict 해결 기본 흐름

먼저 상태를 확인한다.

```bash
git status
```

충돌된 파일을 열어 유지할 내용을 결정한다.

다음 표시를 제거한다.

```text
<<<<<<<
=======
>>>>>>>
```

최종 내용만 남긴 뒤:

```bash
git add <파일명>
```

Commit한다.

```bash
git commit
```

> Git을 처음 사용하는 경우 Conflict가 발생했다고 해서 파일을 바로 삭제하거나 `git reset --hard`, `git push --force`부터 실행하지 않는 것이 중요하다.

---

# Part 5. 작업 임시 보관

---

## 31. `git stash`

현재 작업 중인 변경 사항을 잠시 보관할 수 있다.

```bash
git stash
```

예를 들어 작업 중인데 최신 소스를 먼저 받아야 하는 경우 사용할 수 있다.

```text
작업 중
   ↓
git stash
   ↓
git pull
   ↓
git stash pop
   ↓
작업 계속
```

보관한 내용을 다시 적용:

```bash
git stash pop
```

Stash도 Conflict가 발생할 수 있으므로 기본 개념을 이해하고 사용하는 것이 좋다.

---

# Part 6. 팀 프로젝트에서의 Git 사용

---

## 32. 작업 시작 전 권장 흐름

프로젝트 작업을 시작할 때 다음 순서를 권장한다.

```bash
git status
git pull
```

의미:

```text
git status
→ 내 로컬에 수정 중인 파일이 있는지 확인

git pull
→ Remote Repository의 최신 변경 내용 반영
```

---

## 33. 작업 종료 시 권장 흐름

작업 완료 후:

```bash
git status
git diff
git add <파일명>
git commit -m "작업 내용"
git push
```

전체 흐름:

```text
작업 시작
   ↓
git status
   ↓
git pull
   ↓
파일 수정
   ↓
git status
   ↓
git diff
   ↓
git add
   ↓
git commit
   ↓
git push
```

---

## 34. 왜 `git status`가 중요한가?

Git 명령을 외우는 것보다 `git status`를 자주 확인하는 습관이 더 중요하다.

다음 상황에서 항상 확인하는 것이 좋다.

```text
작업 시작 전
Pull 전
Commit 전
Push 전
Conflict 발생 후
Branch 이동 전
```

현재 Git 상태를 모른 채 명령을 실행하면 의도하지 않은 변경이 발생할 수 있기 때문이다.

---

## 35. `git add .` 사용 시 주의

```bash
git add .
```

현재 위치의 많은 변경 사항을 한 번에 Stage할 수 있어 편리하다.

하지만 다음과 같은 파일까지 포함될 수 있다.

```text
테스트 파일
임시 파일
로그
IDE 설정
생성 결과
민감한 설정 파일
```

따라서 먼저:

```bash
git status
```

를 확인하는 것이 좋다.

기초 단계에서는 가능하면 필요한 파일을 명시적으로 Stage하는 습관도 도움이 된다.

```bash
git add README.md
git add mkdocs.yml
```

---

## 36. Commit 단위를 작게 유지하는 이유

다음 두 작업을 동시에 했다고 가정한다.

```text
1. Python 코드 수정
2. MkDocs 메뉴 변경
```

하나의 Commit으로 묶는 것보다 작업 목적에 따라 분리하면 이력을 이해하기 쉽다.

예:

```text
Commit 1
Fix RAG search logic

Commit 2
Update MkDocs navigation
```

Commit은 가능한 한 **하나의 의미 있는 변경 단위**로 만드는 것이 좋다.

---

# Part 7. 위험한 Git 명령어 주의

---

## 37. `git push --force`

다음 명령은 Remote Repository의 이력을 강제로 덮어쓸 수 있다.

```bash
git push --force
```

또는:

```bash
git push -f
```

특히 여러 사람이 사용하는 `main` Branch에서는 신중해야 한다.

Git을 처음 사용하는 단계에서는 문제가 발생했다고 해서 강제 Push부터 사용하는 것은 피한다.

---

## 38. `git reset --hard`

다음 명령 역시 주의가 필요하다.

```bash
git reset --hard
```

현재 작업 중인 변경 사항이 사라질 수 있다.

중요한 변경 사항이 있는지 먼저 확인한다.

```bash
git status
```

Git 명령을 잘 모르는 상태라면 프로젝트 담당자와 확인한 후 사용하는 것이 안전하다.

---

# Part 8. Git과 `.gitignore`

---

## 39. `.gitignore` 기본 개념

`.gitignore`는 Git이 추적하지 않을 파일과 디렉터리를 지정하는 파일이다.

예:

```gitignore
.venv/
site/
__pycache__/
*.pyc
.env
```

다음과 같은 파일은 Git에 관리할 필요가 없는 경우가 많다.

```text
Python 가상환경
빌드 결과
Cache
Log
IDE 설정
Secret
실습 실행 결과
```

`.gitignore` 상세 구성과 AI-Data-Platform 프로젝트의 권장 설정은 별도의 프로젝트 환경 구성 가이드에서 다룬다.

---

## 40. `.gitignore`가 필요한 이유

예를 들어 Python 가상환경 `.venv`를 Git에 올리면 많은 패키지 파일이 Repository에 포함될 수 있다.

```text
.venv/
 ├─ Scripts 또는 bin
 ├─ Lib 또는 lib
 └─ 수많은 Python 패키지
```

이 파일들은 각 개발자가 다시 생성할 수 있다.

```bash
python -m venv .venv
```

따라서 Git에는 실제 프로젝트 소스와 설정 중심으로 관리하는 것이 좋다.

---

# Part 9. AI-Data-Platform에서의 예제

---

## 41. MkDocs 문서를 수정하는 경우

예를 들어 다음 파일을 수정했다고 가정한다.

```text
docs/basic/git_core_guide.md
```

작업 시작:

```bash
git status
git pull
```

문서 수정 후:

```bash
git status
```

변경 내용 확인:

```bash
git diff docs/basic/git_core_guide.md
```

Stage:

```bash
git add docs/basic/git_core_guide.md
```

Commit:

```bash
git commit -m "Add Git core guide"
```

Push:

```bash
git push
```

---

## 42. 여러 파일을 함께 수정한 경우

예:

```text
docs/basic/git_core_guide.md
mkdocs.yml
```

확인:

```bash
git status
```

Stage:

```bash
git add docs/basic/git_core_guide.md
git add mkdocs.yml
```

Commit:

```bash
git commit -m "Add Git core guide to navigation"
```

Push:

```bash
git push
```

---

## 43. 이미 Clone한 프로젝트를 최신화하는 경우

프로젝트 폴더로 이동한다.

### Windows

```powershell
cd C:\projects\AI-Data-Platform
```

### macOS

```bash
cd ~/projects/AI-Data-Platform
```

상태 확인:

```bash
git status
```

최신 소스:

```bash
git pull
```

이 과정은 프로젝트를 다시 Clone하는 것이 아니다.

---

# Part 10. Git 명령어 빠른 정리

---

## 44. 자주 사용하는 명령어

| 명령어 | 역할 |
|---|---|
| `git --version` | Git 버전 확인 |
| `git status` | 현재 작업 상태 확인 |
| `git clone` | Repository 최초 복제 |
| `git pull` | Remote 최신 변경 내용 반영 |
| `git fetch` | Remote 변경 정보만 가져오기 |
| `git add` | Staging Area에 추가 |
| `git commit` | Local Repository에 변경 이력 저장 |
| `git push` | Commit을 Remote Repository에 반영 |
| `git diff` | 변경 내용 확인 |
| `git log` | Commit 이력 확인 |
| `git branch` | Branch 목록 및 현재 Branch 확인 |
| `git switch` | Branch 이동 |
| `git stash` | 작업 내용을 임시 보관 |
| `git remote -v` | Remote Repository 주소 확인 |

---

## 45. 가장 먼저 익힐 핵심 명령어

Git을 처음 공부한다면 모든 명령어를 한 번에 외울 필요는 없다.

우선 다음 여섯 개를 정확히 이해하는 것이 중요하다.

```bash
git status
```

```bash
git pull
```

```bash
git add
```

```bash
git commit
```

```bash
git push
```

```bash
git log --oneline
```

그리고 다음 흐름을 기억한다.

```text
Pull
 ↓
수정
 ↓
Status
 ↓
Add
 ↓
Commit
 ↓
Push
```

---

## 46. Git 기본 용어 정리

| 용어 | 의미 |
|---|---|
| Repository | Git으로 관리되는 저장소 |
| Local Repository | 내 PC의 Git Repository |
| Remote Repository | GitHub 등의 원격 Repository |
| Working Directory | 실제 파일을 수정하는 영역 |
| Staging Area | 다음 Commit에 넣을 변경 사항 준비 영역 |
| Commit | 하나의 변경 이력 |
| Branch | 독립적인 작업 흐름 |
| Clone | Remote Repository를 최초로 복사 |
| Pull | Remote 변경 내용을 Local에 반영 |
| Push | Local Commit을 Remote에 반영 |
| Conflict | 서로 다른 변경 사항이 충돌한 상태 |
| HEAD | 현재 Checkout되어 있는 Commit 또는 Branch 위치 |

---

## 47. 학습 체크리스트

다음 내용을 이해하면 Git 기초 학습의 기본 목표를 달성한 것이다.

- [ ] Git과 GitHub의 차이를 설명할 수 있다.
- [ ] Repository가 무엇인지 설명할 수 있다.
- [ ] Local Repository와 Remote Repository의 차이를 안다.
- [ ] Working Directory와 Staging Area를 이해한다.
- [ ] Commit이 무엇인지 이해한다.
- [ ] `git status` 결과를 기본적으로 읽을 수 있다.
- [ ] `git pull`의 역할을 안다.
- [ ] `git add`의 역할을 안다.
- [ ] `git commit`의 역할을 안다.
- [ ] `git push`의 역할을 안다.
- [ ] Clone과 Pull의 차이를 설명할 수 있다.
- [ ] Branch의 목적을 이해한다.
- [ ] Conflict가 왜 발생하는지 이해한다.
- [ ] `.gitignore`의 기본 목적을 이해한다.
- [ ] `git push --force`, `git reset --hard`가 주의가 필요한 명령임을 안다.

---

## 48. 최종 정리

Git에서 가장 중요한 것은 명령어를 많이 외우는 것이 아니라 **변경 내용이 어느 단계에 있는지를 이해하는 것**이다.

```text
Working Directory
        ↓ git add
Staging Area
        ↓ git commit
Local Repository
        ↓ git push
Remote Repository
```

그리고 팀 프로젝트에서는 다음 흐름을 기본 습관으로 만든다.

```text
작업 시작
   ↓
git status
   ↓
git pull
   ↓
파일 수정
   ↓
git status / git diff
   ↓
git add
   ↓
git commit
   ↓
git push
```

Git의 기본 흐름을 이해하면 SourceTree 같은 GUI 도구를 사용할 때도 각 버튼이 어떤 Git 명령을 수행하는지 쉽게 이해할 수 있다.

AI-Data-Platform 프로젝트에서도 Git은 단순한 소스 다운로드 도구가 아니라 **팀원이 동일한 문서, Python 코드, RAG 및 Agent 실습 자산을 함께 관리하기 위한 기본 협업 도구**로 사용한다.
