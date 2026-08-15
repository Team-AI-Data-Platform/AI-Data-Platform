# MkDocs + GitHub Pages 문서 사이트 구축 가이드

> 이 문서는 MkDocs로 마크다운 기반 문서 사이트를 만들고, GitHub Pages를 통해 웹에서 확인하는 전체 과정을 정리한 가이드입니다.  
> macOS 기준으로 작성했으며, 팀원이 처음부터 따라 할 수 있도록 설치 → 프로젝트 생성 → 로컬 확인 → GitHub 업로드 → Pages 배포 → 웹 확인 순서로 설명합니다.

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

## 2. 사전 준비사항

아래 프로그램이 필요합니다.

| 항목 | 설명 |
|---|---|
| Python | MkDocs는 Python 기반 도구입니다. |
| pip | Python 패키지 설치 도구입니다. |
| Git | GitHub 저장소에 소스를 올리기 위해 필요합니다. |
| GitHub 계정 | GitHub Pages 사용을 위해 필요합니다. |
| GitHub 저장소 | 문서 사이트를 배포할 Repository입니다. |

설치 여부는 터미널에서 아래 명령어로 확인합니다.

```bash
python3 --version
pip3 --version
git --version
```

예시:

```bash
Python 3.9.6
pip 21.2.4
git version 2.x.x
```

---

## 3. MkDocs 설치

### 3.1 기본 설치

터미널에서 아래 명령어를 실행합니다.

```bash
python3 -m pip install mkdocs mkdocs-material
```

설치가 완료되면 다음 명령어로 확인합니다.

```bash
mkdocs --version
```

정상이라면 아래와 비슷하게 출력됩니다.

```bash
mkdocs, version 1.6.1
```

---

## 4. macOS에서 `mkdocs: command not found`가 나오는 경우

macOS에서 사용자 영역에 Python 패키지가 설치되면 아래와 같은 메시지가 나올 수 있습니다.

```text
WARNING: The script mkdocs is installed in '/Users/사용자명/Library/Python/3.9/bin' which is not on PATH.
```

이 경우 설치는 성공했지만, 터미널이 `mkdocs` 명령어 위치를 찾지 못하는 상태입니다.

### 4.1 PATH 추가

zsh를 사용하는 경우 아래 명령어를 실행합니다.

```bash
echo 'export PATH="$HOME/Library/Python/3.9/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

다시 확인합니다.

```bash
mkdocs --version
```

### 4.2 임시 실행 방법

PATH를 설정하지 않고 바로 실행하려면 아래처럼 전체 경로로 실행할 수도 있습니다.

```bash
~/Library/Python/3.9/bin/mkdocs --version
```

---

## 5. MkDocs 프로젝트 생성

문서 사이트를 만들 폴더로 이동한 뒤 프로젝트를 생성합니다.

```bash
mkdir my-docs
cd my-docs
mkdocs new .
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

## 6. 로컬에서 문서 사이트 실행

아래 명령어를 실행합니다.

```bash
mkdocs serve
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

종료하려면 터미널에서 `Ctrl + C`를 누릅니다.

---

## 7. Material 테마 적용

`mkdocs-material`을 설치했다면 `mkdocs.yml` 파일을 아래처럼 수정합니다.

```yaml
site_name: Project Documentation

theme:
  name: material

nav:
  - Home: index.md
```

다시 실행합니다.

```bash
mkdocs serve
```

화면이 Material 테마로 변경됩니다.

---

## 8. 문서 추가하기

예를 들어 설치 가이드 문서를 추가하려면 아래 파일을 생성합니다.

```text
docs/setup.md
```

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

## 9. 사이트 빌드 확인

로컬 서버 실행 전 또는 배포 전에 빌드가 정상적으로 되는지 확인합니다.

```bash
mkdocs build
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

---

## 10. GitHub 저장소 생성

GitHub에서 새 Repository를 생성합니다.

예시:

```text
Repository name: my-docs
Visibility: Public 또는 Private
```

GitHub Pages 사용 가능 여부는 조직/계정 정책에 따라 다를 수 있습니다.  
일반적으로 Public 저장소에서는 GitHub Pages를 쉽게 사용할 수 있습니다.

---

## 11. 로컬 프로젝트를 GitHub에 업로드

현재 MkDocs 프로젝트 폴더에서 아래 명령어를 실행합니다.

```bash
git init
git add .
git commit -m "Initial MkDocs documentation"
```

GitHub 저장소 주소를 연결합니다.

```bash
git remote add origin https://github.com/<GitHub계정>/<저장소명>.git
```

예시:

```bash
git remote add origin https://github.com/company/my-docs.git
```

기본 브랜치 이름을 `main`으로 맞춥니다.

```bash
git branch -M main
```

GitHub로 push 합니다.

```bash
git push -u origin main
```

---

## 12. GitHub Pages로 배포

MkDocs는 `gh-deploy` 명령어를 제공합니다.

프로젝트 루트, 즉 `mkdocs.yml` 파일이 있는 위치에서 아래 명령어를 실행합니다.

```bash
mkdocs gh-deploy
```

강제로 덮어쓰고 싶다면 아래처럼 실행할 수도 있습니다.

```bash
mkdocs gh-deploy --force
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

## 13. GitHub Pages 설정 확인

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

## 14. 문서 수정 후 다시 배포하는 방법

문서를 수정한 뒤에는 아래 순서로 진행합니다.

### 14.1 로컬에서 확인

```bash
mkdocs serve
```

브라우저에서 확인합니다.

```text
http://127.0.0.1:8000/
```

### 14.2 원본 문서 GitHub 반영

```bash
git add .
git commit -m "Update documentation"
git push
```

### 14.3 GitHub Pages 재배포

```bash
mkdocs gh-deploy --force
```

웹사이트 주소로 접속하여 변경사항을 확인합니다.

---

## 15. 권장 프로젝트 구조

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

## 16. 이미지 넣는 방법

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

## 17. 자주 발생하는 오류와 해결 방법

### 17.1 `mkdocs: command not found`

원인:

```text
MkDocs는 설치되었지만 실행 경로가 PATH에 등록되지 않은 상태
```

해결:

```bash
echo 'export PATH="$HOME/Library/Python/3.9/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
mkdocs --version
```

---

### 17.2 `mkdocs.yml`을 찾을 수 없다는 오류

오류 예시:

```text
Config file 'mkdocs.yml' does not exist.
```

원인:

```text
mkdocs.yml 파일이 있는 프로젝트 루트에서 명령어를 실행하지 않음
```

해결:

```bash
cd my-docs
ls
```

`mkdocs.yml` 파일이 보이는 위치에서 다시 실행합니다.

```bash
mkdocs serve
```

---

### 17.3 GitHub Pages 화면이 404로 나오는 경우

확인할 사항:

1. `mkdocs gh-deploy --force`를 실행했는지 확인
2. GitHub 저장소에 `gh-pages` 브랜치가 생성되었는지 확인
3. Repository → Settings → Pages 설정 확인
4. Branch가 `gh-pages`, Folder가 `/ (root)`인지 확인
5. 배포 후 반영까지 몇 분 정도 기다린 뒤 새로고침

---

### 17.4 수정했는데 웹사이트에 반영되지 않는 경우

확인할 사항:

```bash
git add .
git commit -m "Update documentation"
git push
mkdocs gh-deploy --force
```

그리고 브라우저 캐시 문제일 수 있으므로 강력 새로고침을 합니다.

macOS Chrome 기준:

```text
Cmd + Shift + R
```

---

### 17.5 권한 오류가 나는 경우

GitHub push 권한이 없거나 인증이 안 된 경우입니다.

확인:

```bash
git remote -v
```

GitHub 인증이 필요하면 Personal Access Token 또는 GitHub CLI 로그인이 필요할 수 있습니다.

GitHub CLI 사용 시:

```bash
gh auth login
```

---

## 18. 팀원에게 공유할 기본 작업 순서

팀원이 문서를 수정할 때는 아래 순서만 기억하면 됩니다.

```bash
git pull
mkdocs serve
```

문서 수정 후:

```bash
git add .
git commit -m "Update docs"
git push
mkdocs gh-deploy --force
```

웹 확인:

```text
https://<GitHub계정>.github.io/<저장소명>/
```

---

## 19. 최소 명령어 요약

처음 설치:

```bash
python3 -m pip install mkdocs mkdocs-material
echo 'export PATH="$HOME/Library/Python/3.9/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
mkdocs --version
```

프로젝트 생성:

```bash
mkdir my-docs
cd my-docs
mkdocs new .
mkdocs serve
```

GitHub 업로드:

```bash
git init
git add .
git commit -m "Initial MkDocs documentation"
git branch -M main
git remote add origin https://github.com/<GitHub계정>/<저장소명>.git
git push -u origin main
```

Pages 배포:

```bash
mkdocs gh-deploy --force
```

GitHub Pages 설정:

```text
Repository → Settings → Pages
Source: Deploy from a branch
Branch: gh-pages
Folder: / (root)
```

---

## 20. 참고 공식 문서

- MkDocs 공식 배포 문서: https://www.mkdocs.org/user-guide/deploying-your-docs/
- Material for MkDocs 배포 문서: https://squidfunk.github.io/mkdocs-material/publishing-your-site/
- GitHub Pages 게시 소스 설정: https://docs.github.com/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

---

## 21. 마무리

MkDocs + GitHub Pages 방식은 프로젝트 문서, 개발 가이드, 설치 가이드, 아키텍처 문서를 팀 단위로 공유하기에 적합합니다.

핵심은 아래 세 가지입니다.

```text
1. docs/ 폴더에 마크다운 문서를 작성한다.
2. mkdocs serve로 로컬에서 확인한다.
3. mkdocs gh-deploy --force로 GitHub Pages에 배포한다.
```

이 흐름만 익히면 GitHub 저장소를 기반으로 웹 문서 사이트를 쉽게 운영할 수 있습니다.
