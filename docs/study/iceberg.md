## 1. Iceberg란?

**Iceberg = Apache Iceberg**는 데이터 레이크에 저장된 파일을 **DB 테이블처럼 안전하고 빠르게 관리**하게 해주는 **오픈 테이블 포맷(Open Table Format)**입니다.

쉽게 말하면,

> **S3 / HDFS / ADLS 같은 저장소에 Parquet 파일이 흩어져 있을 때,  
> 그 파일들을 “하나의 신뢰 가능한 분석 테이블”처럼 관리해 주는 기술**입니다.

Apache Iceberg 공식 문서에서는 Iceberg를 **대규모 분석 데이터셋을 위한 Open Table Format**으로 설명합니다. Spark, Trino, Flink, Presto, Hive, Impala 같은 여러 분석 엔진이 동일한 Iceberg 테이블을 함께 사용할 수 있습니다.

공식 사이트: <https://iceberg.apache.org/>

---

## 2. 왜 필요한가?

일반적으로 데이터 레이크에는 다음과 같이 파일이 저장됩니다.

```text
S3 / HDFS / ADLS
 └── customer/
      ├── part-0001.parquet
      ├── part-0002.parquet
      ├── part-0003.parquet
```

Parquet 파일만 있으면 데이터를 저장할 수는 있지만, 운영 관점에서는 여러 문제가 발생합니다.

| 문제 | 설명 |
|---|---|
| 테이블 변경 어려움 | 컬럼 추가, 삭제, 이름 변경 관리가 복잡함 |
| 데이터 정합성 문제 | 쓰는 중인 파일을 읽거나, 일부만 반영된 상태를 볼 수 있음 |
| 과거 시점 조회 어려움 | 어제 기준 데이터, 특정 버전 데이터 조회가 어려움 |
| 파일 증가에 따른 성능 저하 | 어떤 파일을 읽어야 하는지 매번 탐색 비용 발생 |
| 여러 엔진 동시 사용 어려움 | Spark, Trino, Flink가 동시에 읽고 쓸 때 충돌 가능 |

Iceberg는 이러한 문제를 **메타데이터, 스냅샷, 매니페스트** 구조를 통해 해결합니다.

---

## 3. Iceberg의 핵심 구조

Iceberg 테이블은 실제 데이터 파일과 테이블 상태를 관리하는 메타데이터로 구성됩니다.

```text
Iceberg Table
 ├── Metadata File
 │    ├── Schema 정보
 │    ├── Partition 정보
 │    ├── 현재 Snapshot 정보
 │
 ├── Snapshot
 │    └── 특정 시점의 테이블 상태
 │
 ├── Manifest List
 │    └── 어떤 Manifest들이 필요한지 관리
 │
 ├── Manifest File
 │    └── 어떤 데이터 파일을 읽어야 하는지 관리
 │
 └── Data Files
      └── 실제 Parquet / ORC / Avro 파일
```

즉, Iceberg는 실제 데이터를 직접 저장하는 파일 포맷이라기보다는, **데이터 파일 위에 테이블 관리 계층을 얹는 기술**입니다.

---

## 4. 주요 기능

### 4.1 스키마 변경

Iceberg는 컬럼 추가, 삭제, 이름 변경, 타입 변경 등을 안전하게 관리할 수 있습니다.

예를 들어 다음과 같이 컬럼을 추가할 수 있습니다.

```sql
ALTER TABLE customer ADD COLUMN email string;
```

기존 Parquet 파일을 모두 다시 만들지 않아도 테이블 스키마를 관리할 수 있습니다.

---

### 4.2 Time Travel

Iceberg는 특정 시점 또는 특정 버전의 데이터를 조회할 수 있습니다.

예시는 다음과 같습니다.

```sql
SELECT *
FROM customer
FOR TIMESTAMP AS OF TIMESTAMP '2026-06-01 00:00:00';
```

Iceberg는 Snapshot 기반으로 테이블 상태를 관리하기 때문에, 과거 시점 조회와 롤백이 가능합니다.

---

### 4.3 ACID 트랜잭션

Iceberg는 데이터 레이크에서도 DB처럼 안정적인 변경 처리를 지원합니다.

예를 들어 Spark가 데이터를 쓰는 중에 Trino가 조회하더라도, Trino는 **완료되지 않은 중간 상태**를 보지 않습니다.

즉, Iceberg는 다음과 같은 안정성을 제공합니다.

- 쓰기 작업이 완료되기 전에는 변경 내용이 노출되지 않음
- 일부 파일만 반영된 불완전한 상태를 방지
- 여러 엔진이 동시에 접근해도 일관성 있는 테이블 상태 유지

---

### 4.4 Hidden Partitioning

기존 Hive 방식에서는 사용자가 파티션 구조를 직접 알아야 했습니다.

예를 들어 다음과 같이 조회 조건을 작성해야 하는 경우가 많았습니다.

```sql
WHERE year = 2026
  AND month = 6
  AND day = 5
```

Iceberg는 사용자가 파티션 컬럼을 직접 몰라도, 조회 조건을 보고 필요한 파일만 자동으로 읽도록 처리합니다.

이를 **Hidden Partitioning**이라고 합니다.

장점은 다음과 같습니다.

- 사용자가 파티션 구조를 몰라도 됨
- 잘못된 파티션 조건으로 인한 조회 오류 감소
- 필요한 데이터 파일만 읽어 성능 향상

---

### 4.5 여러 분석 엔진에서 공동 사용

Iceberg 테이블은 여러 분석 엔진에서 함께 사용할 수 있습니다.

```text
Spark
Trino
Flink
Presto
Hive
Impala
```

즉, 하나의 Iceberg 테이블을 Spark에서 적재하고, Trino에서 조회하고, Flink에서 스트리밍 처리하는 방식이 가능합니다.

---

## 5. Parquet와 Iceberg의 차이

| 구분 | Parquet | Iceberg |
|---|---|---|
| 역할 | 파일 포맷 | 테이블 포맷 |
| 저장 대상 | 실제 데이터 | 메타데이터 + 테이블 상태 관리 |
| 예시 | `part-0001.parquet` | `customer` 테이블 |
| 스키마 변경 | 제한적 | 체계적 관리 가능 |
| Time Travel | 자체적으로 어려움 | 가능 |
| ACID | 없음 | 지원 |
| 엔진 연계 | 파일 단위 | 테이블 단위 |

정리하면 다음과 같습니다.

> **Parquet는 데이터를 담는 파일이고, Iceberg는 그 파일들을 테이블처럼 관리하는 방식입니다.**

---

## 6. Data Lakehouse에서 Iceberg의 위치

Iceberg는 Data Lakehouse 구조에서 핵심적인 역할을 합니다.

```text
S3 / HDFS / ADLS = 저장소
Parquet = 데이터 파일
Iceberg = 테이블 관리 포맷
Spark / Trino / Flink = 조회·처리 엔진
Data Lakehouse = 이 전체 구조를 활용한 분석 아키텍처
```

Data Lakehouse 관점에서 보면 Iceberg는 다음 역할을 합니다.

| 구성 요소 | 역할 |
|---|---|
| S3 / HDFS / ADLS | 데이터를 저장하는 스토리지 |
| Parquet / ORC / Avro | 실제 데이터 파일 형식 |
| Iceberg | 파일들을 테이블처럼 관리하는 메타데이터 계층 |
| Spark / Trino / Flink | 데이터를 처리하고 조회하는 엔진 |
| Catalog | Iceberg 테이블 위치와 메타데이터를 관리 |

---

## 7. 한 줄 요약

**Apache Iceberg는 S3, HDFS, ADLS 같은 파일 저장소 위의 Parquet 데이터를 DB 테이블처럼 관리하게 해 주는 Lakehouse 핵심 기술입니다.**

실무적으로는 다음과 같이 이해하면 됩니다.

```text
저장소에 파일만 쌓아두는 Data Lake의 한계를 보완하여,
데이터를 안정적인 분석 테이블로 관리하게 해 주는 기술
```

---

## 8. 참고 링크

- Apache Iceberg 공식 사이트: <https://iceberg.apache.org/>
- Apache Iceberg 공식 문서: <https://iceberg.apache.org/docs/latest/>