# Python 핵심 가이드

> 대상: Python을 처음 학습하면서 AI DATA Platform의 RAG / AI Agent 실습 코드를 읽고 수정해야 하는 사람  
> 목적: Python 문법을 단순 암기하는 것이 아니라, 실습 코드가 어떤 흐름으로 동작하는지 이해할 수 있도록 핵심 개념을 정리한다.  
> 권장 위치: `시작하기 > Python 핵심 가이드`

---

## 문서에서 다루는 범위

이 문서는 AI DATA Platform 실습을 진행하면서 자주 만나는 Python 문법과 실행 구조를 중심으로 설명한다.

특히 다음과 같은 코드를 읽을 수 있도록 돕는 것이 목적이다.

```python
from pathlib import Path
import json
import sys

def main() -> None:
    query = " ".join(sys.argv[1:]).strip()
    print(query)

if __name__ == "__main__":
    main()
```

처음 Python을 보면 위 코드는 짧아 보이지만, 실제로는 다음 개념이 모두 들어 있다.

- `import`
- `Path`
- 함수 정의
- 타입 힌트
- `sys.argv`
- 리스트 슬라이싱
- 문자열 `join()`
- 문자열 `strip()`
- `if __name__ == "__main__"`
- 프로그램 실행 흐름

따라서 Python을 배울 때는 문법 하나하나를 따로 외우는 것보다, **실습 코드 안에서 이 문법이 왜 필요한지**를 함께 이해하는 것이 중요하다.

---

# 1. Python을 배울 때 먼저 잡아야 할 관점

## 1.1 Python은 문법이 짧지만 의미가 압축되어 있다

Python은 Java나 C 계열 언어보다 코드가 짧다.  
하지만 코드가 짧다고 해서 항상 쉽다는 뜻은 아니다.

예를 들어 Java에서는 다음처럼 명확하게 타입을 선언한다.

```java
String name = "Python";
int age = 10;
```

Python에서는 다음처럼 작성한다.

```python
name = "Python"
age = 10
```

처음에는 Python 코드가 훨씬 쉬워 보인다.  
하지만 타입을 명시하지 않기 때문에, 코드를 읽는 사람이 직접 값의 성격을 추론해야 하는 경우가 많다.

또한 Python은 중괄호(`{}`)를 사용하지 않고 들여쓰기로 코드 블록을 구분한다.

```python
if age >= 20:
    print("성인입니다.")
else:
    print("미성년자입니다.")
```

Java처럼 중괄호가 있는 언어에 익숙하다면 처음에는 불안하게 느껴질 수 있다.  
하지만 Python에서는 **들여쓰기 자체가 문법**이다.

즉, Python을 배울 때는 다음 관점을 잡아야 한다.

```text
Python은 짧게 쓰는 언어이다.
하지만 짧은 코드 안에 많은 의미가 들어 있다.
따라서 문법을 볼 때 "왜 이렇게 줄여 썼는가?"를 함께 봐야 한다.
```

---

## 1.2 Python 파일은 위에서 아래로 실행된다

Python 파일은 기본적으로 위에서 아래로 순서대로 읽히고 실행된다.

예를 들어 다음 파일이 있다고 하자.

```python
print("1번")

def hello():
    print("2번")

print("3번")
hello()
```

실행 결과는 다음과 같다.

```text
1번
3번
2번
```

왜 이런 결과가 나올까?

Python은 파일을 위에서 아래로 읽는다.  
`def hello():` 부분은 함수를 **정의**하는 것이지, 바로 실행하는 것이 아니다.  
함수 내부의 `print("2번")`은 `hello()`가 호출될 때 실행된다.

이 개념은 매우 중요하다.  
Python 실습 파일을 볼 때 `def`로 시작하는 함수들이 많이 나오면, 그 함수들이 바로 실행되는 것이 아니다.

실제로 실행되는 흐름은 보통 맨 아래의 다음 코드에서 시작된다.

```python
if __name__ == "__main__":
    main()
```

따라서 실습 파일을 읽을 때는 파일의 맨 위부터 무작정 해석하기보다, 먼저 아래 구조를 찾는 습관이 좋다.

```text
1. import 확인
2. 상수 확인
3. 함수 정의 확인
4. main() 함수 확인
5. if __name__ == "__main__" 확인
6. main()에서 어떤 함수가 어떤 순서로 호출되는지 확인
```

---

## 1.3 Python은 "문법"보다 "실행 흐름"이 중요하다

RAG 실습 코드는 대부분 다음 흐름을 가진다.

```text
문서 파일 읽기
  ↓
텍스트 추출
  ↓
Chunk 분리
  ↓
Embedding 생성
  ↓
Vector DB 저장
  ↓
사용자 질문 입력
  ↓
질문 Embedding 생성
  ↓
유사 문서 검색
  ↓
Prompt 생성
  ↓
LLM 호출
  ↓
답변 출력
```

Python 문법은 이 흐름을 구현하기 위한 도구이다.  
따라서 코드를 볼 때 다음 질문을 계속 던지는 것이 좋다.

```text
이 코드는 전체 RAG 흐름 중 어느 단계인가?
입력은 무엇인가?
출력은 무엇인가?
다음 함수로 어떤 값을 넘기는가?
파일을 읽는가, 저장하는가, 검색하는가, 호출하는가?
```

이 질문을 하면서 코드를 보면 단순 문법 암기보다 훨씬 빨리 이해된다.

---

# 2. Python 실행 환경 기본

## 2.1 Python 설치 확인

터미널에서 Python이 설치되어 있는지 확인한다.

```bash
python --version
```

환경에 따라 `python` 명령이 동작하지 않고 `python3` 명령만 동작할 수 있다.

```bash
python3 --version
```

예시 출력:

```text
Python 3.14.5
```

여기서 중요한 것은 Python 버전 자체보다, **내가 지금 어떤 Python을 실행하고 있는가**이다.

Mac이나 Linux에서는 시스템에 기본 Python이 설치되어 있을 수 있고, 별도로 설치한 Python이 또 있을 수 있다.  
가상환경을 사용하면 프로젝트별로 사용하는 Python과 패키지를 분리할 수 있다.

---

## 2.2 `python`과 `python3` 차이

환경에 따라 다음 두 명령어가 다르게 동작할 수 있다.

```bash
python --version
python3 --version
```

어떤 컴퓨터에서는 `python`이 Python 2를 가리키거나 아예 없을 수 있다.  
요즘은 대부분 Python 3를 사용하므로, 문제가 생기면 `python3` 명령을 사용해보면 된다.

다만 프로젝트 문서나 실습 가이드에서는 하나의 기준을 정하는 것이 좋다.  
AI DATA Platform 실습에서는 다음 방식이 가장 안전하다.

```bash
python -m pip install 패키지명
python 실습파일.py
```

만약 `python` 명령이 동작하지 않는 환경이면 다음처럼 바꾸면 된다.

```bash
python3 -m pip install 패키지명
python3 실습파일.py
```

---

## 2.3 pip란 무엇인가?

`pip`는 Python 패키지를 설치하는 도구이다.

Python 자체에는 기본 기능만 들어 있다.  
PDF를 읽거나, Word 문서를 읽거나, ChromaDB를 사용하거나, Embedding 모델을 사용하려면 외부 라이브러리를 설치해야 한다.

예를 들어 RAG 실습에서는 다음과 같은 라이브러리를 사용한다.

```bash
python -m pip install chromadb
python -m pip install sentence-transformers
python -m pip install pypdf
python -m pip install python-docx
python -m pip install openpyxl
```

여기서 `python -m pip install` 형식을 권장하는 이유가 있다.

단순히 다음처럼 실행할 수도 있다.

```bash
pip install chromadb
```

하지만 이 경우 `pip`가 어느 Python에 연결된 pip인지 헷갈릴 수 있다.  
컴퓨터에 Python이 여러 개 설치되어 있으면 패키지가 엉뚱한 Python 환경에 설치될 수 있다.

반면 다음 명령은 의미가 명확하다.

```bash
python -m pip install chromadb
```

의미는 다음과 같다.

```text
현재 python 명령이 가리키는 Python 환경에서
pip 모듈을 실행해서
chromadb 패키지를 설치하라.
```

즉, 실습 파일을 실행할 Python과 패키지를 설치할 Python을 맞추기 쉽다.

---

## 2.4 가상환경이 필요한 이유

가상환경은 프로젝트별로 Python 패키지 설치 공간을 분리하는 기능이다.

예를 들어 다음 두 프로젝트가 있다고 하자.

```text
프로젝트 A: RAG 실습
  - chromadb 필요
  - sentence-transformers 필요
  - pypdf 필요

프로젝트 B: 웹 개발
  - fastapi 필요
  - uvicorn 필요
  - sqlalchemy 필요
```

가상환경 없이 전역 환경에 모든 패키지를 설치하면 프로젝트가 많아질수록 패키지 버전이 섞인다.  
어떤 프로젝트는 `chromadb`의 특정 버전이 필요하고, 다른 프로젝트는 다른 버전이 필요할 수도 있다.

가상환경을 사용하면 다음처럼 분리된다.

```text
AI-Data-Platform/
  .venv/
    chromadb
    sentence-transformers
    pypdf

Other-Project/
  .venv/
    fastapi
    uvicorn
```

즉, 프로젝트마다 독립적인 Python 패키지 공간을 가진다.

---

## 2.5 가상환경 생성과 활성화

프로젝트 루트 디렉터리에서 다음 명령어를 실행한다.

```bash
python -m venv .venv
```

여기서 `.venv`는 가상환경 폴더 이름이다.  
보통 Python 프로젝트에서는 `.venv`라는 이름을 많이 사용한다.

macOS / Linux에서는 다음 명령어로 활성화한다.

```bash
source .venv/bin/activate
```

Windows PowerShell에서는 다음 명령어를 사용한다.

```powershell
.venv\Scripts\Activate.ps1
```

가상환경이 활성화되면 터미널 앞쪽에 보통 다음처럼 표시된다.

```text
(.venv) ➜ AI-Data-Platform
```

이 상태에서 설치하는 패키지는 해당 프로젝트의 `.venv` 안에 설치된다.

비활성화하려면 다음을 실행한다.

```bash
deactivate
```

---

## 2.6 requirements.txt의 역할

`requirements.txt`는 이 프로젝트에서 필요한 Python 패키지 목록을 적어두는 파일이다.

예시:

```text
chromadb
sentence-transformers
pypdf
python-docx
openpyxl
requests
```

새로운 사람이 프로젝트를 내려받았을 때 다음 명령어만 실행하면 필요한 패키지를 한 번에 설치할 수 있다.

```bash
python -m pip install -r requirements.txt
```

반대로 현재 설치된 패키지 목록을 파일로 저장하려면 다음을 사용한다.

```bash
python -m pip freeze > requirements.txt
```

다만 초보 단계에서는 `pip freeze` 결과를 그대로 저장하면 너무 많은 패키지가 들어갈 수 있다.  
예를 들어 `sentence-transformers` 하나를 설치했는데 내부 의존성 패키지까지 모두 저장될 수 있다.

실습 문서에서는 필요한 주요 패키지만 직접 적는 방식이 더 이해하기 쉽다.

---

## 2.7 환경 문제를 확인하는 기본 명령어

Python 실습에서 오류가 나면 먼저 환경을 확인해야 한다.

```bash
which python
python --version
python -m pip --version
python -m pip list
```

macOS / Linux에서 `which python`은 현재 사용 중인 Python 실행 파일 경로를 보여준다.

예시:

```text
/Volumes/data/projects/AI-Data-Platform/.venv/bin/python
```

이렇게 `.venv` 안의 Python이 나오면 가상환경이 잘 활성화된 것이다.

패키지가 설치되어 있는지 확인하려면 다음을 사용한다.

```bash
python -m pip list
```

특정 패키지만 확인하고 싶으면 다음처럼 사용할 수 있다.

```bash
python -m pip show chromadb
```

---

# 3. Python 파일 실행 구조

## 3.1 Python 파일 실행

Python 파일은 다음처럼 실행한다.

```bash
python 08_first_rag.py
```

명령어의 의미는 다음과 같다.

```text
python 인터프리터로
08_first_rag.py 파일을 실행하라.
```

Python은 컴파일 언어라기보다 인터프리터 방식으로 실행된다.  
즉, Python 실행기가 `.py` 파일을 읽으면서 코드를 실행한다.

실습 파일을 실행할 때는 현재 위치가 중요하다.  
예를 들어 파일이 `labs/rag` 폴더에 있다면 다음처럼 해당 폴더로 이동한 뒤 실행한다.

```bash
cd labs/rag
python 08_first_rag.py
```

경로가 맞지 않으면 파일을 찾지 못하거나, 코드 내부에서 참조하는 상대경로가 달라질 수 있다.

---

## 3.2 main() 함수는 자동 실행되지 않는다

Java에서는 다음 메서드가 프로그램의 시작점이다.

```java
public static void main(String[] args) {
    System.out.println("시작");
}
```

하지만 Python에서는 `main()`이라는 이름이 특별한 예약어가 아니다.  
그냥 함수 이름일 뿐이다.

```python
def main() -> None:
    print("프로그램 시작")
```

위 코드는 `main()` 함수를 정의한 것이다.  
하지만 함수 정의만으로는 실행되지 않는다.

실행하려면 다음처럼 직접 호출해야 한다.

```python
main()
```

따라서 다음 코드는 아무것도 출력하지 않는다.

```python
def main() -> None:
    print("프로그램 시작")
```

반면 다음 코드는 출력된다.

```python
def main() -> None:
    print("프로그램 시작")

main()
```

출력:

```text
프로그램 시작
```

---

## 3.3 `if __name__ == "__main__"`의 의미

Python 실습 코드에서 가장 자주 만나는 구조이다.

```python
def main() -> None:
    print("프로그램 시작")


if __name__ == "__main__":
    main()
```

처음 보면 매우 이상해 보일 수 있다.  
하지만 의미는 간단하다.

```text
이 파일이 직접 실행된 경우에만 main() 함수를 실행하라.
```

Python 파일은 두 가지 방식으로 사용될 수 있다.

첫 번째는 직접 실행하는 방식이다.

```bash
python 08_first_rag.py
```

두 번째는 다른 파일에서 가져다 쓰는 방식이다.

```python
import first_rag
```

직접 실행할 때는 `__name__` 값이 `"__main__"`이 된다.  
다른 파일에서 import할 때는 `__name__` 값이 파일명 또는 모듈명이 된다.

그래서 다음 코드는 파일을 직접 실행할 때만 `main()`을 호출한다.

```python
if __name__ == "__main__":
    main()
```

이 구조를 사용하는 이유는 다음과 같다.

- 직접 실행 가능한 실습 파일로 만들 수 있다.
- 다른 파일에서 함수만 가져다 쓸 수 있다.
- import했을 때 원하지 않는 실행이 발생하지 않는다.
- 테스트 코드 작성이 쉬워진다.

---

## 3.4 실습 코드 읽는 기본 순서

Python 실습 파일을 볼 때는 다음 순서가 좋다.

```text
1. 파일명 확인
2. import 확인
3. 상수 확인
4. 함수 목록 확인
5. main() 함수 확인
6. if __name__ == "__main__" 확인
7. main()에서 호출하는 함수 순서 확인
8. 각 함수 내부를 따라가며 세부 구현 확인
```

예를 들어 `08_first_rag.py`라면 다음처럼 추정할 수 있다.

```text
파일명: 08_first_rag.py
역할: 첫 번째 RAG 흐름 구현
관심 포인트:
  - 문서 검색 함수
  - 프롬프트 생성 함수
  - LLM 호출 함수
  - main() 실행 흐름
```

`main()` 함수가 있으면 프로그램의 실제 흐름은 대부분 그 안에 있다.

---

# 4. 들여쓰기와 코드 블록

## 4.1 Python은 중괄호 대신 들여쓰기를 사용한다

Java에서는 코드 블록을 중괄호로 구분한다.

```java
if (score >= 80) {
    System.out.println("합격");
} else {
    System.out.println("불합격");
}
```

Python에서는 중괄호를 사용하지 않는다.

```python
if score >= 80:
    print("합격")
else:
    print("불합격")
```

여기서 `if` 아래에 들여쓰기 된 부분이 if 블록이다.  
`else` 아래에 들여쓰기 된 부분이 else 블록이다.

Python에서 들여쓰기는 단순한 보기 좋게 만드는 스타일이 아니라 **문법**이다.

---

## 4.2 들여쓰기 오류 예시

다음 코드는 오류가 발생한다.

```python
if score >= 80:
print("합격")
```

`if` 다음 줄은 반드시 들여쓰기 되어야 한다.

올바른 코드는 다음과 같다.

```python
if score >= 80:
    print("합격")
```

보통 Python에서는 공백 4칸을 사용한다.

---

## 4.3 들여쓰기 때문에 의미가 달라지는 예시

다음 두 코드는 의미가 다르다.

```python
names = ["A", "B", "C"]

for name in names:
    print(name)
    print("반복 중")
```

출력:

```text
A
반복 중
B
반복 중
C
반복 중
```

반면 다음 코드는 다르다.

```python
names = ["A", "B", "C"]

for name in names:
    print(name)

print("반복 종료")
```

출력:

```text
A
B
C
반복 종료
```

`print("반복 종료")`는 들여쓰기 되어 있지 않으므로 반복문 밖에서 한 번만 실행된다.

RAG 실습에서 파일을 여러 개 처리하거나 페이지를 반복 처리할 때 들여쓰기 하나로 결과가 달라질 수 있으므로 주의해야 한다.

---

# 5. 변수와 기본 자료형

## 5.1 변수 선언

Python은 변수 타입을 직접 선언하지 않는다.

```python
name = "김장관"
age = 50
height = 171.5
is_active = True
```

자료형은 값에 따라 자동으로 결정된다.

| 자료형 | 예시 | 설명 |
|---|---|---|
| `str` | `"hello"` | 문자열 |
| `int` | `10` | 정수 |
| `float` | `3.14` | 실수 |
| `bool` | `True`, `False` | 참/거짓 |
| `None` | `None` | 값이 없음 |

Python에서는 다음처럼 같은 변수에 다른 타입의 값을 다시 넣을 수도 있다.

```python
value = 10
value = "hello"
```

문법적으로는 가능하다.  
하지만 실무에서는 이렇게 타입이 바뀌면 코드를 읽기 어려워지고 오류가 생기기 쉽다.

따라서 한 변수에는 가능하면 같은 성격의 값만 넣는 것이 좋다.

---

## 5.2 변수 이름 작성 관례

Python에서는 변수명과 함수명에 보통 `snake_case`를 사용한다.

```python
user_name = "김장관"
document_count = 10
chunk_size = 500
```

Java에서는 보통 `camelCase`를 많이 사용한다.

```java
String userName = "김장관";
int documentCount = 10;
```

Python에서 다음처럼 작성해도 동작은 한다.

```python
userName = "김장관"
```

하지만 Python 스타일에서는 `user_name`이 더 자연스럽다.

상수처럼 사용하는 값은 대문자와 언더스코어를 사용한다.

```python
BASE_DIR = Path(__file__).resolve().parent
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
COLLECTION_NAME = "microserver_docs"
```

상수라고 해서 Python이 변경을 막아주는 것은 아니다.  
다만 대문자로 작성하면 “이 값은 프로그램 설정값처럼 사용한다”는 의도를 표현한다.

---

## 5.3 `type()` 함수

변수의 자료형을 확인할 때 사용한다.

```python
value = "hello"
print(type(value))
```

출력:

```text
<class 'str'>
```

처음 Python을 배울 때는 `type()`으로 값을 확인하는 습관이 도움이 된다.

예를 들어 다음 코드가 있다고 하자.

```python
result = collection.query(...)
print(type(result))
```

`result`가 `dict`인지, `list`인지, 객체인지 확인하면 이후 코드를 이해하기 쉬워진다.

---

## 5.4 문자열

문자열은 작은따옴표 또는 큰따옴표를 사용할 수 있다.

```python
name1 = 'Python'
name2 = "Python"
```

둘 다 같은 문자열이다.  
프로젝트에서는 하나의 스타일을 정해서 사용하는 것이 좋다.

문자열 안에 작은따옴표가 들어가야 하면 큰따옴표를 사용하면 편하다.

```python
message = "I'm learning Python"
```

문자열 안에 큰따옴표가 들어가야 하면 작은따옴표를 사용할 수 있다.

```python
message = '그는 "Python이 좋다"고 말했다.'
```

---

## 5.5 여러 줄 문자열과 프롬프트 작성

여러 줄 문자열은 삼중 따옴표를 사용한다.

```python
prompt = """
너는 사내 문서 기반 RAG 답변 도우미이다.
아래 참고 문서만 근거로 답변하라.
"""
```

RAG 실습에서는 LLM에게 전달할 프롬프트를 만들 때 여러 줄 문자열을 자주 사용한다.

```python
prompt = f"""
너는 사내 문서 기반 RAG 답변 도우미이다.

아래 [참고 문서]만 근거로 사용해서 질문에 답변하라.
참고 문서에 없는 내용은 추측하지 말고
"제공된 문서에서는 확인되지 않습니다."라고 답변하라.

[참고 문서]
{context}

[질문]
{query}

[답변]
"""
```

삼중 따옴표를 사용하는 이유는 줄바꿈을 포함한 긴 문자열을 보기 좋게 작성하기 위해서이다.

---

## 5.6 f-string

f-string은 문자열 안에 변수값을 넣는 문법이다.

```python
name = "김장관"
message = f"안녕하세요. {name}님"
print(message)
```

출력:

```text
안녕하세요. 김장관님
```

`f`는 format의 의미로 이해하면 된다.  
문자열 앞에 `f`를 붙이면 `{}` 안에 변수나 표현식을 넣을 수 있다.

```python
count = 3
print(f"검색 결과는 {count}건입니다.")
```

출력:

```text
검색 결과는 3건입니다.
```

RAG 실습에서는 프롬프트 생성, 파일 경로 출력, 오류 메시지 작성에 자주 사용한다.

```python
raise RuntimeError(f"컬렉션을 찾을 수 없습니다: {COLLECTION_NAME}")
```

---

# 6. 주요 자료구조

## 6.1 list

`list`는 여러 값을 순서대로 저장하는 자료구조이다.

```python
names = ["김장관", "박은진", "김보경"]
```

값은 인덱스로 접근한다.

```python
print(names[0])
print(names[1])
```

출력:

```text
김장관
박은진
```

Python의 인덱스는 0부터 시작한다.

```text
names = ["김장관", "박은진", "김보경"]
          0        1        2
```

list는 값 변경이 가능하다.

```python
names[0] = "장관"
```

값 추가도 가능하다.

```python
names.append("홍길동")
```

RAG 실습에서는 다음과 같은 곳에서 list를 자주 사용한다.

- 문서 파일 목록
- Chunk 목록
- 검색 결과 목록
- 메타데이터 목록
- 함수에서 여러 결과를 반환할 때

예시:

```python
chunks = [
    {"text": "첫 번째 chunk", "source": "a.md"},
    {"text": "두 번째 chunk", "source": "b.md"},
]
```

---

## 6.2 dict

`dict`는 key-value 형태로 데이터를 저장한다.  
Java의 `Map`과 비슷하게 이해할 수 있다.

```python
person = {
    "name": "김장관",
    "role": "이사",
    "age": 50,
}
```

값을 가져올 때는 key를 사용한다.

```python
print(person["name"])
```

출력:

```text
김장관
```

하지만 없는 key를 `[]`로 접근하면 오류가 발생한다.

```python
print(person["company"])  # KeyError
```

그래서 안전하게 값을 가져올 때는 `get()`을 많이 사용한다.

```python
print(person.get("company"))
```

없는 key이면 `None`을 반환한다.

기본값을 지정할 수도 있다.

```python
print(person.get("company", "회사 정보 없음"))
```

RAG 실습에서는 문서 메타데이터를 dict로 많이 표현한다.

```python
metadata = {
    "source": "sample.pdf",
    "page": 3,
    "chunk_index": 10,
}
```

검색 결과도 dict 형태로 많이 다룬다.

```python
result = {
    "document": "검색된 문서 내용",
    "metadata": {"source": "guide.md"},
    "distance": 0.23,
}
```

dict를 잘 이해하면 JSON, JSONL, API 응답, ChromaDB 검색 결과를 읽기가 훨씬 쉬워진다.

---

## 6.3 tuple

`tuple`은 변경할 수 없는 순서형 자료구조이다.

```python
extensions = (".txt", ".md", ".pdf")
```

list와 비슷하지만 한 번 만든 후 값을 변경할 수 없다.

```python
extensions[0] = ".docx"  # 오류
```

처음에는 이렇게 생각할 수 있다.

```text
list가 있는데 왜 tuple이 필요하지?
```

tuple을 사용하는 이유는 **변경되면 안 되는 값**을 표현하기 위해서이다.

예를 들어 처리 가능한 파일 확장자는 프로그램 실행 중에 바뀔 일이 거의 없다.

```python
ALLOWED_EXTENSIONS = (".txt", ".md", ".pdf", ".docx")
```

이렇게 tuple로 작성하면 이 값은 변경하지 않는 값이라는 의도를 표현할 수 있다.

실무에서는 다음 같은 값에 tuple을 자주 사용한다.

- 처리 대상 확장자 목록
- 좌표값
- RGB 색상값
- 함수에서 여러 값을 묶어 반환할 때
- 변경되면 안 되는 설정값

주의할 점은 tuple은 map이 아니다.  
key-value 구조는 dict이고, tuple은 순서가 있는 값 묶음이다.

---

## 6.4 set

`set`은 중복을 허용하지 않는 자료구조이다.

```python
items = {"pdf", "docx", "pdf"}
print(items)
```

결과에는 `pdf`가 한 번만 들어간다.

```text
{'pdf', 'docx'}
```

set은 순서보다 **포함 여부 확인**이 중요할 때 유용하다.

```python
allowed = {"pdf", "docx", "txt"}

if "pdf" in allowed:
    print("처리 가능")
```

list에서도 `in`을 사용할 수 있지만, 데이터가 많을 때 set이 포함 여부 확인에 더 적합하다.

RAG 실습에서는 중복 파일명 제거, 중복 문서 ID 제거, 처리한 확장자 확인 등에 사용할 수 있다.

---

## 6.5 list, dict, tuple, set 비교

| 자료구조 | 형태 | 변경 가능 | 중복 | 주 사용 목적 |
|---|---|---:|---:|---|
| list | `[1, 2, 3]` | 가능 | 가능 | 순서 있는 목록 |
| dict | `{"key": "value"}` | 가능 | key 중복 불가 | key-value 데이터 |
| tuple | `(1, 2, 3)` | 불가 | 가능 | 변경하지 않을 값 묶음 |
| set | `{1, 2, 3}` | 가능 | 불가 | 중복 제거, 포함 여부 확인 |

초보 단계에서는 다음처럼 기억하면 된다.

```text
여러 개를 순서대로 저장한다 → list
이름표(key)를 붙여 저장한다 → dict
변경되지 않는 목록이다 → tuple
중복을 제거하고 싶다 → set
```

---

# 7. 조건문

## 7.1 if / elif / else

조건문은 조건에 따라 다른 코드를 실행할 때 사용한다.

```python
score = 85

if score >= 90:
    print("A")
elif score >= 80:
    print("B")
else:
    print("C")
```

`elif`는 Java의 `else if`와 비슷하다.

조건문을 읽을 때는 위에서 아래로 조건을 확인한다.

```text
score가 90 이상인가?
  아니면 score가 80 이상인가?
    아니면 C
```

---

## 7.2 조건식에서 자주 쓰는 비교 연산자

| 연산자 | 의미 |
|---|---|
| `==` | 같다 |
| `!=` | 다르다 |
| `>` | 크다 |
| `>=` | 크거나 같다 |
| `<` | 작다 |
| `<=` | 작거나 같다 |

주의할 점은 `=`와 `==`가 다르다는 것이다.

```python
name = "Python"   # 값을 대입
name == "Python"  # 같은지 비교
```

---

## 7.3 and / or / not

여러 조건을 조합할 때 사용한다.

```python
if path.is_file() and path.suffix.lower() in lower_extensions:
    print("처리 대상 파일")
```

의미:

```text
path가 파일이고
확장자가 처리 대상 목록에 포함되어 있으면
처리 대상 파일이다.
```

`and`는 두 조건이 모두 참이어야 한다.  
`or`는 둘 중 하나만 참이어도 된다.  
`not`은 조건을 반대로 뒤집는다.

```python
if not query.strip():
    raise ValueError("검색 질문이 비어 있습니다.")
```

이 코드는 다음 의미이다.

```text
query에서 양쪽 공백을 제거했는데 비어 있다면
오류를 발생시켜라.
```

---

## 7.4 Python에서 비어 있는 값은 False처럼 동작한다

Python에서는 다음 값들이 조건문에서 False처럼 동작한다.

```python
None
""
[]
{}
()
set()
0
```

예를 들어 다음 코드는 query가 빈 문자열이면 실행된다.

```python
query = ""

if not query:
    print("질문이 비어 있습니다.")
```

RAG 실습에서는 사용자 질문이 비어 있는지 확인할 때 자주 사용한다.

```python
if not query.strip():
    raise ValueError("검색 질문이 비어 있습니다.")
```

---

# 8. 반복문

## 8.1 for 문

`for` 문은 목록에서 값을 하나씩 꺼내 반복할 때 사용한다.

```python
names = ["김장관", "박은진", "김보경"]

for name in names:
    print(name)
```

출력:

```text
김장관
박은진
김보경
```

의미는 다음과 같다.

```text
names 안에 있는 값을 하나씩 꺼내서
매번 name 변수에 넣고
반복문 내부를 실행한다.
```

RAG 실습에서는 파일 목록, 문서 목록, Chunk 목록, 페이지 목록을 처리할 때 `for` 문을 자주 사용한다.

```python
for path in input_dir.glob("*.pdf"):
    print(path)
```

---

## 8.2 enumerate()

`enumerate()`는 반복하면서 인덱스와 값을 함께 가져올 때 사용한다.

```python
names = ["김장관", "박은진", "김보경"]

for index, name in enumerate(names):
    print(index, name)
```

출력:

```text
0 김장관
1 박은진
2 김보경
```

PDF 페이지를 처리할 때 자주 나온다.

```python
for page_index, page in enumerate(reader.pages):
    text = page.extract_text() or ""
```

의미는 다음과 같다.

```text
reader.pages에서 페이지를 하나씩 꺼낸다.
page_index에는 몇 번째 페이지인지 저장한다.
page에는 실제 페이지 객체가 저장된다.
```

초보자가 헷갈리는 부분은 쉼표이다.

```python
for page_index, page in enumerate(reader.pages):
```

이 코드는 `enumerate()`가 매 반복마다 두 값을 돌려주기 때문에 가능하다.

```text
0, 첫 번째 페이지
1, 두 번째 페이지
2, 세 번째 페이지
```

그래서 앞쪽에서 두 변수로 나누어 받는다.

```python
page_index, page = 0, 첫 번째 페이지
```

---

## 8.3 while 문

`while` 문은 조건이 참인 동안 반복한다.

```python
count = 0

while count < 3:
    print(count)
    count += 1
```

출력:

```text
0
1
2
```

`for` 문은 반복할 대상이 명확할 때 많이 사용하고,  
`while` 문은 특정 조건이 만족될 때까지 반복해야 할 때 사용한다.

RAG 실습에서는 `while`보다 `for`가 더 자주 등장한다.  
문서 목록, 페이지 목록, Chunk 목록처럼 반복 대상이 명확하기 때문이다.

---

## 8.4 break와 continue

`break`는 반복문을 즉시 종료한다.

```python
for name in names:
    if name == "박은진":
        break
    print(name)
```

`continue`는 현재 반복을 건너뛰고 다음 반복으로 넘어간다.

```python
for path in paths:
    if not path.is_file():
        continue

    print(path)
```

파일 처리 코드에서 `continue`는 자주 사용된다.  
예를 들어 폴더가 섞여 있으면 파일이 아닌 것은 건너뛰고 다음 경로를 처리할 수 있다.

---

# 9. 함수

## 9.1 함수가 필요한 이유

함수는 특정 작업을 이름 붙여 재사용하기 위한 구조이다.

예를 들어 다음 코드가 여러 곳에서 반복된다고 하자.

```python
print("=" * 80)
print("RAG 답변")
print("=" * 80)
```

이 코드를 함수로 만들면 다음처럼 사용할 수 있다.

```python
def print_title(title: str) -> None:
    print("=" * 80)
    print(title)
    print("=" * 80)
```

사용:

```python
print_title("RAG 답변")
```

함수를 사용하는 이유는 다음과 같다.

- 반복되는 코드를 줄일 수 있다.
- 코드의 의도를 이름으로 표현할 수 있다.
- 큰 프로그램을 작은 단위로 나눌 수 있다.
- 테스트하기 쉬워진다.
- 실습 흐름을 단계별로 이해하기 쉬워진다.

RAG 실습에서도 보통 다음처럼 기능별로 함수를 나눈다.

```text
문서 읽기 함수
Chunk 생성 함수
Embedding 생성 함수
ChromaDB 저장 함수
검색 함수
Prompt 생성 함수
LLM 호출 함수
main 함수
```

---

## 9.2 함수 기본 구조

```python
def add(a, b):
    return a + b
```

구조는 다음과 같다.

```text
def 함수명(파라미터):
    실행할 코드
    return 반환값
```

사용:

```python
result = add(3, 5)
print(result)
```

출력:

```text
8
```

---

## 9.3 파라미터와 반환값

파라미터는 함수에 전달하는 입력값이다.

```python
def greet(name):
    print(f"안녕하세요. {name}님")
```

`name`이 파라미터이다.

```python
greet("김장관")
```

반환값은 함수가 처리 결과로 돌려주는 값이다.

```python
def add(a, b):
    return a + b

result = add(3, 5)
```

`return`이 없으면 함수는 기본적으로 `None`을 반환한다.

---

## 9.4 타입 힌트

Python은 타입 선언이 필수는 아니지만, 실무 코드에서는 타입 힌트를 자주 사용한다.

```python
def add(a: int, b: int) -> int:
    return a + b
```

의미:

```text
a는 int를 기대한다.
b는 int를 기대한다.
반환값도 int를 기대한다.
```

주의할 점은 타입 힌트가 Java처럼 강제 타입 검사를 하는 것은 아니라는 점이다.

```python
def add(a: int, b: int) -> int:
    return a + b

print(add("A", "B"))
```

이 코드는 실행될 수 있다.

출력:

```text
AB
```

타입 힌트는 주로 다음 목적에 사용된다.

- 코드를 읽는 사람이 이해하기 쉽게 한다.
- IDE가 자동완성과 오류 힌트를 제공할 수 있다.
- 정적 분석 도구가 잠재 오류를 찾을 수 있다.
- 함수의 입력과 출력을 문서처럼 표현한다.

---

## 9.5 `-> None`의 의미

```python
def main() -> None:
    print("실행")
```

`-> None`은 이 함수가 특별한 값을 반환하지 않는다는 뜻이다.

다음 코드와 비슷하게 이해하면 된다.

```python
def main():
    print("실행")
    return None
```

실무에서는 출력만 하거나 파일 저장만 하는 함수에 `-> None`을 붙이는 경우가 많다.

```python
def ensure_directories() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
```

이 함수는 디렉터리를 만들 뿐, 어떤 값을 반환하지 않는다.

---

## 9.6 기본 파라미터 값

```python
def search_documents(query: str, top_k: int = 3) -> list[dict]:
    pass
```

`top_k: int = 3`의 의미는 다음과 같다.

```text
top_k 값이 전달되지 않으면 기본값으로 3을 사용한다.
```

사용 예시는 다음과 같다.

```python
search_documents("RAG란?")        # top_k는 3
search_documents("RAG란?", 5)     # top_k는 5
```

RAG 검색에서 `top_k`는 보통 상위 몇 개의 유사 문서를 가져올지 의미한다.

```text
top_k = 3 → 가장 유사한 문서 3개 검색
top_k = 5 → 가장 유사한 문서 5개 검색
```

기본값을 주면 실습할 때 매번 값을 넣지 않아도 되어 편리하다.

---

## 9.7 함수 이름을 잘 짓는 것이 중요하다

Python 코드는 함수 이름만 잘 지어도 읽기 쉬워진다.

좋은 예:

```python
def read_jsonl(path: Path) -> list[dict]:
    ...

def create_chunks(text: str) -> list[str]:
    ...

def search_documents(query: str, top_k: int = 3) -> list[dict]:
    ...
```

이름만 봐도 무엇을 하는 함수인지 대략 알 수 있다.

나쁜 예:

```python
def func1():
    ...

def data():
    ...

def process():
    ...
```

이런 이름은 코드가 커질수록 이해하기 어렵다.

---

# 10. import와 모듈

## 10.1 import란?

`import`는 다른 파일이나 외부 라이브러리의 기능을 가져오는 문법이다.

```python
import json
from pathlib import Path
from typing import Any
```

Python은 모든 기능을 기본으로 메모리에 올리지 않는다.  
필요한 기능을 `import`해서 사용한다.

예를 들어 JSON 변환 기능을 사용하려면 `json` 모듈을 import한다.

```python
import json

data = {"name": "Python"}
text = json.dumps(data, ensure_ascii=False)
```

---

## 10.2 `import 모듈명`

```python
import json
```

이 방식은 모듈 전체를 가져온다.  
사용할 때는 모듈명을 붙인다.

```python
json.dumps(data)
```

장점은 어디서 온 기능인지 명확하다는 것이다.

---

## 10.3 `from 모듈 import 기능`

```python
from pathlib import Path
```

이 방식은 모듈 안의 특정 기능만 가져온다.  
사용할 때는 바로 이름을 쓸 수 있다.

```python
base_dir = Path(__file__).resolve().parent
```

만약 `import pathlib`로 가져왔다면 다음처럼 써야 한다.

```python
import pathlib

base_dir = pathlib.Path(__file__).resolve().parent
```

둘 다 가능하지만, 실무에서는 자주 쓰는 클래스나 함수는 `from ... import ...` 형태로 많이 가져온다.

---

## 10.4 표준 라이브러리와 외부 라이브러리

Python 라이브러리는 크게 두 종류가 있다.

```text
표준 라이브러리: Python 설치 시 기본 포함
외부 라이브러리: pip로 별도 설치 필요
```

표준 라이브러리 예:

```python
import json
import sys
from pathlib import Path
```

외부 라이브러리 예:

```python
import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
```

외부 라이브러리를 import했을 때 오류가 나면 보통 설치가 안 된 것이다.

```text
ModuleNotFoundError: No module named 'chromadb'
```

이 경우 다음처럼 설치한다.

```bash
python -m pip install chromadb
```

---

# 11. 파일 경로 처리

## 11.1 파일 경로가 중요한 이유

RAG 실습에서는 파일을 많이 다룬다.

- 입력 문서 폴더
- 추출된 텍스트 폴더
- Chunk 저장 파일
- ChromaDB 저장 폴더
- PDF / DOCX / XLSX 파일
- JSONL 파일

파일 경로를 잘못 잡으면 코드 자체는 맞아도 결과가 0건으로 나오거나 파일을 찾지 못한다.

예를 들어 PDF 파일이 있는데 추출 결과가 0건이면 다음을 의심해야 한다.

```text
정말 PDF 파일이 있는 폴더를 보고 있는가?
확장자가 처리 대상에 포함되어 있는가?
현재 작업 디렉터리가 예상한 위치인가?
PDF가 텍스트 기반이 아니라 스캔 이미지 PDF인가?
```

---

## 11.2 pathlib.Path

Python에서 파일 경로를 다룰 때는 `pathlib.Path`를 많이 사용한다.

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
```

`Path`를 사용하면 문자열로 경로를 조합하는 것보다 안전하고 읽기 쉽다.

예전 방식:

```python
file_path = "data" + "/" + "sample.txt"
```

Path 방식:

```python
file_path = Path("data") / "sample.txt"
```

`/` 연산자로 경로를 연결할 수 있어서 가독성이 좋다.

---

## 11.3 `__file__`

`__file__`은 현재 Python 파일의 경로를 담고 있는 특수 변수이다.

```python
print(__file__)
```

예시:

```text
/Volumes/data/projects/AI-Data-Platform/labs/rag/09_extract_pdf.py
```

이 값을 기준으로 경로를 잡으면 터미널을 어디서 실행하든 비교적 안정적으로 파일 위치를 찾을 수 있다.

---

## 11.4 `resolve()`

`resolve()`는 상대경로를 절대경로로 바꿔준다.

```python
Path(__file__).resolve()
```

예를 들어 상대경로가 다음과 같다면:

```text
09_extract_pdf.py
```

`resolve()` 후에는 다음처럼 전체 경로가 된다.

```text
/Volumes/data/projects/AI-Data-Platform/labs/rag/09_extract_pdf.py
```

절대경로를 사용하면 디버깅할 때 현재 어떤 파일을 기준으로 동작하는지 명확히 볼 수 있다.

---

## 11.5 `parent`

`parent`는 현재 경로의 상위 디렉터리를 의미한다.

```python
BASE_DIR = Path(__file__).resolve().parent
```

예를 들어 파일 경로가 다음과 같다면:

```text
/AI-Data-Platform/labs/rag/09_extract_pdf.py
```

`parent`는 다음 경로가 된다.

```text
/AI-Data-Platform/labs/rag
```

즉, `BASE_DIR`은 현재 Python 파일이 들어 있는 폴더를 의미한다.

RAG 실습에서는 이 기준으로 하위 폴더를 잡는다.

```python
RAW_DOCS_DIR = BASE_DIR / "raw_docs"
EXTRACTED_TEXT_DIR = BASE_DIR / "extracted_text"
CHROMA_DIR = BASE_DIR / "chroma_db"
```

이렇게 하면 실습 파일 위치를 기준으로 폴더 구조를 안정적으로 사용할 수 있다.

---

## 11.6 디렉터리 생성

```python
EXTRACTED_TEXT_DIR.mkdir(parents=True, exist_ok=True)
```

의미는 다음과 같다.

```text
EXTRACTED_TEXT_DIR 경로에 디렉터리를 생성한다.
상위 디렉터리가 없으면 함께 생성한다.
이미 디렉터리가 있어도 오류를 발생시키지 않는다.
```

옵션 설명:

| 옵션 | 의미 |
|---|---|
| `parents=True` | 필요한 상위 디렉터리까지 함께 생성 |
| `exist_ok=True` | 이미 존재해도 오류를 내지 않음 |

예를 들어 다음 경로를 만들려고 한다.

```text
output/jsonl/result.jsonl
```

그런데 `output` 폴더도 없고 `jsonl` 폴더도 없으면 일반 생성은 실패할 수 있다.  
`parents=True`를 주면 중간 폴더까지 함께 만든다.

---

## 11.7 파일인지 확인하기

```python
if path.is_file():
    print("파일입니다.")
```

`path.is_file()`은 해당 경로가 파일인지 확인한다.

폴더인지 확인할 때는 다음을 사용한다.

```python
if path.is_dir():
    print("디렉터리입니다.")
```

파일 처리 코드에서는 보통 다음처럼 사용한다.

```python
for path in INPUT_DIR.iterdir():
    if not path.is_file():
        continue

    print(path)
```

의미:

```text
INPUT_DIR 안의 항목을 하나씩 확인한다.
파일이 아니면 건너뛴다.
파일이면 처리한다.
```

---

## 11.8 확장자 확인하기

`path.suffix`는 파일 확장자를 반환한다.

```python
path = Path("sample.PDF")
print(path.suffix)
```

출력:

```text
.PDF
```

대소문자를 구분하지 않으려면 `lower()`를 함께 사용한다.

```python
print(path.suffix.lower())
```

출력:

```text
.pdf
```

RAG 실습에서 자주 보는 패턴이다.

```python
lower_extensions = (".txt", ".md", ".pdf")

if path.is_file() and path.suffix.lower() in lower_extensions:
    print("처리 대상 파일")
```

의미:

```text
path가 파일이고
확장자가 처리 대상 목록에 포함되면
처리한다.
```

---

# 12. 파일 읽기와 쓰기

## 12.1 파일 열기 기본

파일을 쓸 때는 다음처럼 작성한다.

```python
with path.open("w", encoding="utf-8") as f:
    f.write("hello")
```

이 코드에는 여러 의미가 들어 있다.

```text
path 위치의 파일을 연다.
쓰기 모드("w")로 연다.
문자 인코딩은 utf-8을 사용한다.
열린 파일을 f라는 이름으로 사용한다.
작업이 끝나면 자동으로 파일을 닫는다.
```

---

## 12.2 파일 모드

| 모드 | 의미 | 기존 파일이 있을 때 |
|---|---|---|
| `"r"` | 읽기 | 파일이 없으면 오류 |
| `"w"` | 쓰기 | 기존 내용 삭제 후 새로 씀 |
| `"a"` | 추가 | 기존 내용 뒤에 추가 |
| `"b"` | 바이너리 | 이미지, PDF 같은 바이너리 처리 |

가장 주의할 것은 `"w"` 모드이다.

```python
path.open("w")
```

`"w"` 모드는 기존 파일이 있으면 내용을 모두 지우고 새로 쓴다.  
즉, append가 아니라 overwrite이다.

기존 파일 뒤에 추가하려면 `"a"`를 사용한다.

```python
path.open("a")
```

JSONL 파일을 매번 새로 만들려면 `"w"`가 적합하다.  
로그처럼 계속 추가하려면 `"a"`가 적합하다.

---

## 12.3 with 문

```python
with path.open("w", encoding="utf-8") as f:
    f.write("hello")
```

`with` 문은 파일을 안전하게 열고 닫기 위한 문법이다.

파일은 열었으면 닫아야 한다.  
직접 닫는 방식은 다음과 같다.

```python
f = open("sample.txt", "w", encoding="utf-8")
try:
    f.write("hello")
finally:
    f.close()
```

하지만 매번 이렇게 쓰면 번거롭다.  
`with` 문을 사용하면 작업이 끝났을 때 자동으로 닫아준다.

```python
with open("sample.txt", "w", encoding="utf-8") as f:
    f.write("hello")
```

파일 처리에서는 `with` 문을 사용하는 습관이 좋다.

---

## 12.4 텍스트 파일 읽기

```python
path = Path("sample.txt")

with path.open("r", encoding="utf-8") as f:
    text = f.read()
```

`read()`는 파일 전체 내용을 문자열로 읽는다.

파일이 작으면 편리하지만, 매우 큰 파일이면 메모리를 많이 사용할 수 있다.  
큰 파일을 한 줄씩 읽을 때는 다음처럼 한다.

```python
with path.open("r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
```

JSONL 파일은 한 줄에 하나의 JSON 객체가 들어 있으므로 줄 단위 처리가 잘 맞는다.

---

## 12.5 JSONL 쓰기 예시

```python
import json
from pathlib import Path

records = [
    {"page": 1, "text": "첫 번째 페이지"},
    {"page": 2, "text": "두 번째 페이지"},
]

path = Path("output.jsonl")

with path.open("w", encoding="utf-8") as f:
    for record in records:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
```

이 코드는 다음을 수행한다.

```text
records 목록에서 dict를 하나씩 꺼낸다.
각 dict를 JSON 문자열로 변환한다.
한 줄에 하나씩 파일에 쓴다.
마지막에 줄바꿈(\n)을 붙인다.
```

`"\n"`을 붙이지 않으면 모든 JSON이 한 줄에 붙어서 저장되어 JSONL 형식이 깨진다.

---

# 13. JSON과 JSONL

## 13.1 JSON이란?

JSON은 데이터를 key-value 구조로 표현하는 텍스트 형식이다.

```json
{
  "name": "Python",
  "type": "language"
}
```

Python의 dict와 모양이 비슷하다.

Python dict:

```python
data = {
    "name": "Python",
    "type": "language",
}
```

JSON은 시스템 간 데이터를 주고받을 때 많이 사용한다.  
LLM API 호출, Ollama 응답, ChromaDB 메타데이터, 설정 파일 등에서 자주 만난다.

---

## 13.2 `json.dumps()`

`json.dumps()`는 Python 객체를 JSON 문자열로 변환한다.

```python
import json

record = {"name": "김장관", "role": "이사"}
text = json.dumps(record, ensure_ascii=False)
print(text)
```

출력:

```json
{"name": "김장관", "role": "이사"}
```

`ensure_ascii=False`를 사용하는 이유는 한글을 그대로 저장하기 위해서이다.

만약 `ensure_ascii=True`이면 한글이 다음처럼 유니코드 이스케이프 형태로 저장될 수 있다.

```json
{"name": "\uae40\uc7a5\uad00"}
```

기계적으로는 문제 없지만 사람이 읽기 어렵다.  
그래서 한글 문서 처리에서는 보통 `ensure_ascii=False`를 사용한다.

---

## 13.3 `json.loads()`

`json.loads()`는 JSON 문자열을 Python 객체로 변환한다.

```python
import json

text = '{"name": "Python", "type": "language"}'
data = json.loads(text)

print(data["name"])
```

출력:

```text
Python
```

API 응답이나 JSONL 파일을 읽을 때 자주 사용한다.

---

## 13.4 JSONL이란?

JSONL은 한 줄에 JSON 객체 하나씩 저장하는 형식이다.

```jsonl
{"page": 1, "text": "첫 번째 문서"}
{"page": 2, "text": "두 번째 문서"}
{"page": 3, "text": "세 번째 문서"}
```

RAG 실습에서 JSONL을 사용하는 이유는 다음과 같다.

- 문서 Chunk를 한 줄씩 저장하기 좋다.
- 대용량 데이터를 순차적으로 읽기 좋다.
- 중간에 한 줄이 깨져도 다른 줄은 처리할 수 있다.
- Vector DB 입력 데이터로 변환하기 쉽다.

문서 Chunk 저장 예:

```jsonl
{"chunk_id": "doc1_001", "text": "첫 번째 chunk", "source": "doc1.pdf", "page": 1}
{"chunk_id": "doc1_002", "text": "두 번째 chunk", "source": "doc1.pdf", "page": 1}
```

---

# 14. 자주 나오는 문자열 함수

## 14.1 `strip()`

`strip()`은 문자열 앞뒤의 공백, 탭, 줄바꿈을 제거한다.

```python
query = "  RAG란 무엇인가요?  "
print(query.strip())
```

출력:

```text
RAG란 무엇인가요?
```

주의할 점은 가운데 공백은 제거하지 않는다는 것이다.

```python
text = "AI   Data Platform"
print(text.strip())
```

출력:

```text
AI   Data Platform
```

왜 `strip()`을 사용할까?

사용자 입력에는 의도하지 않은 공백이나 줄바꿈이 들어갈 수 있다.

```python
query = input("질문을 입력하세요: ").strip()
```

이렇게 하면 사용자가 앞뒤에 공백을 넣어도 실제 질문만 사용할 수 있다.

RAG 실습에서는 빈 질문을 검사할 때도 자주 사용한다.

```python
if not query.strip():
    raise ValueError("검색 질문이 비어 있습니다.")
```

---

## 14.2 `lower()`

`lower()`는 문자열을 소문자로 변환한다.

```python
ext = ".PDF"
print(ext.lower())
```

출력:

```text
.pdf
```

파일 확장자를 비교할 때 매우 자주 사용한다.

```python
if path.suffix.lower() == ".pdf":
    print("PDF 파일")
```

사용자가 파일명을 `sample.PDF`, `sample.pdf`, `sample.Pdf` 등으로 만들 수 있기 때문에, 확장자 비교 전 소문자로 통일하면 안전하다.

---

## 14.3 `join()`

`join()`은 여러 문자열을 하나의 문자열로 합친다.

```python
words = ["RAG", "검색", "LLM"]
text = " ".join(words)
print(text)
```

출력:

```text
RAG 검색 LLM
```

여기서 `" "`는 문자열 사이에 넣을 구분자이다.

다음처럼 하면 쉼표로 합친다.

```python
text = ", ".join(words)
```

출력:

```text
RAG, 검색, LLM
```

명령행 인자를 하나의 질문 문자열로 합칠 때 자주 사용한다.

```python
query = " ".join(sys.argv[1:]).strip()
```

의미:

```text
명령행 인자 중 파일명을 제외한 나머지를
공백으로 이어 붙이고
앞뒤 공백을 제거한다.
```

---

## 14.4 `replace()`

`replace()`는 문자열 일부를 다른 문자열로 바꾼다.

```python
text = "hello world"
print(text.replace("world", "Python"))
```

출력:

```text
hello Python
```

문서 전처리에서 줄바꿈이나 특수 문자를 정리할 때 사용할 수 있다.

```python
text = text.replace("\r\n", "\n")
```

---

## 14.5 `split()`

`split()`은 문자열을 나누어 list로 만든다.

```python
text = "RAG 검색 LLM"
words = text.split()
print(words)
```

출력:

```python
['RAG', '검색', 'LLM']
```

구분자를 지정할 수도 있다.

```python
text = "pdf,docx,txt"
items = text.split(",")
```

출력:

```python
['pdf', 'docx', 'txt']
```

---

# 15. 리스트 슬라이싱

## 15.1 슬라이싱 기본

슬라이싱은 list나 문자열의 일부를 잘라내는 문법이다.

```python
values = ["python", "08_first_rag.py", "RAG", "질문"]
print(values[1:])
```

출력:

```python
["08_first_rag.py", "RAG", "질문"]
```

`[1:]`은 인덱스 1부터 끝까지 가져오라는 뜻이다.

기본 형태는 다음과 같다.

```python
values[start:end]
```

- `start`: 시작 인덱스, 포함
- `end`: 끝 인덱스, 미포함

예시:

```python
values = ["a", "b", "c", "d"]

print(values[0:2])
```

출력:

```python
["a", "b"]
```

인덱스 0부터 2 전까지 가져온다.

---

## 15.2 `sys.argv[1:]`를 사용하는 이유

```python
import sys

query = " ".join(sys.argv[1:]).strip()
```

`sys.argv`에는 명령행에서 입력한 값들이 list로 들어간다.

예시 실행:

```bash
python 08_first_rag.py RAG란 무엇인가요?
```

`sys.argv` 내용은 다음과 비슷하다.

```python
[
    "08_first_rag.py",
    "RAG란",
    "무엇인가요?"
]
```

첫 번째 값은 Python 파일명이다.  
실제 질문은 그 다음부터이다.

그래서 `sys.argv[1:]`를 사용한다.

```python
sys.argv[1:]
```

결과:

```python
["RAG란", "무엇인가요?"]
```

이것을 공백으로 합치면 질문 문자열이 된다.

```python
" ".join(sys.argv[1:])
```

결과:

```text
RAG란 무엇인가요?
```

---

# 16. in 연산자

## 16.1 포함 여부 확인

`in`은 어떤 값이 포함되어 있는지 확인하는 연산자이다.

```python
extensions = (".txt", ".md", ".pdf")

if ".pdf" in extensions:
    print("PDF 파일입니다")
```

출력:

```text
PDF 파일입니다
```

list, tuple, set, dict, 문자열에서 사용할 수 있다.

```python
print("RAG" in "RAG 검색 시스템")
```

출력:

```text
True
```

---

## 16.2 파일 확장자 검사에서 사용

RAG 실습에서 자주 보는 패턴이다.

```python
lower_extensions = (".txt", ".md", ".pdf")

if path.is_file() and path.suffix.lower() in lower_extensions:
    print("처리 대상 파일")
```

의미:

```text
path가 파일이고
파일 확장자를 소문자로 바꾼 값이
처리 대상 확장자 목록에 포함되어 있으면
처리한다.
```

이 코드를 풀어 쓰면 다음과 같다.

```python
is_real_file = path.is_file()
extension = path.suffix.lower()
is_allowed_extension = extension in lower_extensions

if is_real_file and is_allowed_extension:
    print("처리 대상 파일")
```

짧은 코드지만 여러 의미가 압축되어 있다.

---

# 17. 리스트 컴프리헨션과 제너레이터

## 17.1 리스트 컴프리헨션

리스트 컴프리헨션은 반복문을 짧게 써서 list를 만드는 문법이다.

일반 반복문:

```python
numbers = [1, 2, 3]
squares = []

for n in numbers:
    squares.append(n * n)

print(squares)
```

리스트 컴프리헨션:

```python
numbers = [1, 2, 3]
squares = [n * n for n in numbers]
print(squares)
```

출력:

```python
[1, 4, 9]
```

처음에는 일반 반복문이 이해하기 쉽다.  
코드에 익숙해지면 리스트 컴프리헨션이 더 간결하게 느껴진다.

---

## 17.2 조건이 있는 리스트 컴프리헨션

```python
numbers = [1, 2, 3, 4, 5]
evens = [n for n in numbers if n % 2 == 0]
print(evens)
```

출력:

```python
[2, 4]
```

파일 목록 필터링에도 사용할 수 있다.

```python
pdf_files = [path for path in input_dir.iterdir() if path.suffix.lower() == ".pdf"]
```

다만 초보 단계에서는 너무 복잡한 컴프리헨션보다 일반 `for` 문으로 풀어 쓰는 것이 좋다.

---

## 17.3 제너레이터 표현식

제너레이터는 값을 한 번에 모두 만들지 않고 필요할 때 하나씩 만든다.

```python
numbers = (n * n for n in range(3))
```

list 컴프리헨션과 모양이 비슷하지만 대괄호가 아니라 소괄호를 사용한다.

```python
[n * n for n in range(3)]  # list
(n * n for n in range(3))  # generator
```

제너레이터는 대용량 데이터를 처리할 때 메모리를 아낄 수 있다.

---

## 17.4 `tuple(ext.lower() for ext in extensions)`

```python
lower_extensions = tuple(ext.lower() for ext in extensions)
```

이 코드는 처음 보면 헷갈린다.  
단계별로 풀어보면 다음과 같다.

원본:

```python
extensions = [".PDF", ".DOCX", ".TXT"]
```

반복하면서 소문자로 바꾸기:

```python
for ext in extensions:
    print(ext.lower())
```

출력:

```text
.pdf
.docx
.txt
```

그 결과를 tuple로 만들기:

```python
lower_extensions = tuple(ext.lower() for ext in extensions)
```

결과:

```python
(".pdf", ".docx", ".txt")
```

즉, 전체 의미는 다음과 같다.

```text
extensions에 들어 있는 확장자를 하나씩 꺼낸다.
각 확장자를 소문자로 바꾼다.
그 결과를 tuple로 묶는다.
```

---

# 18. 예외 처리

## 18.1 예외 처리가 필요한 이유

프로그램은 항상 정상적인 입력만 받지 않는다.

예를 들어 다음 상황이 발생할 수 있다.

- 파일이 없다.
- PDF에서 텍스트가 추출되지 않는다.
- ChromaDB 컬렉션이 없다.
- Ollama 모델이 설치되어 있지 않다.
- API 호출이 실패한다.
- 사용자가 빈 질문을 입력한다.

이런 상황을 처리하지 않으면 프로그램이 갑자기 중단된다.  
예외 처리는 오류 상황을 예상하고 더 친절하게 처리하기 위한 문법이다.

---

## 18.2 try / except

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("0으로 나눌 수 없습니다.")
```

`try` 안에는 오류가 발생할 수 있는 코드를 넣는다.  
`except` 안에는 오류가 발생했을 때 실행할 코드를 넣는다.

RAG 실습에서는 LLM API 호출에서 사용할 수 있다.

```python
try:
    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"Ollama 호출 실패: {e}")
```

---

## 18.3 raise

`raise`는 직접 오류를 발생시킬 때 사용한다.

```python
if not query.strip():
    raise ValueError("검색 질문이 비어 있습니다.")
```

이렇게 하면 잘못된 입력을 초기에 막을 수 있다.

`raise`를 사용하는 이유는 다음과 같다.

```text
잘못된 상태로 계속 진행하는 것보다
문제가 생긴 지점에서 명확히 멈추는 것이 낫다.
```

예를 들어 질문이 비어 있는데 검색을 계속하면 ChromaDB 검색 결과가 이상하게 나오거나 이후 단계에서 더 헷갈리는 오류가 생길 수 있다.

초기에 명확한 메시지로 멈추면 원인을 찾기 쉽다.

---

## 18.4 예외 메시지는 구체적으로 작성한다

나쁜 예:

```python
raise RuntimeError("오류 발생")
```

좋은 예:

```python
raise RuntimeError(
    f"컬렉션은 존재하지만 저장된 문서가 없습니다: {COLLECTION_NAME}\n"
    "03_insert_to_chroma.py 실행 결과를 다시 확인하세요."
)
```

좋은 오류 메시지는 다음 정보를 포함한다.

- 무엇이 문제인지
- 어떤 값에서 문제가 났는지
- 사용자가 다음에 무엇을 확인해야 하는지

실습 문서에서는 오류 메시지를 학습용으로 자세히 작성하는 것이 좋다.

---

# 19. 외부 라이브러리 사용 이해

## 19.1 외부 라이브러리가 필요한 이유

Python은 기본 기능만으로도 많은 일을 할 수 있지만, AI / RAG 실습에는 외부 라이브러리가 필요하다.

| 라이브러리 | 역할 |
|---|---|
| `pypdf` | PDF 파일에서 텍스트 추출 |
| `python-docx` | DOCX 문서 읽기 |
| `openpyxl` | XLSX 엑셀 파일 읽기/쓰기 |
| `sentence-transformers` | 문장을 임베딩 벡터로 변환 |
| `chromadb` | 벡터 DB 저장 및 검색 |
| `requests` | HTTP API 호출 |
| `json` | JSON 변환 |
| `pathlib` | 파일 경로 처리 |

`json`, `pathlib`는 Python 표준 라이브러리이므로 별도 설치가 필요 없다.  
반면 `chromadb`, `sentence-transformers`, `pypdf` 등은 설치가 필요하다.

---

## 19.2 ModuleNotFoundError

외부 라이브러리가 설치되지 않았는데 import하면 다음 오류가 발생한다.

```text
ModuleNotFoundError: No module named 'chromadb'
```

해결 방법:

```bash
python -m pip install chromadb
```

가상환경을 사용 중이라면 반드시 가상환경이 활성화된 상태에서 설치해야 한다.

확인:

```bash
which python
python -m pip show chromadb
```

---

## 19.3 라이브러리를 볼 때 확인할 것

새로운 라이브러리를 만나면 다음을 확인하면 된다.

```text
1. 이 라이브러리는 무엇을 하기 위한 것인가?
2. 표준 라이브러리인가, 외부 라이브러리인가?
3. pip 설치가 필요한가?
4. 어떤 클래스를 import하는가?
5. 반환값은 어떤 형태인가?
```

예를 들어:

```python
from pypdf import PdfReader
```

확인할 내용:

```text
pypdf는 PDF를 읽기 위한 외부 라이브러리이다.
PdfReader는 PDF 파일을 읽는 클래스이다.
reader.pages로 페이지 목록에 접근할 수 있다.
page.extract_text()로 페이지 텍스트를 추출할 수 있다.
```

---

# 20. RAG 실습 코드에서 자주 나오는 개념

## 20.1 문서 Chunk

Chunk는 긴 문서를 작은 조각으로 나눈 단위이다.

```text
문서 전체
  ↓
Chunk 1
Chunk 2
Chunk 3
```

LLM은 긴 문서를 한 번에 모두 처리하기 어렵다.  
또한 사용자의 질문과 관련 있는 부분만 찾아야 하므로 문서를 적당한 크기로 나누어 저장한다.

예를 들어 사내 규정 문서 전체가 100페이지라면, 질문 하나에 100페이지 전체를 LLM에 넣는 것은 비효율적이다.

대신 문서를 Chunk로 나눈 뒤 질문과 관련 있는 Chunk만 검색해서 LLM에 전달한다.

---

## 20.2 Embedding

Embedding은 문장을 숫자 벡터로 바꾸는 과정이다.

```text
"RAG란 무엇인가요?"
  ↓
[0.12, -0.34, 0.56, ...]
```

컴퓨터는 문장의 의미를 직접 이해하지 못한다.  
Embedding 모델은 문장의 의미를 숫자 배열로 표현한다.

이렇게 하면 문장끼리 의미적으로 얼마나 비슷한지 계산할 수 있다.

예:

```text
"RAG란 무엇인가요?"
"검색 증강 생성이란 무엇인가요?"
```

두 문장은 단어는 다르지만 의미가 비슷하다.  
Embedding을 사용하면 이런 의미적 유사성을 계산할 수 있다.

---

## 20.3 Vector DB

Vector DB는 Embedding 벡터를 저장하고 검색하는 데이터베이스이다.

일반 DB가 다음처럼 데이터를 저장한다면:

```text
id | name | age
```

Vector DB는 다음처럼 벡터를 중심으로 저장한다.

```text
id | document | embedding | metadata
```

사용자 질문도 Embedding으로 변환한 뒤, Vector DB에서 가장 유사한 문서 Chunk를 찾는다.

RAG 실습에서는 ChromaDB를 사용한다.

---

## 20.4 collection

ChromaDB에서 `collection`은 일반 DB의 테이블과 비슷하게 이해하면 된다.

```python
collection = client.get_collection("microserver_docs")
```

`microserver_docs`라는 컬렉션 안에 문서 Chunk와 Embedding이 저장되어 있다고 보면 된다.

검색은 다음처럼 수행한다.

```python
results = collection.query(
    query_embeddings=query_embedding,
    n_results=3,
    include=["documents", "metadatas", "distances"],
)
```

의미:

```text
query_embedding과 유사한 벡터를 가진 문서를
상위 3개 검색하고
문서 내용, 메타데이터, 거리값을 함께 반환하라.
```

---

## 20.5 query_embeddings

```python
query_embeddings=query_embedding
```

이 코드는 사용자 질문 자체를 넘기는 것이 아니다.  
사용자 질문을 Embedding 모델로 벡터화한 값을 넘기는 것이다.

흐름은 다음과 같다.

```text
사용자 질문
  ↓
Embedding 모델
  ↓
query_embedding
  ↓
ChromaDB query
  ↓
유사 문서 검색
```

따라서 `query_embeddings`는 "검색 기준이 되는 질문 벡터"라고 이해하면 된다.

---

# 21. PDF 텍스트 추출에서 주의할 점

## 21.1 일반 PDF와 스캔 PDF

PDF라고 해서 항상 텍스트를 추출할 수 있는 것은 아니다.

| PDF 유형 | 설명 | 일반 텍스트 추출 |
|---|---|---|
| 텍스트 기반 PDF | 내부에 글자 정보가 있음 | 가능 |
| 이미지 스캔 PDF | 종이를 이미지로 스캔한 형태 | 어려움 |
| 표/그림 중심 PDF | 레이아웃이 복잡함 | 일부 누락 가능 |

텍스트 기반 PDF는 다음 코드로 텍스트가 추출될 수 있다.

```python
text = page.extract_text()
```

하지만 이미지 스캔 PDF는 사람이 보기에는 글자가 보여도, 내부적으로는 이미지일 수 있다.  
이 경우 `extract_text()` 결과가 비어 있을 수 있다.

---

## 21.2 `page.extract_text() or ""`

```python
text = page.extract_text() or ""
```

의미:

```text
PDF 페이지에서 텍스트를 추출한다.
추출 결과가 None이거나 비어 있으면 빈 문자열로 대체한다.
```

왜 이렇게 할까?

`page.extract_text()`가 `None`을 반환하면 뒤에서 문자열 처리를 할 때 오류가 날 수 있다.

예를 들어:

```python
text = None
cleaned = text.strip()
```

이 코드는 오류가 발생한다.

```text
AttributeError: 'NoneType' object has no attribute 'strip'
```

그래서 안전하게 빈 문자열로 바꾼다.

```python
text = page.extract_text() or ""
```

이후에는 다음처럼 문자열 함수 사용이 가능하다.

```python
text = text.strip()
```

---

## 21.3 PDF 추출 결과가 0건일 때 확인할 것

PDF 텍스트 추출 결과가 0건이면 다음을 확인한다.

```text
1. 입력 폴더 경로가 맞는가?
2. PDF 파일이 실제로 해당 폴더에 있는가?
3. 확장자가 .pdf로 인식되는가?
4. path.suffix.lower() 조건에 포함되는가?
5. PDF가 텍스트 기반인가, 이미지 스캔 PDF인가?
6. 추출 후 text.strip() 결과가 비어 있지는 않은가?
```

특히 스캔 PDF라면 일반 파서로는 텍스트가 나오지 않을 수 있다.  
이 경우 OCR 또는 Vision LLM 기반 처리가 필요하다.

---

# 22. 코드 읽을 때 꼭 보는 순서

## 22.1 초보자는 main()부터 보는 것이 좋다

Python 파일을 처음부터 끝까지 순서대로 읽으면 함수 정의가 많아서 길을 잃기 쉽다.

먼저 다음 코드를 찾는다.

```python
if __name__ == "__main__":
    main()
```

그 다음 `main()` 함수를 찾는다.

```python
def main() -> None:
    ...
```

`main()` 안에 실제 실행 순서가 들어 있는 경우가 많다.

---

## 22.2 실습 코드 분석 순서

```text
1. 파일명 확인
2. 이 파일의 목적 추정
3. import 목록 확인
4. 상수 확인
5. main() 확인
6. main()에서 호출하는 함수 순서 확인
7. 각 함수의 입력과 출력 확인
8. 파일을 읽는지, 쓰는지 확인
9. 외부 API를 호출하는지 확인
10. 최종 출력이 무엇인지 확인
```

예를 들어 `09_extract_pdf.py`라면 다음처럼 볼 수 있다.

```text
파일명: 09_extract_pdf.py
목적: PDF에서 텍스트 추출
입력: PDF 파일
출력: pdf_extracted.jsonl
주요 라이브러리: pypdf
핵심 함수: PdfReader, page.extract_text()
주의: 스캔 PDF는 텍스트가 안 나올 수 있음
```

---

# 23. 실습 코드에 주석을 달 때 권장 방식

## 23.1 좋은 주석은 "번역"이 아니라 "의도 설명"이다

나쁜 주석:

```python
count += 1  # count에 1을 더한다
```

이 주석은 코드만 봐도 알 수 있는 내용이다.

좋은 주석:

```python
count += 1  # 실제로 JSONL에 저장한 record 수를 누적한다
```

좋은 주석은 코드가 "무엇을 하는지"보다 "왜 하는지"를 설명한다.

---

## 23.2 함수 주석에 포함하면 좋은 내용

```text
1. 이 함수의 목적
2. 입력 파라미터의 의미
3. 반환값의 의미
4. 파일을 읽는지, 쓰는지
5. 기존 파일을 덮어쓰는지, 추가하는지
6. 오류가 발생할 수 있는 상황
7. RAG 전체 흐름에서의 역할
```

예시:

```python
def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> int:
    """
    records에 담긴 여러 dict 데이터를 JSONL 파일로 저장한다.

    처리 방식:
    - records에서 dict 데이터를 하나씩 꺼낸다.
    - 각 dict를 JSON 문자열로 변환한다.
    - 한 줄에 하나의 JSON 객체가 오도록 줄바꿈을 붙여 저장한다.

    파라미터:
    - path: 저장할 JSONL 파일 경로
    - records: 한 줄씩 저장할 dict 데이터 목록

    반환값:
    - 실제로 저장한 record 개수

    주의:
    - path.open("w")를 사용하므로 기존 파일이 있으면 내용을 덮어쓴다.
    - 기존 파일 뒤에 추가하려면 "a" 모드를 사용해야 한다.

    RAG 흐름에서의 역할:
    - 추출된 문서 텍스트나 Chunk 결과를 다음 단계에서 읽을 수 있도록
      JSONL 파일로 저장한다.
    """
```

---

# 24. Python 초보자가 자주 헷갈리는 내용 정리

| 헷갈리는 내용 | 핵심 정리 |
|---|---|
| `main()` | Python에서 자동 실행되는 이름이 아니다. 직접 호출해야 한다. |
| `if __name__ == "__main__"` | 파일을 직접 실행했을 때만 main()을 호출하기 위한 구조이다. |
| `sys.argv[1:]` | 명령행 인자 중 파일명을 제외한 실제 입력값만 가져온다. |
| `strip()` | 문자열 양쪽 공백만 제거한다. 가운데 공백은 제거하지 않는다. |
| `tuple` | 변경 불가능한 순서형 자료구조이다. map이 아니다. |
| `dict` | key-value 구조이다. Java의 Map과 비슷하다. |
| `in` | 포함 여부를 확인한다. |
| `with open()` | 파일을 열고 작업 후 자동으로 닫는다. |
| `"w"` 모드 | 기존 파일 내용을 삭제하고 새로 쓴다. |
| `"a"` 모드 | 기존 파일 뒤에 내용을 추가한다. |
| `Path(__file__)` | 현재 Python 파일의 경로를 의미한다. |
| `or ""` | 앞의 값이 None이거나 비어 있으면 빈 문자열을 사용한다. |
| `type hint` | 강제 타입 검사가 아니라 코드 이해와 IDE 지원을 위한 힌트이다. |
| `list comprehension` | 반복문으로 list를 만드는 짧은 문법이다. |
| `generator` | 값을 한 번에 모두 만들지 않고 필요할 때 하나씩 만든다. |

---

# 25. Python 학습 우선순위

RAG / AI Agent 실습을 계속하기 위해서는 다음 순서로 익히는 것이 좋다.

## 25.1 1단계: 기본 문법

- 변수
- 문자열
- list
- dict
- tuple
- set
- 조건문
- 반복문
- 함수

이 단계의 목표는 코드를 보고 "대략 무엇을 하는지" 이해하는 것이다.

---

## 25.2 2단계: 실행 구조

- Python 파일 실행
- `main()` 함수
- `if __name__ == "__main__"`
- `import`
- 모듈 분리

이 단계의 목표는 "프로그램이 어디서 시작해서 어떤 순서로 실행되는지" 파악하는 것이다.

---

## 25.3 3단계: 파일 처리

- `pathlib.Path`
- 파일 읽기
- 파일 쓰기
- JSON
- JSONL
- 디렉터리 생성
- 확장자 필터링

RAG는 문서를 다루는 실습이므로 파일 처리가 매우 중요하다.

---

## 25.4 4단계: 실습 필수 라이브러리

- `pypdf`
- `python-docx`
- `openpyxl`
- `sentence-transformers`
- `chromadb`
- `requests`

이 단계의 목표는 라이브러리 내부를 모두 이해하는 것이 아니다.  
먼저 "무슨 역할을 하는 라이브러리인지"를 이해하면 된다.

---

## 25.5 5단계: AI 실습 개념

- Chunk
- Embedding
- Vector DB
- Similarity Search
- Prompt
- LLM API 호출
- RAG 답변 생성

Python 문법을 어느 정도 이해했다면, 그다음은 AI 실습 흐름을 이해해야 한다.

---

# 26. 실습 코드 분석 템플릿

새로운 Python 실습 파일을 볼 때 아래 양식으로 정리하면 이해가 빠르다.

```markdown
## 파일명

## 이 파일의 목적

## 입력 데이터

## 출력 데이터

## 주요 라이브러리

## 주요 상수

## 주요 함수

## 실행 흐름

1.
2.
3.

## 헷갈리는 코드

## 오류가 발생할 수 있는 부분

## RAG 전체 흐름에서의 역할
```

예시:

```markdown
## 파일명

09_extract_pdf.py

## 이 파일의 목적

PDF 파일에서 텍스트를 추출하여 JSONL로 저장한다.

## 입력 데이터

raw_docs 폴더의 PDF 파일

## 출력 데이터

extracted_text/pdf_extracted.jsonl

## 주요 라이브러리

pypdf.PdfReader

## 주요 함수

- extract_pdf_text()
- write_jsonl()
- main()

## 실행 흐름

1. 입력 폴더 확인
2. PDF 파일 목록 조회
3. PDF 페이지별 텍스트 추출
4. 추출 결과를 JSONL로 저장
5. 처리 건수 출력

## 오류가 발생할 수 있는 부분

- PDF 파일이 없는 경우
- PDF가 스캔 이미지라 텍스트가 추출되지 않는 경우
- 출력 폴더가 없는 경우
```

---

# 27. RAG 실습 파일을 읽는 예시 흐름

예를 들어 `08_first_rag.py` 같은 파일을 읽는다면 다음 순서로 보면 된다.

```text
1. 파일명으로 목적을 추정한다.
2. import 목록을 보고 어떤 라이브러리를 쓰는지 확인한다.
3. MODEL_NAME, COLLECTION_NAME 같은 상수를 확인한다.
4. main() 함수를 찾는다.
5. main() 안에서 호출되는 함수 순서를 본다.
6. 사용자 질문을 어디서 받는지 확인한다.
7. 질문을 임베딩하는 부분을 찾는다.
8. ChromaDB에서 검색하는 부분을 찾는다.
9. 검색 결과를 prompt에 넣는 부분을 찾는다.
10. Ollama 또는 LLM API를 호출하는 부분을 찾는다.
11. 최종 답변을 출력하는 부분을 확인한다.
```

이 순서를 따르면 코드가 길어도 길을 잃지 않는다.

---

# 28. 실습에서 자주 만나는 코드 패턴 해설

## 28.1 명령행 인자 또는 입력값 받기

```python
if len(sys.argv) >= 2:
    query = " ".join(sys.argv[1:]).strip()
else:
    query = input("질문을 입력하세요: ").strip()
```

의미:

```text
명령행에서 질문을 입력했다면 그 값을 사용한다.
명령행 인자가 없다면 input()으로 직접 질문을 입력받는다.
```

예시 1:

```bash
python 08_first_rag.py RAG란 무엇인가요?
```

이 경우 `sys.argv[1:]`를 사용한다.

예시 2:

```bash
python 08_first_rag.py
```

이 경우 입력창에 직접 질문을 입력한다.

이 패턴은 실습 편의성을 높이기 위한 것이다.

---

## 28.2 빈 질문 검사

```python
if not query.strip():
    raise ValueError("검색 질문이 비어 있습니다.")
```

의미:

```text
query의 앞뒤 공백을 제거했는데 비어 있으면
검색을 진행하지 말고 오류를 발생시킨다.
```

빈 질문으로 RAG 검색을 수행하면 의미 없는 결과가 나오므로 초기에 막는 것이 좋다.

---

## 28.3 출력 구분선

```python
print("=" * 80)
print("RAG 답변")
print("=" * 80)
```

`"=" * 80`은 `"="` 문자를 80번 반복한다.

출력:

```text
================================================================================
RAG 답변
================================================================================
```

실습 결과를 보기 좋게 구분하기 위한 코드이다.

---

## 28.4 `or ""`

```python
text = page.extract_text() or ""
```

이 코드는 다음을 짧게 쓴 것이다.

```python
text = page.extract_text()

if not text:
    text = ""
```

PDF 텍스트 추출 결과가 `None`일 수 있기 때문에 빈 문자열로 대체한다.

---

# 29. 앞으로 실습하면서 기억할 핵심 문장

Python은 문법 자체보다 실행 흐름을 잡는 것이 중요하다.

특히 RAG 실습에서는 다음 흐름을 계속 머릿속에 두면 코드가 훨씬 잘 보인다.

```text
문서 읽기
  ↓
텍스트 추출
  ↓
Chunk 분리
  ↓
Embedding 생성
  ↓
Vector DB 저장
  ↓
질문 입력
  ↓
질문 Embedding 생성
  ↓
유사 문서 검색
  ↓
Prompt 구성
  ↓
LLM 호출
  ↓
답변 출력
```

Python 문법은 이 흐름을 구현하기 위한 도구이다.  
따라서 코드를 볼 때 항상 다음 질문을 던지는 것이 좋다.

```text
이 줄은 RAG 흐름 중 어느 단계인가?
입력은 무엇인가?
출력은 무엇인가?
다음 단계로 어떤 값을 넘기는가?
오류가 날 수 있는 지점은 어디인가?
```

---

# 30. 마무리

Python 초보 단계에서는 모든 문법을 한 번에 외우려고 하기보다, 실습 코드에서 반복해서 등장하는 패턴을 먼저 익히는 것이 효과적이다.

우선 다음은 반드시 익혀두는 것을 권장한다.

- `main()` 실행 구조
- `if __name__ == "__main__"`
- `list`, `dict`, `tuple`, `set`
- `for`, `enumerate()`
- `Path(__file__).resolve().parent`
- `with path.open(...) as f`
- `json.dumps(..., ensure_ascii=False)`
- `sys.argv[1:]`
- `strip()`, `lower()`, `join()`
- `try except`
- 외부 라이브러리 import 방식
- 파일 경로와 확장자 처리
- JSONL 저장 구조
- RAG 전체 실행 흐름

이 정도를 이해하면 RAG 실습 파일 01번부터 15번까지의 구조를 훨씬 안정적으로 읽을 수 있다.

Python은 처음에는 낯설지만, 같은 패턴이 반복해서 등장한다.  
실습 파일을 하나씩 분석하면서 “이 코드는 왜 필요한가?”를 계속 확인하면 문법은 자연스럽게 익숙해진다.
