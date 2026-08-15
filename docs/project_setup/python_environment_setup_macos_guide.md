# Python 설치 및 환경 설정 가이드 - macOS

> AI-Data-Platform 프로젝트를 macOS 환경에서 사용하기 위해 Python을 설치하거나 확인하고, pip와 프로젝트 전용 가상환경(`.venv`)을 구성하는 가이드

---

## 1. 문서 작성 목적

이 문서는 **macOS에서 AI-Data-Platform 프로젝트를 처음 시작하거나 새로운 Mac에서 개발 환경을 구성하는 사용자**를 대상으로 Python 설치와 기본 환경 설정 방법을 설명한다.

AI-Data-Platform 프로젝트의 RAG, Local LLM 연계, AI Agent 등 여러 실습은 Python을 기반으로 작성되어 있다.

따라서 프로젝트 실습을 진행하기 전에 다음과 같은 Python 실행 환경을 준비해야 한다.

```text
Python 설치 여부 확인
      ↓
필요 시 Python 설치
      ↓
Python 실행 확인
      ↓
pip 확인
      ↓
프로젝트 디렉터리 이동
      ↓
프로젝트 가상환경(.venv) 생성
      ↓
가상환경 활성화
      ↓
pip 업데이트
      ↓
프로젝트별 Python 패키지 설치 준비 완료
```

이 문서에서는 **macOS에서 Python을 설치하고 프로젝트별 Python 실행 환경을 준비하는 단계까지** 다룬다.

MkDocs, Ollama, LangChain, LangGraph, ChromaDB 등의 프로그램이나 Python 패키지는 해당 기능별 가이드에서 별도로 설치한다.

---

## 2. Python 환경을 별도로 구성하는 이유

Mac에 Python만 설치하면 Python 코드를 실행할 수 있다.

하지만 AI-Data-Platform 프로젝트에서는 Python 패키지를 Mac 전체에 바로 설치하기보다 **프로젝트 전용 가상환경을 만들어 사용하는 방식**을 권장한다.

전체 구조를 단순화하면 다음과 같다.

```text
macOS
│
├─ Python 3
│
└─ AI-Data-Platform
    │
    ├─ .venv
    │   └─ 프로젝트 전용 Python 환경
    │
    ├─ docs
    ├─ labs
    ├─ mkdocs.yml
    └─ ...
```

가상환경을 사용하면 프로젝트별로 Python 패키지와 버전을 분리하여 관리할 수 있다.

예를 들어 다른 Python 프로젝트에서 사용하는 패키지 버전과 AI-Data-Platform에서 사용하는 패키지 버전이 달라도 서로 영향을 최소화할 수 있다.

---

## 3. macOS Python 환경 구성 전체 흐름

새로운 Mac에서 권장하는 Python 환경 구성 순서는 다음과 같다.

```text
1. 기존 Python 설치 여부 확인
        ↓
2. 사용 중인 Python 위치 확인
        ↓
3. 필요 시 Python 설치
        ↓
4. Terminal 다시 실행
        ↓
5. Python 버전 확인
        ↓
6. pip 확인
        ↓
7. AI-Data-Platform 프로젝트 폴더 이동
        ↓
8. .venv 가상환경 생성
        ↓
9. 가상환경 활성화
        ↓
10. 가상환경의 Python 사용 여부 확인
        ↓
11. pip 업데이트
        ↓
12. 프로젝트 Python 환경 구성 완료
```

---

## 4. Python이 이미 설치되어 있는지 먼저 확인

Python을 새로 설치하기 전에 기존 설치 여부를 먼저 확인한다.

macOS의 **Terminal**을 실행하고 다음 명령을 입력한다.

```bash
python3 --version
```

정상적으로 Python 3가 설치되어 있다면 다음과 비슷한 결과가 출력된다.

```text
Python 3.14.x
```

버전 번호는 설치 시점과 프로젝트 환경에 따라 달라질 수 있다.

### Python이 정상적으로 설치된 경우

Python 버전이 정상적으로 출력되더라도 바로 해당 Python을 프로젝트에 사용하는 것보다 **어떤 위치의 Python이 실행되고 있는지 함께 확인**하는 것이 좋다.

```bash
which python3
```

예를 들어 다음과 같은 경로가 표시될 수 있다.

```text
/usr/local/bin/python3
```

또는 Homebrew 환경에서는 Apple Silicon과 Intel Mac에 따라 다음과 같은 경로가 사용될 수 있다.

```text
/opt/homebrew/bin/python3
/usr/local/bin/python3
```

### Python을 찾을 수 없는 경우

다음과 비슷한 메시지가 표시된다면 Python 3가 설치되어 있지 않거나 현재 Shell의 `PATH`에서 Python을 찾지 못하는 상태일 수 있다.

```text
zsh: command not found: python3
```

이 경우 다음 절의 설치 방법을 진행한다.

---

## 5. macOS에 포함된 Python과 프로젝트용 Python 구분

macOS 환경에서는 `python3` 명령이 이미 존재하는 경우가 있다.

특히 Xcode 또는 Xcode Command Line Tools가 설치된 Mac에서는 Apple이 관리하는 Python이 `/usr/bin/python3`에 존재할 수 있다.

```bash
which python3
```

결과가 다음과 같을 수 있다.

```text
/usr/bin/python3
```

이 Python은 Apple 개발 도구나 macOS 구성요소가 사용할 수 있는 **Apple 관리 영역의 Python**이다.

따라서 다음과 같은 방식으로 직접 수정하거나 삭제하지 않는다.

```text
/usr/bin/python3 직접 삭제
시스템 Python 파일 변경
시스템 관리 영역에 패키지 강제 설치
```

AI-Data-Platform 프로젝트에서는 별도로 설치한 Python을 사용하고, 그 Python을 기반으로 프로젝트 전용 `.venv` 가상환경을 생성하는 방식을 권장한다.

---

## 6. macOS에서 Python을 설치하는 방법

macOS에서 Python을 설치하는 대표적인 방법은 다음과 같다.

```text
방법 1. python.org 공식 macOS Installer 사용
방법 2. Homebrew를 이용한 설치
```

이 가이드에서는 처음 Python 환경을 구성하는 사용자가 설치 과정을 명확하게 확인할 수 있도록 **python.org 공식 Installer 방식을 기본 절차**로 설명한다.

이미 Homebrew를 개발 도구 관리에 사용하고 있는 경우에는 뒤쪽의 **Homebrew를 이용한 Python 설치** 절을 참고할 수 있다.

---

## 7. Python 버전 선택 기준

Python은 최신 버전만 선택하기보다 **프로젝트에서 사용하는 버전과의 호환성**을 먼저 고려해야 한다.

예를 들어 팀에서 Python 3.14 계열을 기준으로 실습하고 있다면 macOS에서도 동일한 계열을 사용하는 것이 Windows와 macOS 간 환경 차이를 줄이는 데 도움이 된다.

```text
팀 기준 Python 버전 확인
        ↓
동일한 Python 계열 설치
        ↓
프로젝트별 .venv 생성
```

다음과 같은 AI 관련 라이브러리는 최신 Python 버전 지원 시점이 서로 다를 수 있다.

```text
PyTorch
sentence-transformers
ChromaDB
LangChain
LangGraph
문서 처리 라이브러리
기타 AI / ML 패키지
```

따라서 프로젝트에 다음 파일 또는 별도의 버전 정책이 있다면 **프로젝트에서 지정한 Python 버전을 우선**한다.

```text
requirements.txt
pyproject.toml
.python-version
프로젝트 환경 구성 문서
```

---

## 8. 방법 1 - python.org 공식 Installer로 Python 설치

Python 공식 사이트에서는 macOS용 설치 패키지(`.pkg`)를 제공한다.

현재 공식 macOS Installer는 지원되는 Apple Silicon Mac과 Intel Mac에서 사용할 수 있는 `universal2` 빌드를 제공한다.

설치 흐름은 다음과 같다.

```text
Python 공식 다운로드 페이지 접속
        ↓
macOS용 Installer 다운로드
        ↓
.pkg 파일 실행
        ↓
설치 안내에 따라 진행
        ↓
설치 완료
        ↓
Install Certificates.command 실행
        ↓
Terminal 다시 실행
        ↓
python3 --version 확인
```

---

## 9. Python Installer 실행

다운로드한 macOS용 Python 설치 파일은 일반적으로 `.pkg` 형식이다.

설치 파일을 실행하고 macOS Installer의 안내에 따라 진행한다.

일반적인 순서는 다음과 같다.

```text
Introduction
    ↓
Read Me
    ↓
License
    ↓
Installation Type
    ↓
Install
    ↓
Summary
```

일반적인 프로젝트 개발 환경이라면 기본 설치 옵션을 사용하면 된다.

설치 과정에서 macOS 관리자 권한을 요구할 수 있다.

> Python Installer의 화면 구성과 Python 버전 번호는 설치 시점에 따라 달라질 수 있다.

---

## 10. Free-threaded Python 옵션은 기본적으로 사용하지 않는다

최근 Python의 macOS Installer에는 선택적으로 **Free-threaded Python**을 추가 설치할 수 있는 옵션이 제공될 수 있다.

이는 GIL(Global Interpreter Lock)을 사용하지 않는 별도의 Python 빌드를 실험하거나 활용하기 위한 기능이다.

AI-Data-Platform의 기본 학습 및 실습 환경에서는 특별한 목적이 없다면 이 옵션을 추가로 선택하지 않고 **기본 Python 빌드**를 사용한다.

이유는 다음과 같다.

```text
기본 Python 환경과의 차이를 줄임
서드파티 패키지 호환성 문제 가능성 최소화
팀원 간 실행 환경 통일
초기 학습 환경의 복잡성 감소
```

---

## 11. Install Certificates.command 실행

python.org의 macOS Installer로 Python을 설치한 경우 설치 완료 후 `/Applications` 아래에 Python 버전별 디렉터리가 생성된다.

예를 들어 Python 3.14 계열을 설치했다면 다음과 비슷한 위치를 확인할 수 있다.

```text
/Applications/Python 3.14/
```

여기에는 다음과 같은 파일이 포함될 수 있다.

```text
IDLE
Python Launcher
Install Certificates.command
...
```

Python 공식 문서에서는 macOS Installer 설치 후 다음 파일을 실행하여 SSL 인증서 구성을 완료하도록 안내한다.

```text
Install Certificates.command
```

Finder에서 다음 순서로 실행한다.

```text
응용 프로그램(Applications)
        ↓
Python 3.x
        ↓
Install Certificates.command 더블 클릭
```

실행하면 Terminal 창이 열리고 Python에서 사용할 SSL Root Certificate 구성이 진행된다.

정상적으로 완료되면 다음과 비슷한 메시지를 확인할 수 있다.

```text
Successfully installed certifi
update complete
```

이 단계는 향후 `pip`를 이용하여 HTTPS 기반으로 Python 패키지를 내려받을 때 인증서 관련 문제를 줄이는 데 도움이 된다.

---

## 12. Python 설치 후 Terminal 다시 실행

Python 설치가 완료된 후 기존에 열려 있던 Terminal에서는 새로운 `PATH` 설정이 바로 반영되지 않을 수 있다.

따라서 설치 후에는 다음 순서로 확인하는 것을 권장한다.

```text
1. 기존 Terminal 종료
2. Terminal 새로 실행
3. python3 --version 확인
4. which python3 확인
5. pip 확인
```

---

## 13. Python 설치 확인

새 Terminal을 열고 다음 명령을 실행한다.

```bash
python3 --version
```

정상 예:

```text
Python 3.14.x
```

설치된 Python의 정확한 버전을 조금 더 자세하게 확인하려면 다음 명령도 사용할 수 있다.

```bash
python3 -VV
```

---

## 14. 실제 사용 중인 Python 위치 확인

macOS에서는 여러 Python이 함께 존재할 수 있으므로 어떤 Python이 실행되는지 확인하는 것이 중요하다.

다음 명령을 실행한다.

```bash
which python3
```

python.org Installer로 설치한 Python이 우선 사용되는 환경에서는 다음과 비슷한 경로가 표시될 수 있다.

```text
/usr/local/bin/python3
```

반면 다음과 같이 표시된다면 Apple이 관리하는 Python일 수 있다.

```text
/usr/bin/python3
```

여러 Python이 설치되어 있어 혼동될 경우 다음 명령으로 Shell에서 인식하는 후보를 확인할 수도 있다.

```bash
type -a python3
```

예:

```text
python3 is /usr/local/bin/python3
python3 is /usr/bin/python3
```

위에서 먼저 표시되는 Python이 일반적으로 현재 Shell에서 우선 실행된다.

---

## 15. macOS에서는 기본적으로 `python3` 명령을 사용한다

macOS에서 가상환경을 만들기 전에는 다음 명령을 기준으로 사용하는 것을 권장한다.

```bash
python3
python3 -m pip
python3 -m venv
```

다음 명령은 환경에 따라 존재하지 않을 수도 있다.

```bash
python
```

따라서 프로젝트 가상환경을 **생성하기 전**에는 명확하게 `python3`를 사용한다.

```bash
python3 --version
```

다만 `.venv` 가상환경을 활성화한 뒤에는 가상환경 내부의 `python` 명령을 사용할 수 있다.

```text
가상환경 활성화 전
python3

가상환경 활성화 후
python
또는
python3
```

---

## 16. pip란?

`pip`는 Python 패키지를 설치하고 관리하는 도구이다.

예를 들어 다음과 같은 Python 라이브러리를 설치할 때 사용한다.

```text
requests
pypdf
python-docx
openpyxl
chromadb
langchain
langgraph
```

python.org의 macOS Installer에는 일반적으로 pip가 함께 포함된다.

---

## 17. pip 설치 여부 확인

가상환경을 생성하기 전에 Python과 연결된 pip가 정상적인지 확인한다.

```bash
python3 -m pip --version
```

정상적으로 설치되어 있다면 다음과 비슷한 결과가 출력된다.

```text
pip 26.x from .../site-packages/pip (python 3.14)
```

### 왜 `pip3 --version`보다 `python3 -m pip --version`을 권장하는가?

다음과 같이 직접 `pip3` 명령을 사용할 수도 있다.

```bash
pip3 --version
```

하지만 Mac에 여러 Python이 설치되어 있다면 `pip3`가 어떤 Python에 연결되어 있는지 혼동될 수 있다.

반면 다음 명령은:

```bash
python3 -m pip
```

현재 `python3` 명령으로 실행되는 Python 인터프리터의 pip를 사용한다.

따라서 프로젝트 환경을 구성할 때는 다음 형식을 사용하는 것을 권장한다.

```bash
python3 -m pip <명령>
```

---

## 18. AI-Data-Platform 프로젝트 디렉터리로 이동

Python과 pip가 정상적으로 확인되었다면 프로젝트 루트 디렉터리로 이동한다.

예를 들어 프로젝트를 다음 위치에 Clone했다고 가정한다.

```text
~/projects/AI-Data-Platform
```

Terminal에서 다음 명령을 실행한다.

```bash
cd ~/projects/AI-Data-Platform
```

현재 위치는 다음 명령으로 확인할 수 있다.

```bash
pwd
```

파일과 디렉터리 목록을 확인하려면 다음 명령을 사용한다.

```bash
ls
```

프로젝트 루트에는 일반적으로 다음과 같은 파일과 디렉터리가 있다.

```text
AI-Data-Platform
│
├─ docs
├─ labs
├─ mkdocs.yml
├─ README.md
└─ ...
```

---

## 19. Python 가상환경이란?

Python 가상환경(Virtual Environment)은 **특정 프로젝트에서 사용하는 Python과 패키지를 별도의 공간에 분리하여 관리하기 위한 환경**이다.

AI-Data-Platform 프로젝트에서는 `.venv`라는 이름으로 가상환경을 생성하는 것을 권장한다.

```text
AI-Data-Platform
│
├─ .venv
│   ├─ bin
│   ├─ lib
│   └─ ...
│
├─ docs
├─ labs
└─ ...
```

가상환경을 사용하면 다음과 같은 장점이 있다.

```text
1. 프로젝트마다 서로 다른 패키지 버전을 사용할 수 있다.
2. 다른 Python 프로젝트와의 라이브러리 충돌을 줄일 수 있다.
3. Mac 전체의 Python 환경을 불필요하게 변경하지 않는다.
4. 프로젝트를 새로운 PC에서 다시 구성하기 쉽다.
5. 문제가 생겼을 때 .venv를 삭제하고 다시 생성할 수 있다.
```

---

## 20. `.venv`라는 이름을 사용하는 이유

가상환경 디렉터리 이름은 반드시 `.venv`여야 하는 것은 아니다.

다음과 같은 이름도 사용할 수 있다.

```text
venv
env
myenv
```

하지만 AI-Data-Platform 프로젝트에서는 다음 이름을 사용하는 것을 권장한다.

```text
.venv
```

이유는 다음과 같다.

```text
프로젝트 가상환경임을 쉽게 알 수 있음
IDE에서 자동으로 인식하기 쉬움
Git 저장소에서 제외하기 쉬움
Windows와 macOS에서 동일한 가상환경 디렉터리 이름 사용 가능
팀원 간 동일한 명명 규칙 사용 가능
```

---

## 21. Windows와 macOS의 `.venv`는 서로 다르다

가상환경은 운영체제와 Python 설치 환경에 의존한다.

따라서 Windows에서 생성한 `.venv`를 macOS로 복사하거나, macOS에서 생성한 `.venv`를 Windows에서 그대로 사용하면 안 된다.

대표적으로 가상환경 실행 파일의 디렉터리 구조부터 다르다.

Windows:

```text
.venv/
└─ Scripts/
```

macOS:

```text
.venv/
└─ bin/
```

따라서 프로젝트 Repository를 새로운 PC에 Clone한 경우 해당 PC에서 가상환경을 새로 생성한다.

```text
Repository Clone
      ↓
해당 PC에서 Python 확인
      ↓
해당 PC에서 .venv 새로 생성
      ↓
프로젝트 패키지 재설치
```

`.venv` 디렉터리 자체를 GitHub에 올려서 공유하지 않는다.

---

## 22. 가상환경 생성

AI-Data-Platform 프로젝트 루트에서 다음 명령을 실행한다.

```bash
python3 -m venv .venv
```

명령을 분해하면 다음과 같다.

```text
python3
→ Python 3 실행

-m
→ Python 모듈을 실행

venv
→ Python 표준 가상환경 모듈

.venv
→ 생성할 가상환경 디렉터리 이름
```

즉 다음 명령은:

```bash
python3 -m venv .venv
```

**현재 `python3`를 이용하여 `.venv`라는 프로젝트 전용 가상환경을 생성한다**는 의미이다.

> 가상환경 생성은 프로젝트 환경을 처음 구성할 때 한 번만 수행한다. Terminal을 새로 실행할 때마다 `.venv`를 다시 생성하는 것이 아니다.

---

## 23. 가상환경 생성 확인

명령 실행 후 다음 명령으로 프로젝트 디렉터리를 확인한다.

```bash
ls -a
```

`-a` 옵션을 사용하는 이유는 `.venv`처럼 이름이 `.`으로 시작하는 디렉터리는 일반 `ls` 명령에서 보이지 않을 수 있기 때문이다.

다음과 같이 `.venv` 디렉터리가 생성되어 있으면 정상이다.

```text
.
..
.venv
docs
labs
mkdocs.yml
README.md
...
```

macOS의 `.venv` 내부에는 일반적으로 다음과 같은 구조가 생성된다.

```text
.venv
│
├─ bin
├─ include
├─ lib
└─ pyvenv.cfg
```

가상환경 실행과 관련된 주요 파일은 `bin` 디렉터리에 있다.

---

## 24. Terminal에서 가상환경 활성화

macOS의 Terminal에서는 다음 명령으로 가상환경을 활성화한다.

```bash
source .venv/bin/activate
```

성공하면 Terminal 프롬프트 앞에 일반적으로 다음과 같이 가상환경 이름이 표시된다.

```text
(.venv) user@Mac AI-Data-Platform %
```

앞의:

```text
(.venv)
```

는 **현재 Terminal 세션이 `.venv` 가상환경을 사용하고 있다는 의미**이다.

> `.venv`는 최초 1회만 생성한다. 이후 Terminal을 새로 실행할 때는 가상환경을 다시 생성하지 않고 `source .venv/bin/activate` 명령으로 **활성화만 다시 수행**한다.

---

## 25. `source .venv/bin/activate`의 의미

가상환경 활성화 명령을 나누어 보면 다음과 같다.

```bash
source .venv/bin/activate
```

각 부분의 의미는 다음과 같다.

```text
source
→ 현재 Shell에서 지정한 스크립트의 내용을 실행

.venv/bin/activate
→ .venv 가상환경의 활성화 스크립트
```

가상환경 활성화는 별도의 프로그램을 새로 실행하는 것이 아니라 **현재 Terminal 세션의 환경변수와 PATH를 가상환경 기준으로 변경하는 작업**이다.

---

## 26. 가상환경 활성화가 의미하는 것

가상환경을 활성화하면 현재 Terminal 세션에서 `python`과 `pip` 명령이 프로젝트의 `.venv` 안에 있는 실행 파일을 우선 사용하도록 `PATH`가 변경된다.

개념적으로 다음과 같다.

```text
가상환경 활성화 전

python3
   ↓
Mac에 설치된 Python


가상환경 활성화 후

python
   ↓
AI-Data-Platform/.venv/bin/python
```

따라서 가상환경이 활성화된 상태에서 설치한 Python 패키지는 시스템 전체가 아니라 해당 프로젝트의 `.venv` 내부에 설치된다.

---

## 27. 실제 사용 중인 Python 확인

가상환경을 활성화한 뒤 다음 명령을 실행한다.

```bash
which python
```

정상적으로 `.venv`가 활성화되어 있다면 결과 경로에 프로젝트의 `.venv/bin/python`이 포함된다.

예:

```text
/Users/user/projects/AI-Data-Platform/.venv/bin/python
```

Python 버전도 확인한다.

```bash
python --version
```

예:

```text
Python 3.14.x
```

필요하면 `python3` 위치도 함께 확인할 수 있다.

```bash
which python3
```

가상환경이 정상적으로 활성화되었다면 이 경로 역시 `.venv`를 가리키는 것이 일반적이다.

---

## 28. 가상환경에서 pip 확인

가상환경이 활성화된 상태에서 다음 명령을 실행한다.

```bash
python -m pip --version
```

결과 경로에 `.venv`가 포함되어 있으면 정상이다.

예:

```text
pip 26.x from .../AI-Data-Platform/.venv/lib/python3.14/site-packages/pip (python 3.14)
```

여기서 중요한 점은 다음과 같다.

```text
가상환경 활성화 전 pip
→ Mac의 기본 Python 환경과 연결될 수 있음

가상환경 활성화 후 pip
→ AI-Data-Platform/.venv에 연결
```

따라서 프로젝트 패키지는 반드시 가상환경을 활성화한 뒤 설치하는 습관을 갖는 것이 좋다.

---

## 29. pip 업데이트

가상환경을 활성화한 상태에서 pip를 업데이트한다.

```bash
python -m pip install --upgrade pip
```

업데이트 후 버전을 확인한다.

```bash
python -m pip --version
```

정상적으로 `.venv` 내부 경로가 표시되는지 함께 확인한다.

---

## 30. Python 패키지는 가상환경에 설치한다

AI-Data-Platform 프로젝트에서 사용하는 Python 패키지는 시스템 전체가 아니라 프로젝트의 `.venv`에 설치한다.

예를 들어 `requests` 패키지를 설치한다면 다음과 같이 진행한다.

```bash
source .venv/bin/activate
```

```bash
python -m pip install requests
```

개념적으로는 다음과 같다.

```text
AI-Data-Platform
│
└─ .venv
    │
    └─ lib
        └─ python3.x
            └─ site-packages
                └─ requests
```

이렇게 하면 다른 프로젝트의 Python 패키지와 충돌하는 문제를 줄일 수 있다.

---

## 31. requirements.txt가 있는 경우

프로젝트에 `requirements.txt`가 있다면 가상환경 활성화 후 다음 명령으로 필요한 패키지를 설치할 수 있다.

```bash
python -m pip install -r requirements.txt
```

일반적인 순서는 다음과 같다.

```text
프로젝트 이동
      ↓
가상환경 활성화
      ↓
pip 업데이트
      ↓
requirements.txt 기반 패키지 설치
```

명령으로 표현하면 다음과 같다.

```bash
cd ~/projects/AI-Data-Platform
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

다만 AI-Data-Platform 프로젝트에서 기능별로 별도의 requirements 파일을 사용하는 경우에는 해당 실습 가이드의 설치 명령을 우선한다.

---

## 32. 가상환경 비활성화

가상환경 사용을 종료하려면 다음 명령을 실행한다.

```bash
deactivate
```

실행하면 Terminal 프롬프트 앞의 `(.venv)` 표시가 사라진다.

예:

```text
가상환경 활성화
(.venv) user@Mac AI-Data-Platform %

        ↓ deactivate

가상환경 비활성화
user@Mac AI-Data-Platform %
```

Terminal 창을 종료해도 현재 Terminal 세션의 가상환경 활성화 상태는 함께 종료된다.

---

## 33. Terminal을 새로 열었을 때

Terminal을 종료했다가 새로 열면 가상환경은 자동으로 활성화되지 않는다.

하지만 `.venv` 디렉터리가 삭제되는 것은 아니다.

따라서 **가상환경을 다시 생성할 필요가 없다.**

프로젝트 작업을 다시 시작할 때 다음 명령만 실행한다.

```bash
cd ~/projects/AI-Data-Platform
```

```bash
source .venv/bin/activate
```

정리하면 다음과 같다.

```text
최초 환경 구성

Python 설치
    ↓
.venv 생성
    ↓
.venv 활성화


다음 작업부터

Terminal 실행
    ↓
프로젝트 폴더 이동
    ↓
.venv 활성화
```

---

## 34. `.venv`를 GitHub에 올리지 않는다

`.venv`는 각 개발자의 PC에서 생성하는 로컬 실행 환경이다.

따라서 Git Repository에 Commit하거나 GitHub에 Push하지 않는다.

프로젝트의 `.gitignore`에 다음 항목이 포함되어 있는지 확인한다.

```gitignore
.venv/
```

확인 명령:

```bash
grep -n "\.venv" .gitignore
```

또는 `.gitignore` 파일을 직접 열어 확인할 수 있다.

가상환경 자체는 공유하지 않고, 필요한 패키지 정보만 다음과 같은 파일을 이용하여 공유한다.

```text
requirements.txt
pyproject.toml
기타 프로젝트 의존성 관리 파일
```

---

## 35. 방법 2 - Homebrew로 Python 설치

이미 Homebrew를 사용하고 있는 Mac이라면 Homebrew를 이용해 Python을 설치할 수도 있다.

먼저 Homebrew 설치 여부를 확인한다.

```bash
brew --version
```

정상적으로 버전이 출력된다면 Python을 설치한다.

```bash
brew install python
```

특정 Python 계열이 필요한 경우 Homebrew Formula를 확인한 뒤 버전을 지정하여 설치할 수도 있다.

예:

```bash
brew install python@3.14
```

설치가 완료되면 다음 명령으로 확인한다.

```bash
python3 --version
```

그리고 실제 실행 경로를 확인한다.

```bash
which python3
```

> 팀 프로젝트에서는 개인별로 임의의 Python 버전을 선택하기보다 프로젝트에서 정한 버전 정책을 우선한다.

---

## 36. Apple Silicon과 Intel Mac의 Homebrew 경로 차이

Homebrew의 기본 설치 위치는 Mac의 CPU 아키텍처에 따라 다를 수 있다.

대표적인 경로는 다음과 같다.

```text
Apple Silicon Mac
/opt/homebrew

Intel Mac
/usr/local
```

현재 Mac의 CPU 아키텍처는 다음 명령으로 확인할 수 있다.

```bash
uname -m
```

Apple Silicon Mac에서는 일반적으로 다음과 같이 표시된다.

```text
arm64
```

Intel Mac에서는 일반적으로 다음과 같이 표시된다.

```text
x86_64
```

Homebrew가 설치되어 있는데 `brew` 명령을 찾지 못하는 경우에는 Homebrew 설치 위치와 Shell의 `PATH` 설정을 확인한다.

---

## 37. Homebrew Python과 가상환경 사용

Homebrew로 설치한 Python도 프로젝트에서는 동일하게 `.venv`를 생성하여 사용한다.

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

Homebrew의 최근 Python은 시스템 또는 패키지 관리자가 관리하는 Python 환경을 보호하기 위해 전역 `pip install`을 제한할 수 있다.

이때 다음과 같은 오류 문구가 나타날 수 있다.

```text
externally-managed-environment
```

이 경우 시스템 Python 환경에 강제로 패키지를 설치하지 말고 프로젝트 전용 가상환경을 생성하고 활성화한 뒤 패키지를 설치한다.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install <package-name>
```

AI-Data-Platform에서는 처음부터 `.venv` 사용을 기본 원칙으로 하므로 이러한 문제를 예방하는 데도 도움이 된다.

---

## 38. `python3`는 되는데 `python`은 실행되지 않는 경우

가상환경을 활성화하기 전 macOS Terminal에서 다음 명령이 실패할 수 있다.

```bash
python --version
```

예:

```text
zsh: command not found: python
```

하지만 다음 명령은 정상적으로 실행될 수 있다.

```bash
python3 --version
```

이것은 반드시 오류라고 볼 수 없다.

macOS에서는 가상환경 생성 전 다음 명령을 기준으로 사용한다.

```bash
python3
```

가상환경을 활성화한 후에는 다음 명령으로 확인한다.

```bash
python --version
```

---

## 39. `python3`가 예상한 버전이 아닌 경우

Python을 새로 설치했는데도 다음 명령의 결과가 예상한 버전과 다를 수 있다.

```bash
python3 --version
```

먼저 실제 실행 경로를 확인한다.

```bash
which python3
```

추가로 다음 명령을 실행한다.

```bash
type -a python3
```

여러 Python 경로가 표시된다면 Shell의 `PATH` 순서에 따라 먼저 발견되는 Python이 실행된다.

예:

```text
python3 is /usr/local/bin/python3
python3 is /usr/bin/python3
```

python.org Installer를 사용한 경우 기본 설치 과정에서 새 Python의 실행 경로가 Shell `PATH`에서 우선되도록 구성되지만, 기존 Shell 설정이나 다른 Python 관리 도구를 사용하고 있다면 경로가 달라질 수 있다.

이 경우 임의로 `/usr/bin/python3`를 삭제하거나 수정하지 않는다.

---

## 40. 가상환경이 활성화되지 않는 경우

다음 명령을 실행했는데 오류가 발생한다면:

```bash
source .venv/bin/activate
```

먼저 현재 위치를 확인한다.

```bash
pwd
```

그리고 `.venv`가 실제로 존재하는지 확인한다.

```bash
ls -a
```

`.venv`가 없다면 프로젝트 최초 구성 시 다음 명령으로 생성한다.

```bash
python3 -m venv .venv
```

이미 `.venv`가 존재한다면 다시 생성할 필요는 없다.

또한 Windows용 활성화 명령과 혼동하지 않도록 주의한다.

Windows PowerShell:

```text
.\.venv\Scripts\Activate.ps1
```

macOS Terminal:

```text
source .venv/bin/activate
```

---

## 41. pip 설치 시 권한 오류가 발생하는 경우

가상환경을 사용하지 않고 Mac 전체 Python 환경에 패키지를 설치하려고 하면 권한 또는 관리 환경 관련 오류가 발생할 수 있다.

이 문제를 해결하기 위해 다음과 같이 `sudo pip` 또는 `sudo pip3`를 습관적으로 사용하는 것은 권장하지 않는다.

```bash
sudo pip3 install <package-name>
```

AI-Data-Platform 프로젝트에서는 다음 순서로 해결한다.

```bash
cd ~/projects/AI-Data-Platform
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

그 뒤 필요한 패키지를 설치한다.

```bash
python -m pip install <package-name>
```

즉 **권한을 높여 시스템 환경에 설치하는 것이 아니라 프로젝트 가상환경에 설치**하는 방식으로 관리한다.

---

## 42. Python 환경 최종 확인

환경 구성이 끝나면 다음 순서로 최종 확인한다.

### 42.1 프로젝트 위치 확인

```bash
pwd
```

### 42.2 가상환경 활성화

```bash
source .venv/bin/activate
```

### 42.3 Python 위치 확인

```bash
which python
```

정상 예:

```text
.../AI-Data-Platform/.venv/bin/python
```

### 42.4 Python 버전 확인

```bash
python --version
```

### 42.5 pip 위치와 버전 확인

```bash
python -m pip --version
```

출력 경로에 `.venv`가 포함되어 있으면 프로젝트 전용 Python 환경을 사용하고 있는 것이다.

---

## 43. 환경 구성 완료 기준

다음 항목이 모두 정상이라면 macOS의 Python 기본 환경 구성이 완료된 것이다.

```text
[ ] python3 --version이 정상적으로 출력된다.
[ ] 프로젝트에서 사용할 Python 버전이 적절하다.
[ ] which python3로 설치 위치를 확인했다.
[ ] python3 -m pip --version이 정상적으로 출력된다.
[ ] AI-Data-Platform 프로젝트 루트로 이동할 수 있다.
[ ] .venv 가상환경을 생성했다.
[ ] source .venv/bin/activate로 활성화할 수 있다.
[ ] 활성화 후 프롬프트에 (.venv)가 표시된다.
[ ] which python 결과가 .venv/bin/python을 가리킨다.
[ ] python -m pip --version 경로에 .venv가 포함된다.
[ ] .venv/가 .gitignore에 포함되어 있다.
```

---

## 44. 최초 구성과 이후 사용 순서 정리

### 최초 1회 환경 구성

```bash
python3 --version
which python3
python3 -m pip --version

cd ~/projects/AI-Data-Platform
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### 이후 프로젝트 작업을 시작할 때

```bash
cd ~/projects/AI-Data-Platform
source .venv/bin/activate
```

필요하면 다음 명령으로 정상 활성화 여부를 확인한다.

```bash
which python
python --version
python -m pip --version
```

### 작업 종료 시

```bash
deactivate
```

---

## 45. Windows와 macOS 명령 비교

Windows와 macOS를 함께 사용하는 경우 다음 차이를 기억하면 편하다.

| 작업 | Windows PowerShell | macOS Terminal |
|---|---|---|
| Python 버전 확인 | `python --version` | `python3 --version` |
| pip 확인 | `python -m pip --version` | `python3 -m pip --version` |
| 가상환경 생성 | `python -m venv .venv` | `python3 -m venv .venv` |
| 가상환경 활성화 | `.\.venv\Scripts\Activate.ps1` | `source .venv/bin/activate` |
| 활성화 후 Python 확인 | `where python` | `which python` |
| 가상환경 종료 | `deactivate` | `deactivate` |

가장 중요한 차이는 가상환경 내부 구조이다.

```text
Windows
.venv/Scripts/

macOS
.venv/bin/
```

---

## 46. 이 문서 이후의 다음 단계

이 문서의 환경 구성이 끝났다면 macOS에서 Python 기반 프로젝트를 실행할 기본 준비가 완료된 것이다.

이후 프로젝트 구성은 필요한 기능에 따라 다음 단계로 진행한다.

```text
Python 기본 환경 구성 완료
        ↓
프로젝트 참여 및 Repository Clone
        ↓
프로젝트별 패키지 설치
        ↓
MkDocs 환경 구성
        ↓
RAG 실습 환경 구성
        ↓
LangChain / LangGraph 학습
        ↓
AI Agent / Enterprise AI Agent 실습
```

> 실제 패키지 설치 명령과 실행 방법은 각 기능별 가이드의 내용을 우선한다.

---

## 47. 참고 공식 문서

이 가이드는 다음 공식 문서를 기준으로 macOS Python 환경 구성 방법을 정리하였다.

- Python 공식 문서 - Using Python on macOS  
  https://docs.python.org/3/using/mac.html

- Python Packaging User Guide - Install packages in a virtual environment using pip and venv  
  https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/

- Homebrew Documentation - Homebrew and Python  
  https://docs.brew.sh/Homebrew-and-Python

- Homebrew Python Formula  
  https://formulae.brew.sh/formula/python

---

## 48. 최종 정리

macOS에서 AI-Data-Platform 프로젝트의 Python 환경을 구성할 때 핵심 원칙은 다음과 같다.

```text
1. 기존 Python 설치 여부와 실행 위치를 먼저 확인한다.
2. Apple이 관리하는 /usr/bin/python3를 임의로 수정하거나 삭제하지 않는다.
3. 프로젝트에서 사용할 별도의 Python을 설치한다.
4. 가상환경 생성 전에는 python3 명령을 기준으로 사용한다.
5. 프로젝트 루트에 .venv를 생성한다.
6. Terminal을 새로 열 때마다 .venv를 다시 생성하지 않고 활성화만 한다.
7. Python 패키지는 시스템 전체가 아니라 .venv 내부에 설치한다.
8. pip는 가능하면 python -m pip 형식으로 실행한다.
9. Windows에서 만든 .venv와 macOS에서 만든 .venv를 서로 공유하지 않는다.
10. 팀에서 지정한 Python 버전과 패키지 버전 정책을 우선한다.
```

이 원칙을 유지하면 Windows와 macOS를 함께 사용하는 팀에서도 Python 실행 환경 차이로 발생하는 문제를 크게 줄일 수 있다.
