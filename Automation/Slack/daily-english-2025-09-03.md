# 📦 Daily English Quiz Auto-Grader — Dev Log (v1.1)

- **Stack**: Google Forms → Google Sheets → Apps Script (.gs) → Slack (Incoming Webhook / Block Kit)

---

- 폼 제출 시 **자동 채점 → 시트 기록(세로 누적) → Slack Block Kit 전송**까지 동작.  
- 가독성 떨어지던 “코드블록 표” 제거, **Block Kit(섹션+필드)** UI로 교체.  
- `Form Responses 1` 시트에 `Score`와 `Detail(JSON)`을 **행 단위**로 기록.

---

## 1) 프로젝트 개요

매일 영어 학습(단어·구어체·문법) 퀴즈를 **Google Form**으로 제출하면:

1. **자동 채점**  
2. **점수 + 상세결과를 Google Sheet에 누적 저장**  
3. **Slack으로 결과 요약 전송**

### 효과
- 제출 즉시 피드백(점수/정답) 확인  
- Slack에서 읽기 쉬운 카드형 결과  
- 시트에 누적 기록(복습·분석·리뷰 용이)

---

## 2) 오늘의 진행 사항

- [x] Slack 메시지 **Block Kit**로 전환 (섹션+필드 4칸: 문제/내답/정답/OX)  
- [x] 시트 **세로 누적**: `Score` 고정 열에 **항상 마지막 행**에 점수 기록  
- [x] 시트 **상세결과 저장**: `Detail` 열에 `rows` 배열(JSON: title/user/correct/mark) 저장  
- [x] 기존 채점·정답키 로딩 구조 유지 (`_loadLatestAnswerKey_`, `judgeRow`)

---

## 3) 어려웠던 점과 해결책

### A. Slack 표 가독성 문제
- **원인**: 코드블록 표는 폭/줄바꿈 제약으로 답·오답 구분이 어려움  
- **해결**: Slack 권장 UI인 **Block Kit**로 전환 (`section.fields` 활용)

### B. 시트가 가로로 늘어나는 현상
- **원인**: 점수 기록 시 매번 `lastCol + 1`로 새 열 추가  
- **해결**: `Score`/`Detail` 열을 **한 번만 생성** 후, 항상 마지막 행에 기록 (세로 누적)

### C. 수동 테스트 필요
- **해결**: `onFormSubmit_autoGrade`에서 **수동 실행 시 마지막 응답 행 로드** 기능 구현

---

## 4) Apps Script 구조

- **파일**: `grading.gs`
  - `_saveAnswerKey_(dayLabel, ymd, key)`: 정답키 저장  
  - `_loadLatestAnswerKey_()`: 최신 정답키 로드  
  - `onFormSubmit_autoGrade(e)`: 핵심 엔트리 (채점 → 기록 → Slack)  
  - `postToSlack_(payload)`: Slack Webhook POST (Block Kit 지원)

- **트리거**: 이벤트 소스 = **폼 제출(Form submit)**, 함수 = `onFormSubmit_autoGrade`  
- **로그**: IDE 좌측 **Executions** 탭에서 실행 결과 확인, `Logger.log()` 활용

---

## 5) 구현 흐름

1. **정답키 로드**: `_loadLatestAnswerKey_()`  
2. **응답 파싱**: `e.namedValues` 또는 수동 실행 시 마지막 행 로드  
3. **채점**: `judgeRow()`로 `rows` 배열(title/user/correct/mark) 생성  
4. **시트 기록**: 마지막 행의 `Score`와 `Detail(JSON)`에 기록  
5. **Slack 전송**: Block Kit 카드로 요약 메시지 발송

---

## 6) 코드 스니펫

### Score + Detail(JSON) 세로 누적 기록
```javascript
const sh = getFormResponseSheet_();
const lastRow = sh.getLastRow();
const headers = sh.getRange(1,1,1,sh.getLastColumn()).getValues()[0];

// Score 열
let scoreCol = headers.indexOf('Score') + 1;
if (scoreCol <= 0) {
  scoreCol = headers.length + 1;
  sh.getRange(1, scoreCol).setValue('Score');
}
sh.getRange(lastRow, scoreCol).setValue(`${score}/${total}`);

// Detail 열(JSON)
let detailCol = headers.indexOf('Detail') + 1;
if (detailCol <= 0) {
  detailCol = headers.length + 2;
  sh.getRange(1, detailCol).setValue('Detail');
}
sh.getRange(lastRow, detailCol).setValue(JSON.stringify(rows));

// Slack Block Kit 전송
const blocks = [
  {
    type: "header",
    text: { type: "plain_text", text: `🧮 Daily Quiz 채점 결과 — ${score}/${total}` }
  },
  {
    type: "context",
    elements: [{ type: "mrkdwn", text: `날짜: ${meta.date} / Day: ${meta.day}` }]
  },
  ...rows.map(r => ({
    type: "section",
    fields: [
      { type: "mrkdwn", text: `*문제:* ${r.title}` },
      { type: "mrkdwn", text: `*내가 쓴 글:* ${r.user}` },
      { type: "mrkdwn", text: `*정답:* ${r.correct}` },
      { type: "mrkdwn", text: `*정답유무:* ${r.mark}` }
    ]
  }))
];

postToSlackResult_({ blocks });  // ← Slack 전송 함수 호출
}
```

## 7) 시트 스키마

- **Form Responses 1**
  - 기본 구글폼 응답(1행 = 헤더, 2행부터 데이터)  
  - 추가 열(자동 관리)  
    - `Score`: 예) `"5/7"`  
    - `Detail`: 예) `[{"title":"문제 1.","user":"apple","correct":"apple","mark":"O"}, ...]`

- **Meta_AnswerKey**
  - 헤더: `Date | Day | AnswerKey(JSON)`  
  - 예시:
    ```json
    {
      "words": [["apple"], ["borrow"], ["venue"]],
      "wordEx": [["I like apples."], ["Can I borrow your pen?"], ["The venue is great."]],
      "expr": ["Sounds good."]
    }
    ```

---

## 8) 실행 단계

1. **트리거 설정**: Apps Script → Triggers → On form submit → `onFormSubmit_autoGrade`  
2. **정답키 세팅**: `_saveAnswerKey_()` 실행 후 `_loadLatestAnswerKey_()` 로드  
3. **테스트**
   - 폼 제출 → Slack 카드 수신 확인  
   - 시트 `Score`/`Detail` 열에 기록 확인  
   - 수동 실행 시 마지막 행 로드 확인

---

## 9) 체크리스트

- [ ] 트리거가 `onFormSubmit_autoGrade`에 연결되어 있는가  
- [ ] `Meta_AnswerKey`에 최신값이 있는가  
- [ ] `Score`/`Detail` 열이 중복 생성 없이 유지되는가  
- [ ] Slack Webhook URL 또는 Bot Token이 유효한가  
- [ ] 수동 실행 경로에서 정상 동작하는가

---

## 10) 변경 이력

- **v1.1 (2025-09-03)**  
  - Slack: 코드블록 표 → Block Kit 전환  
  - Sheet: `Score`/`Detail(JSON)` 세로 누적 저장  
  - 수동 실행 시 마지막 행 로드 안정화

- **v1.0**  
  - 자동 채점/Slack 전송 초기 구현 (코드블록 표)

### Commit 메시지 예시
- `feat(slack): replace codeblock table with Block Kit`  
- `feat(sheet): append Score and Detail(JSON) vertically per submission`  
- `refactor(grade): stabilize manual-run path reading last response row`  
- `docs: add dev log and setup guide`

---

## 11) 다음 액션

- [ ] `Detail`을 열 단위로 분해해 저장 (문제별 내답/정답/OX)  
- [ ] Slack 요약 카드에서 오답만 하이라이트  
- [ ] `_isLooseCorrect()` 개선 (동의어·오타 허용 폭 옵션화)  
- [ ] AnswerKey 관리용 시트/메뉴 추가  
- [ ] Bot Token 방식 전환 시 인터랙션 지원

---

## 12) 주요 함수 설명

- `_saveAnswerKey_(dayLabel, ymd, key)`: 날짜/Day와 함께 정답키 저장  
- `_loadLatestAnswerKey_()`: 최신 정답키 로드  
- `onFormSubmit_autoGrade(e)`: 채점 → `Score`/`Detail` 기록 → Slack 전송  
- `postToSlack_(payload)`: Webhook POST (Block Kit 메시지 전송)

---

> 제안: `/docs/devlog-2025-09-03.md` 로 저장, 루트 `README.md`에는 Quick Start 요약 추가
