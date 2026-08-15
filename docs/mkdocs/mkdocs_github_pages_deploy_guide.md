# GitHub Pages 배포 및 운영 가이드

> 이 문서는 MkDocs로 구축한 AI-Data-Platform 문서 사이트를 **GitHub Pages에 배포하고 이후 변경 내용을 운영하는 방법**을 설명한다.  
> Windows 및 macOS 공통 가이드이며, MkDocs 문서 사이트가 로컬에서 정상적으로 실행되는 상태를 기준으로 한다.

---

## 1. 문서 작성 목적

MkDocs에서 작성한 문서는 기본적으로 로컬 PC에서 확인할 수 있다.

```text
Markdown 문서
    ↓
mkdocs serve
    ↓
http://127.0.0.1:8000/
```

팀원 또는 외부 사용자가 웹 브라우저에서 문서 사이트에 접근하려면 정적 웹사이트 결과물을 웹 서버에 배포해야 한다.

AI-Data-Platform에서는 GitHub Repository와 GitHub Pages를 이용해 MkDocs 문서 사이트를 배포할 수 있다.

전체 구조는 다음과 같다.

```text
docs/
mkdocs.yml
   ↓
MkDocs Build
   ↓
정적 사이트
   ↓
gh-pages Branch
   ↓
GitHub Pages
   ↓
웹 브라우저
```

---

## 2. 본 가이드의 범위

본 문서에서는 다음 내용을 다룬다.

- GitHub Pages와 `gh-pages` Branch 개념
- 배포 전 로컬 확인
- Git Repository 상태 확인
- `mkdocs gh-deploy`
- GitHub Pages Publishing Source 설정
- 배포 URL 확인
- 문서 수정 후 재배포
- `main`과 `gh-pages` 역할 차이
- GitHub 인증
- 대표적인 배포 오류
- 운영 시 권장 작업 흐름

MkDocs 설치 및 문서 사이트 구성은 다음 문서에서 다룬다.

```text
MkDocs 문서 관리
 → MkDocs 문서 사이트 구축
```

---

## 3. 사전 준비사항

GitHub Pages 배포 전에 다음 항목이 완료되어 있어야 한다.

- GitHub Repository가 존재한다.
- 로컬 프로젝트가 Remote Repository와 연결되어 있다.
- GitHub Repository에 대한 필요한 Push 권한이 있다.
- MkDocs 설치가 완료되어 있다.
- Material for MkDocs가 필요한 경우 설치되어 있다.
- `mkdocs serve`가 정상적으로 실행된다.
- `mkdocs build`가 정상적으로 완료된다.

---

## 4. 프로젝트 디렉터리 이동

### Windows PowerShell

```powershell
cd C:\projects\AI-Data-Platform
```

### macOS

```bash
cd ~/projects/AI-Data-Platform
```

현재 디렉터리에 다음 항목이 있는지 확인한다.

```text
docs/
mkdocs.yml
.git/
```

---

## 5. Python 가상환경 활성화

MkDocs가 `.venv`에 설치되어 있다면 가상환경을 활성화한다.

### Windows

```powershell
.\.venv\Scripts\Activate.ps1
```

### macOS

```bash
source .venv/bin/activate
```

확인:

```bash
mkdocs --version
```

---

## 6. 배포 전 로컬 확인

배포 전에 문서 사이트가 정상적으로 동작하는지 확인한다.

```bash
mkdocs serve
```

브라우저:

```text
http://127.0.0.1:8000/
```

확인할 항목:

```text
메뉴가 정상적으로 표시되는가?
문서 링크가 정상적으로 열리는가?
이미지가 정상적으로 표시되는가?
코드 블록이 정상적으로 표시되는가?
Mermaid가 정상적으로 표시되는가?
경고 메시지가 없는가?
```

로컬 확인이 끝나면:

```text
Ctrl + C
```

로 서버를 종료한다.

---

## 7. 배포 전 빌드 확인

다음 명령을 실행한다.

```bash
mkdocs build
```

오류 없이 완료되어야 한다.

특히 다음과 같은 Warning은 확인한다.

```text
A reference to 'xxx.md' is included in the 'nav' configuration,
which is not found in the documentation files.
```

이 경우 실제 배포 전에 `mkdocs.yml`의 경로를 수정한다.

---

## 8. Git Repository 연결 확인

Remote Repository를 확인한다.

```bash
git remote -v
```

예:

```text
origin  https://github.com/Team-AI-Data-Platform/AI-Data-Platform.git (fetch)
origin  https://github.com/Team-AI-Data-Platform/AI-Data-Platform.git (push)
```

Remote가 없다면 GitHub Repository 연결부터 진행해야 한다.

본 문서에서는 이미 Repository가 연결되어 있다고 가정한다.

---

## 9. Source Branch와 배포 Branch 이해

MkDocs + GitHub Pages 배포에서는 일반적으로 역할이 두 부분으로 나뉜다.

```text
main
│
├─ docs/
├─ mkdocs.yml
├─ README.md
└─ 기타 소스
```

그리고:

```text
gh-pages
│
├─ index.html
├─ assets/
├─ search/
└─ MkDocs가 생성한 정적 사이트 결과물
```

정리하면:

| Branch | 역할 |
|---|---|
| `main` | Markdown 원본, 설정 파일, 프로젝트 소스 |
| `gh-pages` | GitHub Pages에 게시할 정적 웹사이트 결과물 |

`gh-pages` Branch의 파일은 일반적으로 개발자가 직접 수정하지 않는다.

MkDocs 배포 명령이 자동으로 생성하고 갱신한다.

---

## 10. `mkdocs gh-deploy`란?

MkDocs는 GitHub Pages 배포를 위한 `gh-deploy` 명령을 제공한다.

```bash
mkdocs gh-deploy
```

이 명령을 실행하면 기본적으로 다음과 같은 흐름이 수행된다.

```text
MkDocs Build
     ↓
정적 사이트 생성
     ↓
gh-pages Branch 준비
     ↓
배포 결과 Commit
     ↓
GitHub Push
```

MkDocs 공식 문서 기준 기본 Remote 이름은 `origin`, 기본 배포 Branch는 `gh-pages`이다.

---

## 11. 첫 배포 실행

프로젝트 루트에서 실행한다.

```bash
mkdocs gh-deploy
```

정상적으로 완료되면 `gh-pages` Branch가 GitHub에 생성 또는 갱신된다.

배포 과정에서 GitHub 인증이 필요할 수 있다.

---

## 12. `--force` 옵션

필요한 경우 다음 명령을 사용할 수 있다.

```bash
mkdocs gh-deploy --force
```

`--force`는 배포 이력을 강제로 갱신해야 하는 특정 상황에서 사용할 수 있다.

하지만 다음과 같은 문제는 `--force`로 해결되지 않는다.

```text
GitHub 인증 실패
Repository 권한 없음
Remote URL 오류
mkdocs.yml 오류
```

따라서 오류가 발생하면 원인을 먼저 확인한다.

---

## 13. GitHub Pages 설정

GitHub Repository에서 다음 경로로 이동한다.

```text
Repository
 → Settings
 → Pages
```

Branch 기반 배포를 사용하는 경우 `Build and deployment`에서 Publishing Source를 설정한다.

일반적인 구성:

```text
Source
→ Deploy from a branch

Branch
→ gh-pages

Folder
→ / (root)
```

GitHub Pages는 지정된 Branch와 디렉터리를 Publishing Source로 사용할 수 있다.

---

## 14. GitHub Pages URL 확인

설정이 완료되고 배포가 처리되면 GitHub Pages URL을 확인할 수 있다.

프로젝트 사이트는 일반적으로 다음 형식이다.

```text
https://<조직명 또는 계정명>.github.io/<Repository명>/
```

예:

```text
https://team-ai-data-platform.github.io/AI-Data-Platform/
```

실제 URL은 Repository와 GitHub Pages 설정에 따라 확인한다.

---

## 15. 최초 배포 후 반영 시간

GitHub Pages 설정 또는 `gh-pages` Push 직후 사이트가 즉시 표시되지 않을 수 있다.

잠시 기다린 뒤 다시 확인한다.

확인할 항목:

```text
gh-pages Branch가 존재하는가?
Pages Source가 gh-pages인가?
Folder가 / (root)인가?
Pages 배포 상태가 정상인가?
URL이 정확한가?
```

---

## 16. 원본 문서 GitHub 반영

`mkdocs gh-deploy`는 문서 사이트 배포 작업이다.

Markdown 원본과 `mkdocs.yml`의 변경 내용은 별도로 Source Branch에 Commit하고 Push해야 한다.

예:

```bash
git status
```

```bash
git add docs/ mkdocs.yml
```

```bash
git commit -m "Update MkDocs documentation"
```

```bash
git push
```

그 다음 사이트를 배포한다.

```bash
mkdocs gh-deploy
```

---

## 17. 문서 수정 후 권장 배포 흐름

문서를 수정한 뒤에는 다음 순서를 권장한다.

```text
git pull
   ↓
문서 수정
   ↓
mkdocs serve
   ↓
로컬 확인
   ↓
mkdocs build
   ↓
git status
   ↓
git add / commit / push
   ↓
mkdocs gh-deploy
   ↓
GitHub Pages 확인
```

명령 예:

```bash
git pull
mkdocs serve
```

문서 확인 후 서버 종료:

```text
Ctrl + C
```

그 다음:

```bash
mkdocs build
git status
git add .
git commit -m "Update documentation"
git push
mkdocs gh-deploy
```

---

## 18. GitHub 인증 이해

`mkdocs gh-deploy` 마지막 단계에서는 Git이 `gh-pages` Branch를 GitHub에 Push한다.

따라서 GitHub 인증이 정상적으로 되어 있어야 한다.

HTTPS Remote를 사용하는 경우 GitHub 계정 비밀번호를 Git 작업 인증에 직접 사용하는 방식은 지원되지 않는다.

대표적인 인증 방식은 다음과 같다.

```text
Git Credential Manager
Personal Access Token
SSH
GitHub CLI
```

Windows의 Git for Windows 환경에서는 Git Credential Manager를 통해 브라우저 로그인 방식으로 인증할 수 있다.

---

## 19. Windows에서 Git Credential Manager 확인

현재 Credential Helper를 확인한다.

```powershell
git config --get credential.helper
```

예:

```text
manager
```

현재 GCM GitHub 계정 확인:

```powershell
git credential-manager github list
```

계정이 없다면 로그인할 수 있다.

```powershell
git credential-manager github login
```

브라우저 로그인 방식을 선택하고 GitHub 인증을 완료한다.

---

## 20. macOS의 GitHub 인증

macOS에서도 HTTPS, SSH, GitHub CLI 등 여러 인증 방식을 사용할 수 있다.

Repository가 HTTPS로 연결되어 있다면:

```bash
git remote -v
```

를 통해 Remote URL을 확인한다.

GitHub CLI를 사용하는 경우 다음과 같이 인증할 수 있다.

```bash
gh auth login
```

SSH 방식을 사용하는 경우 GitHub 계정에 SSH Key가 사전에 등록되어 있어야 한다.

---

## 21. `Invalid username or token`

오류 예:

```text
remote: Invalid username or token.
Password authentication is not supported for Git operations.
fatal: Authentication failed
```

이 오류는 MkDocs Build 문제가 아니라 **GitHub Push 인증 문제**이다.

확인 순서:

```text
1. git remote -v
2. 현재 GitHub 인증 계정 확인
3. Repository 접근 권한 확인
4. Credential 재로그인
5. 다시 배포
```

Windows에서 GCM을 사용하는 경우:

```powershell
git credential-manager github list
```

필요하면:

```powershell
git credential-manager github login
```

을 사용할 수 있다.

---

## 22. Repository 권한 오류

인증된 GitHub 계정이 Repository에 Push할 권한이 없는 경우 배포가 실패한다.

확인:

```text
Repository에 올바른 GitHub 계정으로 로그인했는가?
Repository 초대를 수락했는가?
Write 이상의 필요한 권한이 있는가?
조직 정책에 의해 Push가 제한되어 있지 않은가?
```

`gh-pages`에 Push해야 하므로 단순 조회 권한만으로는 배포할 수 없다.

---

## 23. `Repository not found`

가능한 원인:

```text
Remote URL 오류
Repository 이름 오류
GitHub 계정 오류
Private Repository 접근 권한 없음
```

확인:

```bash
git remote -v
```

브라우저에서도 현재 GitHub 계정으로 Repository가 정상적으로 열리는지 확인한다.

---

## 24. Pages가 404로 표시되는 경우

확인 순서:

```text
1. gh-pages Branch 생성 확인
2. Repository → Settings → Pages 확인
3. Source가 Deploy from a branch인지 확인
4. Branch가 gh-pages인지 확인
5. Folder가 / (root)인지 확인
6. 배포 처리 완료 여부 확인
7. URL 확인
```

배포 직후라면 잠시 기다린 뒤 다시 확인한다.

---

## 25. 수정했는데 사이트에 반영되지 않는 경우

먼저 로컬 문서 변경이 저장되어 있는지 확인한다.

```bash
git status
```

배포를 다시 실행한다.

```bash
mkdocs gh-deploy
```

필요한 경우:

```bash
mkdocs gh-deploy --force
```

브라우저 Cache 문제일 수도 있으므로 새로고침한다.

### Windows / Chrome 일반 예

```text
Ctrl + Shift + R
```

### macOS / Chrome 일반 예

```text
Cmd + Shift + R
```

---

## 26. `mkdocs gh-deploy` 전에 Build 오류가 발생하는 경우

배포 명령은 먼저 MkDocs 사이트를 Build하므로 `mkdocs.yml` 또는 Markdown 오류가 있으면 배포 전에 실패할 수 있다.

먼저:

```bash
mkdocs build
```

를 실행해 오류를 분리해서 확인한다.

예:

```text
nav 경로 오류
YAML 문법 오류
Plugin 미설치
Theme 미설치
Extension 설정 오류
```

---

## 27. Material for MkDocs Version Warning

Material for MkDocs에서 향후 호환성 관련 Warning이 표시될 수 있다.

예:

```text
WARNING - ...
```

Warning이 표시되더라도 Build가 정상 완료되고 `gh-pages` Push 단계까지 진행된다면 실제 실패 원인은 다른 곳에 있을 수 있다.

따라서 다음을 구분해서 확인한다.

```text
WARNING
→ 주의 메시지

ERROR / Traceback / fatal
→ 실제 실패 원인
```

배포 실패 시 마지막 오류 메시지부터 확인하는 것이 좋다.

---

## 28. `gh-pages` Branch를 직접 수정하지 않는 이유

`gh-pages`는 MkDocs가 생성한 정적 결과물 관리용 Branch이다.

```text
main
→ 사람이 수정

gh-pages
→ MkDocs가 생성
```

따라서 일반적으로 다음 작업은 `main`에서 수행한다.

```text
Markdown 수정
mkdocs.yml 수정
이미지 추가
CSS 수정
```

그 후:

```bash
mkdocs gh-deploy
```

로 `gh-pages`를 갱신한다.

---

## 29. GitHub Pages와 `site/` 차이

로컬에서:

```bash
mkdocs build
```

를 실행하면:

```text
site/
```

가 생성된다.

GitHub Pages 배포에서는 MkDocs가 이와 같은 정적 결과물을 `gh-pages` Branch에 배포한다.

```text
Local

docs/
mkdocs.yml
   ↓
site/
```

```text
GitHub

main
   ↓
mkdocs gh-deploy
   ↓
gh-pages
   ↓
GitHub Pages
```

따라서 `main` Branch의 `site/`는 일반적으로 `.gitignore`로 제외한다.

---

## 30. 배포 Branch 설정 변경 참고

MkDocs의 `gh-deploy`는 기본적으로 다음 설정을 사용한다.

```text
Remote
→ origin

Branch
→ gh-pages
```

필요한 경우 `mkdocs.yml`에서 Remote 관련 설정을 지정할 수 있다.

예:

```yaml
remote_name: origin
remote_branch: gh-pages
```

일반적인 프로젝트에서는 기본값을 그대로 사용할 수 있다.

---

## 31. GitHub Pages 운영 방식 참고

GitHub Pages는 Branch 기반 Publishing Source 또는 GitHub Actions 기반 배포 방식을 사용할 수 있다.

본 가이드는 MkDocs의 기본 `gh-deploy` 명령을 이용해:

```text
gh-pages Branch
        ↓
GitHub Pages
```

로 배포하는 방식을 기준으로 한다.

향후 CI/CD 자동 배포가 필요하다면 GitHub Actions 기반 방식으로 확장할 수 있다.

---

## 32. 팀 운영 시 배포 담당

팀원이 여러 명인 경우 모든 사람이 동시에 배포하는 것보다 배포 원칙을 정하는 것이 좋다.

예:

```text
팀원
→ Markdown 수정 / Push

문서 담당자
→ 최종 검토

배포 담당자
→ mkdocs gh-deploy
```

또는 작은 학습 프로젝트에서는 팀원 누구나 배포할 수 있도록 운영할 수도 있다.

프로젝트 규모가 커지면 GitHub Actions로 자동 배포하는 방법을 검토할 수 있다.

---

## 33. 배포 전 체크리스트

- [ ] 최신 `main`을 Pull했다.
- [ ] Python 가상환경을 활성화했다.
- [ ] `mkdocs --version`이 정상이다.
- [ ] `mkdocs serve`로 로컬 확인했다.
- [ ] 메뉴와 이미지가 정상적으로 표시된다.
- [ ] `mkdocs build`가 정상 완료된다.
- [ ] `git status`를 확인했다.
- [ ] 원본 Markdown 변경사항을 Commit했다.
- [ ] `main` Branch에 Push했다.
- [ ] GitHub 인증 계정이 올바르다.
- [ ] Repository Push 권한이 있다.

---

## 34. 배포 후 체크리스트

- [ ] `mkdocs gh-deploy`가 정상 완료되었다.
- [ ] GitHub에 `gh-pages` Branch가 존재한다.
- [ ] Repository → Settings → Pages 설정이 정상이다.
- [ ] Publishing Source가 `gh-pages`이다.
- [ ] Folder가 `/ (root)`이다.
- [ ] GitHub Pages URL이 정상적으로 열린다.
- [ ] 최신 문서가 웹사이트에 반영되었다.
- [ ] 이미지와 메뉴가 정상적으로 표시된다.

---

## 35. 최소 배포 명령어 정리

로컬 확인:

```bash
mkdocs serve
```

Build 확인:

```bash
mkdocs build
```

원본 문서 Git 반영:

```bash
git add .
git commit -m "Update documentation"
git push
```

GitHub Pages 배포:

```bash
mkdocs gh-deploy
```

필요한 경우:

```bash
mkdocs gh-deploy --force
```

---

## 36. 전체 운영 흐름

```text
GitHub main 최신화
       ↓
Markdown 수정
       ↓
mkdocs serve
       ↓
브라우저 검토
       ↓
mkdocs build
       ↓
Git Commit / Push
       ↓
mkdocs gh-deploy
       ↓
gh-pages 갱신
       ↓
GitHub Pages 반영
       ↓
웹사이트 확인
```

---

## 37. 참고 공식 문서

- MkDocs - Deploying Your Docs  
  https://www.mkdocs.org/user-guide/deploying-your-docs/

- MkDocs CLI - `gh-deploy`  
  https://www.mkdocs.org/user-guide/cli/

- MkDocs Configuration  
  https://www.mkdocs.org/user-guide/configuration/

- GitHub Pages - Configuring a publishing source  
  https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

- GitHub Pages Quickstart  
  https://docs.github.com/pages/quickstart

---

## 38. 최종 정리

MkDocs와 GitHub Pages의 역할을 구분하면 배포 구조를 쉽게 이해할 수 있다.

```text
MkDocs
→ Markdown을 정적 웹사이트로 변환

GitHub
→ 원본 문서와 소스 관리

gh-pages
→ 정적 웹사이트 결과물 관리

GitHub Pages
→ gh-pages의 결과물을 웹사이트로 제공
```

가장 중요한 배포 명령은 다음과 같다.

```bash
mkdocs gh-deploy
```

하지만 실제 운영에서는 그 전에 다음 절차를 지키는 것이 중요하다.

```text
로컬 확인
→ Build 확인
→ 원본 Git 반영
→ GitHub Pages 배포
→ 웹사이트 확인
```

Windows와 macOS는 Git/Python/가상환경 설치 과정에는 차이가 있지만, **MkDocs 문서 사이트를 GitHub Pages에 배포하는 핵심 흐름은 동일하게 적용할 수 있다.**
