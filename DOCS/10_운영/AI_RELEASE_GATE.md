# AI_RELEASE_GATE

## 1. 목적
이 문서는 AI-PY 저장소가 배포직전 완료로 판정되기 위한 AI 서비스 전용 게이트를 정의한다.

## 2. 상위 기준 문서
- 루트 `DOCS/10_운영/RELEASE_GATE.md`
- 루트 `DOCS/00_기준/ONE_SHOT_DELIVERY_CONTRACT.md`
- `AI-PY/DOCS/00_기준/통합_개발_테스트_방법론.md`
- `AI-PY/DOCS/10_운영/AI_SMOKE_CHECKLIST.md`
- 루트 `DOCS/10_운영/EVIDENCE_TEMPLATE.md`
- 루트 `DOCS/07_정책/ENV_SOURCE_OF_TRUTH.md`

## 3. 필수 명령
- 테스트: `pytest`
- 로컬 구동 확인: `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`

### Railway 포트 규칙
- Railway 배포 환경에서는 플랫폼이 주입하는 `PORT`를 우선 사용해야 한다.
- `AI_PORT`는 로컬/수동 실행용 fallback 으로만 본다.
- `python -m app.main` 로 실행해도 `PORT` 또는 `AI_PORT` 를 읽어 동일하게 기동되어야 한다.

## 4. 필수 게이트

### 4.1 테스트 게이트
- `pytest`가 성공해야 한다.
- 실패 테스트가 남아 있으면 배포직전 완료로 보지 않는다.

### 4.2 smoke 게이트
아래 엔드포인트가 기본 smoke 기준을 만족해야 한다.
- `/health`
- `/extract-material`
- `/generate-questions`
- `/qa`

### 4.3 fallback 게이트
- 외부 모델/API 문제 발생 시 서비스가 어떻게 실패하는지 명시돼야 한다.
- 범위 밖 질문 또는 근거 부족 응답 정책이 유지되어야 한다.

### 4.4 운영 연동 게이트
- AI-BACK이 참조하는 `APP_AI_BASE_URL` 기준 연결 대상이 명확해야 한다.
- 응답 형태가 백엔드 기대 계약을 깨지 않아야 한다.

## 5. 배포/구동 기준
- 문서상 AI-PY는 별도 AI 서비스로 동작한다.
- 배포 플랫폼은 루트 문서에서 명시된 외부 AI 서비스 연결 기준과 일치해야 한다.
- 실제 운영 호스팅이 정해지면 본 문서에 반영한다.

## 6. 필수 확인 항목
- [ ] pytest 통과
- [ ] `/health` 확인
- [ ] `/extract-material` smoke 확인
- [ ] `/generate-questions` smoke 확인
- [ ] `/qa` smoke 확인
- [ ] fallback 정책 확인

## 7. 배포 차단 조건
- pytest 실패
- 핵심 엔드포인트 smoke 실패
- 응답 계약 불일치
- 운영 AI 서비스 주소 미확정

## 8. 증거 기록
- 실행 명령
- pytest 결과
- 엔드포인트 smoke 결과
- fallback 검증 결과
- known issue

## 9. 실제 운영 입력 항목
- APP_AI_BASE_URL 실제 값:
- 운영 호스팅 위치:
- 외부 모델/API 책임자:
- smoke 테스트 기준 환경:
- 배포 승인자:

## 10. Railway 운영 메모
- `APP_AI_BASE_URL` 에는 `https://...railway.app` 형태의 **베이스 URL만** 입력한다.
- `/qa` 같은 path 는 `APP_AI_BASE_URL` 에 포함하지 않는다.
- Railway 서비스 공개 도메인에서 `/health`, `/qa` smoke 를 확인한 뒤 AI-BACK 에 반영한다.
