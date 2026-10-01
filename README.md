# 주문 API · Event 일관성 QA 프로젝트

## 프로젝트 개요

주문 서비스에서 발생할 수 있는 API 응답 오류와
DB·Event 데이터 간 불일치를 검증한 QA 포트폴리오입니다.

가상의 주문 DB와 Event Log 데이터를 대상으로 pandas 기반 검증을 수행하고,
Postman을 이용해 실제 공개 API의 상태코드, 필수 필드, 데이터 타입을 확인했습니다.

검증 결과는 Test Case와 Bug Report 형태로 문서화했습니다.

## 사용 기술

- Python
- pandas
- Postman
- HTTP / JSON
- CSV
- Git / GitHub

## 검증 범위

### Event / 데이터 검증

다음 항목을 확인했습니다.

- event_id 중복 여부
- payment_completed의 선행 order_created 존재 여부
- 취소 주문의 payment_completed 발생 여부
- completed 주문의 payment_completed 존재 여부
- DB와 Event의 주문 상태 일관성
- event_id / order_id / event_name / event_time NULL 여부
- event_name 허용값 여부

### API 검증

Postman에서 `GET /carts/1` 요청을 대상으로 다음 항목을 확인했습니다.

- HTTP Status Code 200
- id 필드 존재 여부
- products 필드 존재 여부
- userId 필드 존재 여부
- id의 number 타입 여부
- products의 array 타입 여부
- userId의 number 타입 여부

## 주요 검증 결과

Event 데이터 검증에서 다음 문제를 발견했습니다.

- `EVT-1011` event_id 중복
- `ORD-208`의 order_created 이벤트 누락
- `ORD-209` 취소 주문에 payment_completed 이벤트 발생
- `ORD-207`의 DB status와 Event status 불일치

반면 다음 항목은 정상적으로 통과했습니다.

- completed 주문의 payment_completed 누락 없음
- 필수 Event 필드의 NULL 없음
- event_name 허용값 위반 없음
- Postman API 테스트 7개 모두 PASS

## QA 문서화

`test_cases.csv`에 각 검증 항목의 Expected / Actual / PASS·FAIL 결과를 기록했습니다.

`bug_report.csv`에는 FAIL이 발생한 항목만 별도로 정리하여
결함 내용과 Severity / Priority를 관리했습니다.

## 파일 구성

```text
portfolio2-api-event-qa/
├─ README.md
├─ orders_db.csv
├─ event_logs.csv
├─ event_validation.py
├─ test_cases.csv
├─ bug_report.csv
└─ postman/
   └─ GET Cart 1.request.yaml