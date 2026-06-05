# MkDocs + GitHub Pages 문서 사이트 구축 가이드 — Windows 기준

> 이 문서는 MkDocs로 마크다운 기반 문서 사이트를 만들고, GitHub Pages를 통해 웹에서 확인하는 전체 과정을 정리한 가이드입니다.  
> Windows 환경 기준으로 작성했으며, 팀원이 처음부터 따라 할 수 있도록 설치 → 프로젝트 생성 → 로컬 확인 → GitHub 업로드 → Pages 배포 → 웹 확인 순서로 설명합니다.

---

## 1. 전체 흐름 이해

MkDocs + GitHub Pages를 사용하면 다음과 같은 방식으로 문서 사이트를 운영할 수 있습니다.

```text
마크다운 문서 작성
        ↓
MkDocs로 정적 웹사이트 생성
        ↓
GitHub 저장소에 소스 업로드
        ↓
mkdocs gh-deploy 실행
        ↓
gh-pages 브랜치에 웹사이트 결과물 배포
        ↓
GitHub Pages URL로 웹에서 확인
```

일반적으로 저장소에는 두 종류의 내용이 관리됩니다.

| 구분 | 위치 | 설명 |
|---|---|---|
| 문서 원본 | `main` 또는 `master` 브랜치 | `docs/`, `mkdocs.yml` 등 실제 작성하는 파일 |
| 배포 결과물 | `gh-pages` 브랜치 | MkDocs가 생성한 HTML/CSS/JS 정적 사이트 |

---

## 2. Windows 사전 준비사항

아래 프로그램이 필요합니다.

| 항목 | 설명 |
|---|---|
| Python | MkDocs는 Python 기반 도구입니다. |
| pip | Python 패키지 설치 도구입니다. Python 설치 시 함께 설치되는 경우가 많습니다. |
| Git | GitHub 저장소에 소스를 올리기 위해 필요합니다. |
| VS Code 또는 메모장 | `mkdocs.yml`, `.md` 파일을 수정하기 위한 편집기입니다. |
| GitHub 계정 | GitHub Pages 사용을 위해 필요합니다. |
| GitHub 저장소 | 문서 사이트를 배포할 Repository입니다. |

Windows에서는 **PowerShell** 또는 **명령 프롬프트(cmd)** 에서 명령어를 실행합니다.  
VS Code를 사용한다면 상단 메뉴에서 다음 경로로 터미널을 열 수 있습니다.

```text
VS Code → Terminal → New Terminal
```

이 문서의 명령어는 기본적으로 **PowerShell 기준**으로 작성합니다.

---

## 3. 설치 여부 확인

PowerShell을 열고 아래 명령어를 실행합니다.

```powershell
python --version
pip --version
git --version
```

또는 Windows Python Launcher를 사용하는 경우 아래처럼 확인할 수도 있습니다.

```powershell
py --version
py -m pip --version
git --version
```

예시:

```text
Python 3.13.0
pip 25.x.x
git version 2.x.x.windows.x
```

Python이 여러 개 설치되어 있거나 `python` 명령어가 동작하지 않는 경우에는 이 문서에서 `py` 명령어를 사용하는 방식을 권장합니다.

---

## 4. MkDocs 설치

### 4.1 기본 설치

PowerShell에서 아래 명령어를 실행합니다.

```powershell
py -m pip install mkdocs mkdocs-material
```

설치가 완료되면 다음 명령어로 확인합니다.

```powershell
mkdocs --version
```

정상이라면 아래와 비슷하게 출력됩니다.

```text
mkdocs, version 1.6.1
```

### 4.2 `mkdocs` 명령어가 안 될 때 권장 실행 방법

Windows에서는 PATH 설정 문제 때문에 `mkdocs` 명령어가 바로 인식되지 않을 수 있습니다.

이 경우 아래처럼 실행하면 됩니다.

```powershell
py -m mkdocs --version
```

즉, 아래 두 명령어는 같은 역할로 이해하면 됩니다.

| 일반 명령어 | PATH 문제가 있을 때 |
|---|---|
| `mkdocs --version` | `py -m mkdocs --version` |
| `mkdocs serve` | `py -m mkdocs serve` |
| `mkdocs build` | `py -m mkdocs build` |
| `mkdocs gh-deploy --force` | `py -m mkdocs gh-deploy --force` |

처음 환경 설정이 익숙하지 않다면 이 문서에서는 `py -m mkdocs` 방식을 사용해도 됩니다.

---

## 5. Windows에서 `mkdocs`가 인식되지 않는 경우

### 5.1 오류 예시

```text
mkdocs : 'mkdocs' 용어가 cmdlet, 함수, 스크립트 파일 또는 실행할 수 있는 프로그램 이름으로 인식되지 않습니다.
```

또는 영문 환경에서는 아래처럼 나올 수 있습니다.

```text
'mkdocs' is not recognized as an internal or external command,
operable program or batch file.
```

원인은 MkDocs는 설치되었지만, Windows가 `mkdocs.exe` 위치를 PATH에서 찾지 못하는 상태입니다.

### 5.2 가장 쉬운 해결 방법

PATH를 수정하지 않고 아래처럼 실행합니다.

```powershell
py -m mkdocs --version
```

이 방식은 Windows에서 가장 안전합니다.

### 5.3 MkDocs 실행 파일 위치 확인

아래 명령어로 Python 패키지 설치 경로를 확인할 수 있습니다.

```powershell
py -m site --user-base
```

예시:

```text
C:\Users\User\AppData\Roaming\Python
```

MkDocs 실행 파일은 보통 아래와 비슷한 위치에 있습니다.

```text
C:\Users\User\AppData\Roaming\Python\Python313\Scripts
```

또는 Python을 설치한 방식에 따라 아래 위치일 수 있습니다.

```text
C:\Users\User\AppData\Local\Programs\Python\Python313\Scripts
```

### 5.4 PATH에 추가하는 방법

Windows 검색창에서 아래 메뉴를 엽니다.

```text
시스템 환경 변수 편집 → 환경 변수 → 사용자 변수 Path → 편집 → 새로 만들기
```

아래 경로를 추가합니다.

```text
C:\Users\User\AppData\Roaming\Python\Python313\Scripts
```

사용자명과 Python 버전은 PC 환경에 맞게 변경합니다.

설정 후 PowerShell을 완전히 닫았다가 다시 열고 확인합니다.

```powershell
mkdocs --version
```

---

## 6. PowerShell 실행 정책 오류가 나는 경우

Windows PowerShell에서 아래와 같은 오류가 나올 수 있습니다.

```text
mkdocs.ps1 cannot be loaded because running scripts is disabled on this system.
```

이 경우에는 두 가지 방법 중 하나를 사용합니다.

### 6.1 권장 방법: `py -m mkdocs`로 실행

```powershell
py -m mkdocs serve
```

이 방식은 PowerShell 실행 정책을 변경하지 않아도 됩니다.

### 6.2 실행 정책 변경

회사 보안 정책상 허용되는 경우에만 아래 명령어를 사용합니다.

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

그 후 PowerShell을 다시 열고 실행합니다.

```powershell
mkdocs --version
```

회사 PC에서는 보안 정책상 제한될 수 있으므로, 가능하면 `py -m mkdocs` 방식을 권장합니다.

---

## 7. MkDocs 프로젝트 생성

문서 사이트를 만들 폴더로 이동한 뒤 프로젝트를 생성합니다.

예를 들어 `C:\Users\User\PEJ` 아래에 프로젝트를 만들 경우:

```powershell
cd C:\Users\User\PEJ
mkdir my-docs
cd my-docs
py -m mkdocs new .
```

생성 후 폴더 구조는 다음과 같습니다.

```text
my-docs/
├── docs/
│   └── index.md
└── mkdocs.yml
```

| 파일/폴더 | 설명 |
|---|---|
| `mkdocs.yml` | MkDocs 설정 파일 |
| `docs/` | 마크다운 문서를 저장하는 폴더 |
| `docs/index.md` | 사이트 첫 화면 문서 |

---

## 8. VS Code에서 프로젝트 열기

프로젝트 폴더에서 아래 명령어를 실행하면 VS Code로 열 수 있습니다.

```powershell
code .
```

`code` 명령어가 인식되지 않는 경우에는 VS Code에서 직접 폴더를 열면 됩니다.

```text
VS Code → File → Open Folder → my-docs 선택
```

---

## 9. 로컬에서 문서 사이트 실행

프로젝트 루트, 즉 `mkdocs.yml` 파일이 있는 위치에서 아래 명령어를 실행합니다.

```powershell
py -m mkdocs serve
```

정상 실행되면 아래와 비슷한 메시지가 표시됩니다.

```text
INFO    -  Building documentation...
INFO    -  Documentation built in 0.XX seconds
INFO    -  [16:00:00] Watching paths for changes: 'docs', 'mkdocs.yml'
INFO    -  [16:00:00] Serving on http://127.0.0.1:8000/
```

브라우저에서 아래 주소로 접속합니다.

```text
http://127.0.0.1:8000/
```

문서를 수정하면 브라우저 화면이 자동으로 갱신됩니다.

종료하려면 PowerShell에서 아래 키를 누릅니다.

```text
Ctrl + C
```

---

## 10. Material 테마 적용

`mkdocs-material`을 설치했다면 `mkdocs.yml` 파일을 아래처럼 수정합니다.

```yaml
site_name: Project Documentation

theme:
  name: material

nav:
  - Home: index.md
```

다시 실행합니다.

```powershell
py -m mkdocs serve
```

화면이 Material 테마로 변경됩니다.

---

## 11. 문서 추가하기

예를 들어 설치 가이드 문서를 추가하려면 아래 파일을 생성합니다.

```text
docs/setup.md
```

VS Code에서 `docs` 폴더를 우클릭한 뒤 `New File`을 선택해 `setup.md` 파일을 만들면 됩니다.

내용 예시:

```markdown
# 설치 가이드

이 문서는 프로젝트 설치 방법을 설명합니다.

## 1. 사전 준비

- Java
- Git
- IDE

## 2. 설치 절차

```bash
git clone <repository-url>
```
```

그리고 `mkdocs.yml`에 메뉴를 추가합니다.

```yaml
site_name: Project Documentation

theme:
  name: material

nav:
  - Home: index.md
  - 설치 가이드: setup.md
```

---

## 12. 사이트 빌드 확인

로컬 서버 실행 전 또는 배포 전에 빌드가 정상적으로 되는지 확인합니다.

```powershell
py -m mkdocs build
```

정상 빌드되면 `site/` 폴더가 생성됩니다.

```text
my-docs/
├── docs/
├── mkdocs.yml
└── site/
```

`site/` 폴더는 MkDocs가 만든 정적 웹사이트 결과물입니다.

일반적으로 `site/` 폴더는 Git에 올리지 않습니다.

`.gitignore` 파일에 아래 내용을 추가합니다.

```gitignore
site/
```

PowerShell에서 직접 만들고 싶다면 아래 명령어를 사용할 수 있습니다.

```powershell
New-Item -Path .gitignore -ItemType File -Force
Add-Content -Path .gitignore -Value "site/"
```

또는 메모장으로 열어서 작성할 수도 있습니다.

```powershell
notepad .gitignore
```

---

## 13. GitHub 저장소 생성

GitHub에서 새 Repository를 생성합니다.

예시:

```text
Repository name: my-docs
Visibility: Public 또는 Private
```

GitHub Pages 사용 가능 여부는 조직/계정 정책에 따라 다를 수 있습니다.  
일반적으로 Public 저장소에서는 GitHub Pages를 쉽게 사용할 수 있습니다.

---

## 14. 로컬 프로젝트를 GitHub에 업로드

현재 MkDocs 프로젝트 폴더에서 아래 명령어를 실행합니다.

```powershell
git init
git add .
git commit -m "Initial MkDocs documentation"
```

GitHub 저장소 주소를 연결합니다.

```powershell
git remote add origin https://github.com/<GitHub계정>/<저장소명>.git
```

예시:

```powershell
git remote add origin https://github.com/company/my-docs.git
```

기본 브랜치 이름을 `main`으로 맞춥니다.

```powershell
git branch -M main
```

GitHub로 push 합니다.

```powershell
git push -u origin main
```

---

## 15. GitHub Pages로 배포

MkDocs는 `gh-deploy` 명령어를 제공합니다.

프로젝트 루트, 즉 `mkdocs.yml` 파일이 있는 위치에서 아래 명령어를 실행합니다.

```powershell
py -m mkdocs gh-deploy
```

강제로 덮어쓰고 싶다면 아래처럼 실행할 수도 있습니다.

```powershell
py -m mkdocs gh-deploy --force
```

이 명령어는 내부적으로 다음 작업을 수행합니다.

```text
1. mkdocs build 실행
2. site/ 폴더에 정적 웹사이트 생성
3. gh-pages 브랜치 생성 또는 갱신
4. gh-pages 브랜치를 GitHub에 push
```

배포가 완료되면 GitHub 저장소에 `gh-pages` 브랜치가 생깁니다.

---

## 16. GitHub Pages 설정 확인

GitHub 저장소 화면에서 다음 경로로 이동합니다.

```text
Repository → Settings → Pages
```

아래와 같이 설정합니다.

| 항목 | 값 |
|---|---|
| Source | Deploy from a branch |
| Branch | `gh-pages` |
| Folder | `/ (root)` |

설정 후 저장합니다.

잠시 기다리면 GitHub Pages 주소가 표시됩니다.

```text
https://<GitHub계정>.github.io/<저장소명>/
```

예시:

```text
https://company.github.io/my-docs/
```

브라우저에서 해당 주소로 접속하면 MkDocs 문서 사이트를 확인할 수 있습니다.

---

## 17. 문서 수정 후 다시 배포하는 방법

문서를 수정한 뒤에는 아래 순서로 진행합니다.

### 17.1 로컬에서 확인

```powershell
py -m mkdocs serve
```

브라우저에서 확인합니다.

```text
http://127.0.0.1:8000/
```

### 17.2 원본 문서 GitHub 반영

```powershell
git add .
git commit -m "Update documentation"
git push
```

### 17.3 GitHub Pages 재배포

```powershell
py -m mkdocs gh-deploy --force
```

웹사이트 주소로 접속하여 변경사항을 확인합니다.

---

## 18. 권장 프로젝트 구조

팀 문서로 운영할 경우 아래 구조를 추천합니다.

```text
my-docs/
├── docs/
│   ├── index.md
│   ├── guide/
│   │   ├── setup.md
│   │   ├── development.md
│   │   └── deployment.md
│   ├── architecture/
│   │   ├── overview.md
│   │   └── system-structure.md
│   └── images/
│       └── architecture.png
├── mkdocs.yml
└── .gitignore
```

`mkdocs.yml` 예시:

```yaml
site_name: Project Documentation
site_description: 프로젝트 개발 및 운영 문서
site_author: Project Team

theme:
  name: material
  language: ko

nav:
  - Home: index.md
  - 가이드:
      - 설치 가이드: guide/setup.md
      - 개발 가이드: guide/development.md
      - 배포 가이드: guide/deployment.md
  - 아키텍처:
      - 개요: architecture/overview.md
      - 시스템 구성: architecture/system-structure.md

markdown_extensions:
  - admonition
  - tables
  - toc:
      permalink: true
  - pymdownx.highlight
  - pymdownx.superfences
```

---

## 19. 이미지 넣는 방법

이미지는 보통 `docs/images/` 폴더에 저장합니다.

예시:

```text
docs/images/system-architecture.png
```

마크다운 문서에서는 아래처럼 사용합니다.

```markdown
![시스템 구성도](../images/system-architecture.png)
```

`docs/index.md`에서 참조할 경우:

```markdown
![시스템 구성도](images/system-architecture.png)
```

문서 위치에 따라 상대 경로가 달라질 수 있으므로 주의합니다.

---

## 20. 자주 발생하는 오류와 해결 방법

### 20.1 `mkdocs` 명령어가 인식되지 않는 경우

오류 예시:

```text
'mkdocs' is not recognized as an internal or external command
```

원인:

```text
MkDocs는 설치되었지만 실행 경로가 PATH에 등록되지 않은 상태
```

해결 1: `py -m mkdocs`로 실행

```powershell
py -m mkdocs --version
py -m mkdocs serve
```

해결 2: PATH에 Scripts 경로 추가

```text
C:\Users\User\AppData\Roaming\Python\Python313\Scripts
```

PowerShell을 다시 열고 확인합니다.

```powershell
mkdocs --version
```

---

### 20.2 `mkdocs.ps1 cannot be loaded` 오류

원인:

```text
PowerShell 실행 정책 때문에 스크립트 실행이 막힌 상태
```

권장 해결:

```powershell
py -m mkdocs serve
```

또는 회사 정책상 가능할 때만 실행 정책을 변경합니다.

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

---

### 20.3 `mkdocs.yml`을 찾을 수 없다는 오류

오류 예시:

```text
Config file 'mkdocs.yml' does not exist.
```

원인:

```text
mkdocs.yml 파일이 있는 프로젝트 루트에서 명령어를 실행하지 않음
```

해결:

```powershell
cd C:\Users\User\PEJ\my-docs
dir
```

`mkdocs.yml` 파일이 보이는 위치에서 다시 실행합니다.

```powershell
py -m mkdocs serve
```

---

### 20.4 GitHub Pages 화면이 404로 나오는 경우

확인할 사항:

1. `py -m mkdocs gh-deploy --force`를 실행했는지 확인
2. GitHub 저장소에 `gh-pages` 브랜치가 생성되었는지 확인
3. Repository → Settings → Pages 설정 확인
4. Branch가 `gh-pages`, Folder가 `/ (root)`인지 확인
5. 배포 후 반영까지 몇 분 정도 기다린 뒤 새로고침

---

### 20.5 수정했는데 웹사이트에 반영되지 않는 경우

확인할 사항:

```powershell
git add .
git commit -m "Update documentation"
git push
py -m mkdocs gh-deploy --force
```

그리고 브라우저 캐시 문제일 수 있으므로 강력 새로고침을 합니다.

Windows Chrome / Edge 기준:

```text
Ctrl + F5
```

또는

```text
Ctrl + Shift + R
```

---

### 20.6 GitHub push 권한 오류가 나는 경우

GitHub push 권한이 없거나 인증이 안 된 경우입니다.

확인:

```powershell
git remote -v
```

GitHub 인증이 필요하면 Personal Access Token 또는 GitHub CLI 로그인이 필요할 수 있습니다.

GitHub CLI를 사용하는 경우:

```powershell
gh auth login
```

---

### 20.7 `fatal: remote origin already exists` 오류

이미 원격 저장소가 등록되어 있는 상태입니다.

현재 등록된 원격 저장소를 확인합니다.

```powershell
git remote -v
```

기존 origin을 변경하려면 아래 명령어를 사용합니다.

```powershell
git remote set-url origin https://github.com/<GitHub계정>/<저장소명>.git
```

---

## 21. 팀원에게 공유할 기본 작업 순서

팀원이 문서를 수정할 때는 아래 순서만 기억하면 됩니다.

```powershell
git pull
py -m mkdocs serve
```

문서 수정 후:

```powershell
git add .
git commit -m "Update docs"
git push
py -m mkdocs gh-deploy --force
```

웹 확인:

```text
https://<GitHub계정>.github.io/<저장소명>/
```

---

## 22. Windows 기준 최소 명령어 요약

처음 설치:

```powershell
py -m pip install mkdocs mkdocs-material
py -m mkdocs --version
```

프로젝트 생성:

```powershell
mkdir my-docs
cd my-docs
py -m mkdocs new .
py -m mkdocs serve
```

GitHub 업로드:

```powershell
git init
git add .
git commit -m "Initial MkDocs documentation"
git branch -M main
git remote add origin https://github.com/<GitHub계정>/<저장소명>.git
git push -u origin main
```

Pages 배포:

```powershell
py -m mkdocs gh-deploy --force
```

GitHub Pages 설정:

```text
Repository → Settings → Pages
Source: Deploy from a branch
Branch: gh-pages
Folder: / (root)
```

---

## 23. Windows에서 자주 쓰는 명령어 비교

| 작업 | PowerShell 명령어 |
|---|---|
| 현재 폴더 파일 보기 | `dir` |
| 폴더 이동 | `cd 폴더명` |
| 상위 폴더 이동 | `cd ..` |
| 폴더 생성 | `mkdir 폴더명` |
| 파일 열기 | `notepad 파일명` |
| 현재 위치 확인 | `pwd` |
| 명령어 위치 확인 | `where 명령어` |

예시:

```powershell
where python
where git
where mkdocs
```

---

## 24. 참고 공식 문서

- MkDocs 공식 배포 문서: https://www.mkdocs.org/user-guide/deploying-your-docs/
- Material for MkDocs 배포 문서: https://squidfunk.github.io/mkdocs-material/publishing-your-site/
- GitHub Pages 게시 소스 설정: https://docs.github.com/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

---

## 25. 마무리

MkDocs + GitHub Pages 방식은 프로젝트 문서, 개발 가이드, 설치 가이드, 아키텍처 문서를 팀 단위로 공유하기에 적합합니다.

Windows 환경에서는 핵심적으로 아래 세 가지를 기억하면 됩니다.

```text
1. docs/ 폴더에 마크다운 문서를 작성한다.
2. py -m mkdocs serve로 로컬에서 확인한다.
3. py -m mkdocs gh-deploy --force로 GitHub Pages에 배포한다.
```

특히 Windows에서는 `mkdocs` 명령어가 인식되지 않거나 PowerShell 실행 정책 오류가 날 수 있으므로, 처음에는 `py -m mkdocs` 방식으로 실행하는 것이 가장 안정적입니다.
