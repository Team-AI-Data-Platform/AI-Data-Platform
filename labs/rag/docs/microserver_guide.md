# MicroServer 개발 가이드

## 1. MicroServer 개요

MicroServer는 Spring Boot 기반의 MSA 개발 프레임워크이다.
공통 모듈, 런타임 모듈, 관리자 모듈로 구성되며 Maven 멀티모듈 구조를 사용한다.

## 2. 로컬 개발환경

로컬 개발환경은 개발자가 자신의 PC에서 MicroServer를 실행하고 테스트할 수 있도록 구성한 환경이다.
Java, Maven, STS 또는 IntelliJ, Git, 데이터베이스가 필요하다.

## 3. Maven 멀티모듈 구조

MicroServer는 여러 개의 Maven 모듈로 구성된다.
공통 기능은 module-common에 위치하며, 실행 관련 기능은 m-runtime에서 관리한다.

## 4. Lombok 적용

MicroServer는 반복적인 Getter, Setter, 생성자 코드를 줄이기 위해 Lombok을 사용한다.
개발자는 IDE에 Lombok 플러그인을 설치해야 한다.

## 5. API Gateway

API Gateway는 외부 요청을 내부 서비스로 라우팅하는 역할을 한다.
Spring Cloud Gateway를 사용할 수 있으며, 인증, 로깅, 라우팅 정책을 적용할 수 있다.