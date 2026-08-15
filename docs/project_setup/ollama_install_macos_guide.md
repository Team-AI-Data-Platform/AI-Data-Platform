# Ollama 설치 및 기본 설정 가이드 - macOS

> 이 문서는 macOS 로컬 개발환경에서 **Ollama를 설치하고 Local LLM을 실행할 수 있는 상태까지 준비하는 방법**을 설명한다.  
> 본 가이드의 범위는 Ollama 설치, 실행 확인, 기본 명령어 확인, 테스트 모델 다운로드 및 실행까지이다.  
> Python에서 Ollama를 호출하는 방법, RAG, Agent 연동 등은 `AI Lab > Step 1 Local LLM 구축`의 별도 학습 가이드에서 다룬다.

---

## 1. Ollama란?

Ollama는 Local LLM 모델을 개인 Mac에서 다운로드하고 실행할 수 있도록 도와주는 도구이다.

대표적으로 다음과 같은 모델을 실행할 수 있다.

- Gemma
- Qwen
- Llama
- Mistral

기본 구조는 다음과 같다.

```text
사용자 / 애플리케이션
        ↓
      Ollama
        ↓
 Local LLM Model
        ↓
      Response
```

Ollama는 이후 Python, RAG, AI Agent, Open WebUI 등에서 Local LLM을 호출할 때 기반이 되는 실행 환경이다.

---

## 2. 설치 범위

이번 환경 구성 단계에서는 다음까지만 진행한다.

```text
Ollama 설치
    ↓
설치 확인
    ↓
Ollama 실행 확인
    ↓
테스트 모델 다운로드
    ↓
모델 실행 확인
    ↓
완료
```

다음 내용은 별도의 AI Lab 학습 가이드에서 다룬다.

- Ollama Python Library 연동
- Python에서 Ollama API 호출
- 여러 Local LLM 모델 비교
- RAG 연동
- AI Agent 연동
- Open WebUI 연동

---

## 3. 사전 확인

Ollama 공식 문서 기준 macOS용 Ollama는 **macOS 14 Sonoma 이상**을 요구한다.

현재 macOS 버전은 다음 경로에서 확인할 수 있다.

```text
Apple 메뉴()
 → 이 Mac에 관하여
```

터미널에서는 다음 명령으로 확인할 수 있다.

```bash
sw_vers
```

---

## 4. Ollama 다운로드

macOS에서는 Ollama 공식 문서에서 안내하는 **DMG 설치 방식**을 사용하는 것이 가장 일반적이다.

Ollama 공식 다운로드 페이지에서 macOS용 설치 파일을 다운로드한다.

```text
https://ollama.com/download/mac
```

---

## 5. Ollama 설치

다운로드한 `ollama.dmg` 파일을 연다.

설치 화면에서 Ollama 애플리케이션을 `Applications` 폴더로 이동한다.

```text
ollama.dmg
    ↓
Ollama.app
    ↓
Applications
```

설치 후 `Applications` 폴더에서 Ollama를 실행한다.

```text
응용 프로그램
   ↓
Ollama
   ↓
실행
```

---

## 6. CLI 등록 확인

Ollama 앱을 처음 실행하면 `ollama` CLI가 PATH에서 사용 가능한지 확인한다.

필요한 경우 `/usr/local/bin`에 CLI 링크를 생성하기 위한 권한을 요청할 수 있다.

허용 후 Terminal을 새로 열어 다음 명령을 실행한다.

```bash
ollama --version
```

정상적으로 설치되었다면 Ollama 버전이 출력된다.

예시:

```text
ollama version x.x.x
```

현재 Ollama 실행 파일 위치는 다음 명령으로 확인할 수 있다.

```bash
which ollama
```

정상적인 경우 다음과 비슷한 경로가 출력될 수 있다.

```text
/usr/local/bin/ollama
```

---

## 7. Ollama 명령어 확인

다음 명령을 실행한다.

```bash
ollama
```

정상적으로 설치되어 있다면 사용할 수 있는 Ollama 명령어 목록이 표시된다.

주요 명령어는 다음과 같다.

| 명령어 | 설명 |
|---|---|
| `ollama run` | 모델 실행 |
| `ollama pull` | 모델 다운로드 |
| `ollama list` | 로컬에 설치된 모델 목록 확인 |
| `ollama ps` | 현재 실행 중인 모델 확인 |
| `ollama rm` | 설치된 모델 삭제 |

---

## 8. Ollama 실행 상태 확인

다음 명령으로 현재 로컬에 설치되어 있는 모델 목록을 확인한다.

```bash
ollama list
```

처음 설치한 경우 모델이 없어서 목록이 비어 있을 수 있다.

이는 정상이다.

```text
NAME    ID    SIZE    MODIFIED
```

`ollama list` 명령이 정상적으로 실행된다면 Ollama CLI를 사용할 수 있는 상태이다.

---

## 9. 테스트 모델 다운로드

Ollama가 정상적으로 동작하는지 확인하기 위해 테스트용 Local LLM 모델을 하나 다운로드한다.

본 프로젝트에서는 비교적 가벼운 실습 모델의 예로 `gemma3:4b`를 사용할 수 있다.

```bash
ollama pull gemma3:4b
```

Local LLM 모델은 수 GB 이상의 저장공간을 사용할 수 있으므로 다운로드 전에 디스크 여유 공간을 확인한다.

다운로드가 완료되면 다음 명령으로 확인한다.

```bash
ollama list
```

예시:

```text
NAME          ID              SIZE
gemma3:4b     ........        ...
```

> 실제 모델 크기와 사용 메모리는 모델 종류, Quantization 방식 등에 따라 달라질 수 있다.

---

## 10. Local LLM 실행

다운로드한 모델을 실행한다.

```bash
ollama run gemma3:4b
```

정상적으로 실행되면 터미널에서 질문을 입력할 수 있다.

예:

```text
>>> Local LLM이 무엇인지 간단하게 설명해줘.
```

모델의 답변이 출력되면 Ollama와 Local LLM이 정상적으로 동작하는 것이다.

대화를 종료할 때는 다음 명령을 입력할 수 있다.

```text
/bye
```

---

## 11. 모델 실행 상태 확인

다른 Terminal 창에서 다음 명령을 실행하면 현재 메모리에 올라가 있는 모델을 확인할 수 있다.

```bash
ollama ps
```

모델이 실행 중이면 모델명과 관련 정보가 표시된다.

---

## 12. Ollama API 기본 주소

Ollama는 로컬에서 API Server 역할도 수행한다.

기본 API 주소는 다음과 같다.

```text
http://localhost:11434
```

이 주소는 이후 Python 프로그램이나 RAG, Agent 애플리케이션에서 Ollama를 호출할 때 사용된다.

이번 가이드에서는 API를 직접 호출하지 않는다.

연동 방법은 이후 AI Lab 학습 단계에서 다룬다.

---

## 13. `ollama: command not found` 오류가 발생하는 경우

다음과 같은 오류가 발생할 수 있다.

```text
zsh: command not found: ollama
```

먼저 다음 항목을 확인한다.

### 13.1 Terminal 새로 실행

Ollama 설치 이전부터 열려 있던 Terminal이라면 종료 후 다시 실행한다.

### 13.2 Ollama 앱 실행

`Applications` 폴더에서 Ollama 앱을 실행한다.

### 13.3 CLI 경로 확인

다음 명령을 실행한다.

```bash
which ollama
```

경로가 출력되지 않는 경우 Ollama 앱을 다시 실행하여 CLI 링크 생성 안내가 나타나는지 확인한다.

Ollama 공식 macOS 앱은 CLI가 PATH에서 발견되지 않을 경우 `/usr/local/bin`에 링크를 생성할 수 있도록 안내한다.

---

## 14. Ollama가 실행되지 않는 경우

Ollama CLI가 설치되어 있어도 Ollama 앱 또는 서버가 실행되지 않은 경우 API 호출이 실패할 수 있다.

Applications에서 Ollama를 실행한다.

```text
Applications
 → Ollama
 → 실행
```

필요한 경우 터미널에서 직접 서버를 실행할 수도 있다.

```bash
ollama serve
```

> macOS용 Ollama 앱을 일반적인 방식으로 실행하는 경우 백그라운드에서 Ollama Server가 동작하므로 `ollama serve`를 매번 직접 실행할 필요는 없다.

---

## 15. Apple Silicon과 Unified Memory 참고

Apple Silicon 기반 Mac은 CPU와 GPU가 Unified Memory를 공유한다.

Local LLM을 실행할 때는 Mac의 전체 Unified Memory 용량이 중요한 기준이 된다.

예:

```text
16GB
→ 소형 모델 및 기본 실습

24GB
→ 7B ~ 8B급 모델 중심 실습

32GB 이상
→ 8B ~ 14B급 모델 및 RAG / Agent 병행에 유리
```

> 위 구분은 학습 환경을 이해하기 위한 일반적인 참고 기준이며, 실제 사용 가능 모델 크기는 Quantization, Context Window, 동시에 실행 중인 프로그램 등에 따라 달라진다.

---

## 16. 모델 저장공간 참고

Ollama 모델은 수 GB에서 수십 GB 이상의 저장공간을 사용할 수 있다.

Ollama 공식 macOS 문서에서도 Local LLM 모델 저장을 위해 추가적인 디스크 공간이 필요할 수 있음을 안내한다.

따라서 다음 항목을 고려한다.

```text
SSD 여유공간 확인
      ↓
필요한 모델 중심으로 다운로드
      ↓
사용하지 않는 모델은 필요 시 삭제
```

설치된 모델은 다음 명령으로 확인한다.

```bash
ollama list
```

필요 없는 모델은 다음과 같이 삭제할 수 있다.

```bash
ollama rm <모델명>
```

예:

```bash
ollama rm gemma3:4b
```

---

## 17. 설치 완료 확인 체크리스트

다음 항목이 모두 확인되면 macOS용 Ollama 환경 구성이 완료된 것이다.

- [ ] macOS에서 Ollama 설치 완료
- [ ] Ollama 앱 실행 완료
- [ ] `ollama --version` 정상 출력
- [ ] `which ollama` 경로 확인
- [ ] `ollama list` 정상 실행
- [ ] 테스트 모델 다운로드 완료
- [ ] `ollama run gemma3:4b` 정상 실행
- [ ] Local LLM 응답 확인

---

## 18. 다음 단계

Ollama 설치가 완료되면 이후 AI Lab 학습 과정에서 다음 내용을 진행할 수 있다.

```text
Ollama 설치 완료
      ↓
Local LLM 기본 학습
      ↓
Python에서 Ollama 호출
      ↓
RAG 구축
      ↓
AI Agent 구축
```

환경 구성 단계에서는 **Ollama 설치와 테스트 모델 실행이 정상적으로 되는 것까지 확인하면 완료**이다.
