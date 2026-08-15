# MkDocs + GitHub Pages 문서 배포 가이드

## 개요

본 문서는 MkDocs와 GitHub Pages를 이용하여 문서를 배포하는 과정과 문서 수정 후 재배포하는 방법을 정리한 가이드이다.

## 문서 수정 후 반영 절차

```text
Markdown 수정
    ↓
Git Push
    ↓
MkDocs Build
    ↓
GitHub Pages 배포
    ↓
웹 페이지 반영
```

---

## 1. 문서 작성

예시

```text
docs/new-document.md
```

---

## 2. mkdocs.yml 메뉴 등록

```yaml
nav:
  - Home: index.md
  - 설치 가이드: install-guide.md
  - 운영 가이드: operation-guide.md
  - 신규 문서: new-document.md
```

---

## 3. GitHub Push

```bash
git add .
git commit -m "신규 문서 추가"
git push origin main
```

---

## 4. 로컬 확인

```bash
mkdocs serve
```

브라우저 접속

```text
http://127.0.0.1:8000
```

---

## 5. GitHub Pages 배포

가장 중요한 명령어

```bash
mkdocs gh-deploy
```

내부 동작

```text
docs/*.md
      ↓
mkdocs build
      ↓
site/*.html
      ↓
gh-pages 브랜치 Push
      ↓
GitHub Pages 반영
```

---

## 6. 정적 사이트 생성만 수행

```bash
mkdocs build
```

생성 결과

```text
site/
├── index.html
├── assets/
└── ...
```

---

## 자주 사용하는 명령어

### 로컬 실행

```bash
mkdocs serve
```

### 정적 사이트 생성

```bash
mkdocs build
```

### GitHub Pages 배포

```bash
mkdocs gh-deploy
```

---

## 가장 많이 사용하는 작업 순서

```bash
git add .
git commit -m "문서 수정"
git push origin main

mkdocs serve

mkdocs gh-deploy
```

---

## 문제 해결

### GitHub에는 있는데 Pages에는 안 보임

원인

- Git Push만 수행함
- GitHub Pages 재배포 안 함

조치

```bash
mkdocs gh-deploy
```

### 메뉴에 안 보임

원인

- mkdocs.yml nav 미등록

조치

```yaml
nav:
  - 신규 문서: new-document.md
```

---

## 결론

문서 수정 후 아래 두 명령어만 기억하면 된다.

```bash
git push origin main
mkdocs gh-deploy
```

