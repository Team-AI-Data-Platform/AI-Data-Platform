# Tool Calling

Tool Calling은 LLM이 외부 도구 호출 요청을 구조화해서 생성하는 방식이다.

LLM은 도구를 직접 실행하지 않는다.

LLM은 다음과 같은 요청을 생성한다.

```json
{
  "tool_name": "calculator",
  "arguments": {
    "expression": "12500 * 17"
  }
}
```

실제 실행은 애플리케이션의 Tool Executor가 담당한다.
