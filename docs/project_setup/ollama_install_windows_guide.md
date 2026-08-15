# Ollama 설치 및 기본 설정 가이드 - Windows

> 이 문서는 Windows 로컬 개발환경에서 **Ollama를 설치하고 Local LLM을 실행할 수 있는 상태까지 준비하는 방법**을 설명한다.  
> 본 가이드의 범위는 Ollama 설치, 실행 확인, 기본 명령어 확인, 테스트 모델 다운로드 및 실행까지이다.  
> Python에서 Ollama를 호출하는 방법, RAG, Agent 연동 등은 `AI Lab > Step 1 Local LLM 구축`의 별도 학습 가이드에서 다룬다.

---

## 1. Ollama란?

Ollama는 Local LLM 모델을 개인 PC에서 다운로드하고 실행할 수 있도록 도와주는 도구이다.

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

Ollama 공식 문서 기준 Windows용 Ollama는 **Windows 10 이상** 환경을 지원한다.

Windows 버전은 다음 경로에서 확인할 수 있다.

```text
설정
 → 시스템
 → 정보
```

또는 PowerShell에서 다음 명령을 실행한다.

```powershell
winver
```

---

## 4. Ollama 다운로드

Windows에서는 공식 `OllamaSetup.exe` 설치 프로그램을 사용하는 방식이 가장 간단하다.

Ollama 공식 다운로드 페이지에서 Windows용 설치 프로그램을 다운로드한다.

```text
https://ollama.com/download/windows
```

공식 설치 프로그램은 일반 사용자 계정에 설치할 수 있으며, 일반적인 설치 과정에서는 관리자 권한이 필수는 아니다.

---

## 5. Ollama 설치

다운로드한 다음 파일을 실행한다.

```text
OllamaSetup.exe
```

설치 프로그램의 안내에 따라 설치를 진행한다.

설치가 완료되면 Windows 시작 메뉴에서 Ollama를 실행한다.

```text
시작 메뉴
   ↓
Ollama
   ↓
실행
```

Ollama 앱이 실행되면 백그라운드에서 Ollama 서비스가 동작하며 CLI와 API를 사용할 수 있다.

---

## 6. PowerShell 새로 실행

설치가 완료된 후 PowerShell을 새로 실행하는 것을 권장한다.

설치 이전부터 열려 있던 PowerShell에서는 새로 등록된 실행 경로가 즉시 반영되지 않을 수 있다.

PowerShell을 새로 실행한 뒤 다음 명령으로 설치 여부를 확인한다.

```powershell
ollama --version
```

정상적으로 설치되었다면 Ollama 버전이 출력된다.

예시:

```text
ollama version x.x.x
```

---

## 7. Ollama 명령어 확인

다음 명령을 실행한다.

```powershell
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

```powershell
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

```powershell
ollama pull gemma3:4b
```

모델 파일은 수 GB 이상의 저장공간을 사용할 수 있으므로 다운로드 전에 디스크 여유 공간을 확인한다.

다운로드가 완료되면 다시 확인한다.

```powershell
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

```powershell
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

다른 PowerShell 창에서 다음 명령을 실행하면 현재 메모리에 올라가 있는 모델을 확인할 수 있다.

```powershell
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

## 13. `ollama` 명령을 찾을 수 없는 경우

다음과 같은 오류가 발생할 수 있다.

```text
ollama : 'ollama' 용어가 cmdlet, 함수, 스크립트 파일 또는
실행할 수 있는 프로그램의 이름으로 인식되지 않습니다.
```

먼저 다음 항목을 확인한다.

### 13.1 PowerShell 새로 실행

Ollama 설치 전에 열려 있던 PowerShell이라면 종료 후 다시 실행한다.

### 13.2 Ollama 설치 여부 확인

Windows 시작 메뉴에서 Ollama가 설치되어 있는지 확인한다.

### 13.3 Ollama 다시 실행

시작 메뉴에서 Ollama 앱을 실행한 뒤 다시 확인한다.

```powershell
ollama --version
```

그래도 해결되지 않는 경우 Ollama를 재설치한 뒤 다시 확인한다.

---

## 14. Ollama가 실행되지 않는 경우

Ollama CLI가 설치되어 있어도 Ollama 앱 또는 서비스가 실행되지 않은 경우 API 호출이 실패할 수 있다.

Windows 시작 메뉴에서 Ollama를 실행한다.

```text
시작
 → Ollama
 → 실행
```

필요한 경우 터미널에서 직접 서버를 실행할 수도 있다.

```powershell
ollama serve
```

> Windows용 Ollama 앱을 일반적인 방식으로 사용하는 경우 백그라운드에서 Ollama가 실행되므로 `ollama serve`를 매번 직접 실행할 필요는 없다.

---

## 15. 모델 저장공간 참고

Ollama 모델은 Python 소스 코드보다 훨씬 많은 저장공간을 사용할 수 있다.

예를 들어 여러 Local LLM 모델을 설치하면 수십 GB 이상의 공간을 사용할 수 있다.

따라서 다음 항목을 고려한다.

```text
SSD 여유공간 확인
      ↓
필요한 모델 중심으로 다운로드
      ↓
사용하지 않는 모델은 필요 시 삭제
```

설치된 모델은 다음 명령으로 확인한다.

```powershell
ollama list
```

필요 없는 모델은 다음과 같이 삭제할 수 있다.

```powershell
ollama rm <모델명>
```

예:

```powershell
ollama rm gemma3:4b
```

---

## 16. 설치 완료 확인 체크리스트

다음 항목이 모두 확인되면 Windows용 Ollama 환경 구성이 완료된 것이다.

- [ ] Windows에서 Ollama 설치 완료
- [ ] Ollama 앱 실행 완료
- [ ] `ollama --version` 정상 출력
- [ ] `ollama list` 정상 실행
- [ ] 테스트 모델 다운로드 완료
- [ ] `ollama run gemma3:4b` 정상 실행
- [ ] Local LLM 응답 확인

---

## 17. 다음 단계

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
