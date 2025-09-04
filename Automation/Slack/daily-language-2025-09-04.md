# 📘 Daily English Dev Log (2025-09-04)

## ✅ 오늘 작업 정리

### 1. Slack 발송 개선

* Daily Expression → Slack으로 정상 발송 확인.
* 볼드체 및 카테고리 간 공백 추가하여 가시성 개선.
* Sent? / SentAt 컬럼 업데이트 로직 정상 작동.

### 2. Google Form 연동

* `sendEveningForm` 구현 → 아침에 보낸 학습 데이터를 바탕으로 퀴즈 문제 자동 갱신.
* 문제 번호(`문제 n.`) 일관성 유지 → 응답 시트 가로 확장 문제 해결.
* Slack 메시지와 Google Form 문제 포맷을 동일하게 맞춤.

### 3. 채점 로직 구현

* `onFormSubmit` 트리거 등록 → 폼 제출 시 자동 채점.
* `extractAnswers` 수정:

  * 단어 뜻 문제 → 정답 = 단어 자체.
  * 단어 예문 문제 → 정답 = 영문 예문 전체.
  * 구어체 문제 → 정답 = 구어체 표현 전체.
* `normalize()` 추가 → 대소문자, 구두점(`.,!?`), 공백, `'` vs `’` 차이 무시.

### 4. Trigger 자동 등록

* `registerTriggers()` 개선 → 아침/저녁 발송 및 폼 제출 채점 트리거 자동 등록.

### 5. GPT-S 설정 점검 및 수정 제안

* **설명**: 고정된 3+1+1 → 유동적 개수 + Slack/Google Form/채점 자동화 포함.
* **지침**: 단어·구어체·문법 개수 N/M/K 조정 가능, 저녁 퀴즈 및 채점 프로세스 반영.
* **지식 파일**:

  * Headers에 `FormSent?, FormSentAt` 추가.
  * 문제 생성/채점 규칙 및 normalize 규칙 명시.

---

## 📌 오늘의 핵심 이슈 & 해결

1. **구글폼 응답 시트 가로 확장 문제** → 문제 번호를 `updateFormWithQuiz`에서만 붙여 일관성 유지.
2. **채점 오류(예문 vs 단어 혼동)** → `extractAnswers` 수정으로 예문 문제는 영문 예문 전체를 정답 처리.
3. **작은따옴표 vs 꺾은따옴표 문제** → `normalize()`에서 통일 처리.

---

## 📅 다음 단계 제안

* Slack 채점 결과 메시지에 **정답률(%)** 표시.
* 시트에 FormSent? / FormSentAt 기록 자동화.
* 7일치/30일치 배치 데이터 자동 Slack 발송 기능 확장.
