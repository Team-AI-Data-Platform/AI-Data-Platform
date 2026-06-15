"""
Step2-2 실습

실습용 문서를 생성한다.

실제 프로젝트에서는 PDF, Word, Markdown 등의
업무 문서를 사용하지만

학습 환경에서는 실습용 문서를 자동 생성하여
이후 Chunking → Embedding → Vector DB 적재 과정을
진행한다.
"""

from pathlib import Path

# docs 디렉터리 생성
docs_dir = Path("docs")
docs_dir.mkdir(exist_ok=True)

# 생성할 파일
file_path = docs_dir / "microserver_guide.md"

content = """
# MicroServer Framework Guide

MicroServer Framework는 Spring Boot 기반의
MSA(Micro Service Architecture) 플랫폼이다.

## 주요 구성요소

- API Gateway
- Eureka Service Discovery
- Config Server
- Business Service
- Monitoring

## API Gateway

API Gateway는 모든 외부 요청의 진입점이다.

주요 기능

- Routing
- 인증 처리
- 로깅
- Rate Limit

## Eureka

서비스 등록 및 탐색 기능을 제공한다.

## Monitoring

Prometheus와 Grafana를 사용하여
서비스 상태를 모니터링한다.
"""

# 파일 생성
file_path.write_text(content, encoding="utf-8")

print("문서 생성 완료")
print(file_path.resolve())