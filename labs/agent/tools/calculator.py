from __future__ import annotations


def calculate(expression: str) -> str:
    """
    문자열로 전달된 간단한 수식을 계산한다.

    이 함수는 Agent가 사용할 수 있는 계산 Tool이다.

    Args:
        expression:
            계산할 수식 문자열.
            예: "12500 * 17"

    Returns:
        계산 결과를 문자열로 반환한다.

    Raises:
        ValueError:
            수식이 비어 있거나 허용되지 않은 문자가 포함된 경우 발생한다.

    주의:
        eval()은 임의의 Python 코드를 실행할 수 있기 때문에 실제 운영 환경에서는 위험하다.
        여기서는 Agent Tool 개념을 이해하기 위한 실습용 예제로만 사용한다.
    """
    if not expression or not expression.strip():
        raise ValueError("계산할 수식이 비어 있습니다.")

    allowed_chars = "0123456789+-*/(). "

    if any(char not in allowed_chars for char in expression):
        raise ValueError("허용되지 않은 문자가 포함되어 있습니다.")

    result = eval(expression, {"__builtins__": {}}, {})

    return str(result)
