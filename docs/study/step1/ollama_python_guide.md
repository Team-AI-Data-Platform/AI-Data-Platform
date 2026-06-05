# Ollama Python 연동 가이드

## 목적
Local LLM 구축 후 Python 프로그램에서 Ollama를 호출하는 방법을 설명합니다.

## 1. 가상환경 생성

```bash
python3 -m venv .venv
```

### 명령어 설명

- python3 : Python 실행
- -m : 모듈 실행
- venv : 가상환경 생성 모듈
- .venv : 생성될 폴더명

생성 후:

```text
AI-Data-Platform
 ├── docs
 ├── mkdocs.yml
 └── .venv
```

## 2. 가상환경 활성화

```bash
source .venv/bin/activate
```

### 설명

- source : 현재 쉘에 적용
- activate : 가상환경 활성화

정상 실행 시:

```bash
(.venv) ➜
```

## 3. pip 업그레이드

```bash
python -m pip install --upgrade pip
```

### 설명

현재 가상환경 안의 pip를 최신 버전으로 업그레이드합니다.

## 4. Ollama 라이브러리 설치

```bash
python -m pip install ollama
```

### 설명

주의:

이 명령은 Ollama 서버 설치가 아닙니다.

Python 프로그램에서 Ollama API를 호출하기 위한 라이브러리를 설치하는 것입니다.

구조:

Python Program
→ Ollama Library
→ Ollama Server
→ Gemma/Qwen

## 5. 설치 확인

```bash
python -c "import ollama; print('ollama python library ok')"
```

정상 결과:

```text
ollama python library ok
```

## 6. 첫 번째 예제

파일명:

test_ollama.py

```python
from ollama import chat

response = chat(
    model='gemma3:4b',
    messages=[
        {
            'role': 'user',
            'content': 'Local LLM이 무엇인지 설명해줘'
        }
    ]
)

print(response['message']['content'])
```

실행:

```bash
python test_ollama.py
```

## 7. 내부 동작 구조

Python
↓
Ollama Library
↓
localhost:11434
↓
Gemma3 4B
↓
Response

## 8. 향후 활용

- RAG 구축
- Agent 구축
- Open WebUI 연동
- Vector DB 연동

모든 단계에서 Python을 사용하게 됩니다.
