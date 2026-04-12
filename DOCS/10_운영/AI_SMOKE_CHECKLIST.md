# AI_SMOKE_CHECKLIST

## 1. 목적
이 문서는 AI-PY 핵심 엔드포인트 smoke 검증 절차를 빠르게 수행하기 위한 체크리스트다.

## 관련 문서
- AI 게이트: `AI_RELEASE_GATE.md`
- 공통 배포 게이트: `../../../DOCS/10_운영/RELEASE_GATE.md`
- 증거 템플릿: `../../../DOCS/10_운영/EVIDENCE_TEMPLATE.md`

## 2. 실행 전 확인
- 로컬 또는 대상 환경에서 서비스가 기동 중인지 확인
- 필요한 외부 모델/API 키 주입 여부 확인
- 샘플 입력 자료 준비 여부 확인

## 3. 엔드포인트별 체크

### 3.1 `/health`
- 기대 결과: 정상 상태 응답

### 3.2 `/extract-material`
- 기대 결과: 자료 추출 응답 구조 유지

### 3.3 `/generate-questions`
- 기대 결과: 객관식 문제 생성 응답 구조 유지

### 3.4 `/qa`
- 기대 결과: 답변, 근거, grounded/insufficientEvidence 형태 유지

## 4. fallback 확인
- 근거 부족 질문 시 안내 메시지 유지
- 외부 모델 실패 시 서비스 전체가 비정상 종료하지 않는지 확인

## 5. 기록 항목
- 실행 환경:
- 요청 샘플:
- 실제 응답 요약:
- 판정:
- 증거:

## 6. 실제 smoke 환경 입력
- base AI URL:
- 외부 모델/API 사용 여부:
- 테스트 일시:
- 수행자:
