# ReAct

ReAct는 Reasoning과 Acting을 결합한 Agent 동작 패턴이다.

ReAct의 기본 흐름은 다음과 같다.

```text
Thought
   ↓
Action
   ↓
Observation
   ↓
Final Answer
```

Thought는 Agent가 무엇을 해야 할지 판단하는 단계이다.

Action은 도구를 선택하고 호출하는 단계이다.

Observation은 도구 실행 결과를 확인하는 단계이다.

Final Answer는 최종 답변을 생성하는 단계이다.
