# 📦 Daily English Quiz Auto-Grader — Dev Log (v1.0)

> Google Sheet → Apps Script → Slack 매일 7시 영어 학습 발송 (단어·구어체 5 + 문법 1)

---

## 1) 디렉터리 구조

```
📁 daily-english-slack
├─ README.md
├─ LICENSE (MIT)
├─ .gitignore
├─ docs/
│  ├─ architecture.md
│  ├─ setup.md
│  └─ workflow.md
├─ sheets/
│  └─ headers.md
├─ scripts/
│  └─ apps_script/
│     ├─ sendToSlack.gs
│     └─ README.md
├─ devlog/
│  └─ 2025-08-29.md
└─ .github/
   ├─ ISSUE_TEMPLATE.md
   └─ PULL_REQUEST_TEMPLATE.md
```

---

## 2) 핵심 파일 초안

### 2.1 `README.md`

```markdown
# daily-english-slack
Google Sheet → Apps Script → Slack으로 매일 07:00에 영어 학습(단어·구어체 5, 문법 1)을 발송합니다.

## Features
- Daily Expressions(5) + Grammar(1) 슬랙 메시지 자동 구성
- Settings 시트로 **ON/OFF 토글** 및 **WebhookURL** 관리
- 수동 발송 메뉴(시트 상단 메뉴: 📤 Daily English)

## Quickstart
1) Google Sheet 4탭 생성: `Daily Expressions`, `Grammar Focus`, `Weekly Review`, `My Story Practice`  
   + `Settings` 탭 (Key/Value)
2) Apps Script에 `scripts/apps_script/sendToSlack.gs` 붙여넣기 → 권한 허용
3) `Settings` 탭 입력
   - `SendToSlack | ON`
   - `WebhookURL | https://hooks.slack.com/services/...`
4) 시트 새로고침 → 메뉴 **📤 Daily English → Slack으로 보내기**
5) Apps Script 트리거: `sendToSlack` / Time-driven / Day / 07:00 (Asia/Seoul)

## Repository Structure
- `/docs` 아키텍처, 설정, 워크플로우
- `/sheets` 시트 헤더 정의
- `/scripts/apps_script` Apps Script 코드와 가이드
- `/devlog` 작업 일지 (Planner → Executor → Reviewer)
```

### 2.2 `docs/architecture.md`

````markdown
# Architecture

```mermaid
graph TD
  A[Google Sheet
  - Daily Expressions
  - Grammar Focus
  - Weekly Review
  - My Story Practice
  - Settings(ON/OFF, WebhookURL)] -->|getDisplayValues()| B[Apps Script
  - sendToSlack()
  - pingSlack()
  - onOpen() 메뉴]
  B -->|Webhook| C[Slack #daily-english]
  B -->|Time Trigger 07:00| C
````

## Key Choices

* 날짜는 `getDisplayValues()`로 읽어 **표시 포맷 차이** 안전 처리
* 오늘 데이터 없으면 **가장 최근 날짜** 사용 (아침 발송 유연성)
* Settings 시트로 **배포 환경 변수화** (ON/OFF, WebhookURL)

````

### 2.3 `docs/setup.md`
```markdown
# Setup

## 1) Sheets 탭 & 헤더
- Daily Expressions: Date | Expression | Meaning | Example Sentence | 번역 | Note
- Grammar Focus: Date | Grammar Point | Rule | Example 1 | Example 1 번역 | Example 2 | Example 2 번역 | Common Mistake
- Weekly Review: Week | Expression Review | Grammar Quiz | My Answer | Correct Answer
- My Story Practice: Date | Topic | My Draft (영어) | Corrected | 번역
- Settings(Key/Value):
  - SendToSlack | ON
  - WebhookURL | https://hooks.slack.com/services/...

## 2) Apps Script 코드 배치
- 시트 상단 `확장 프로그램 → App Script` 열기
- `sendToSlack.gs` 내용 전체 붙여넣기 → 저장 → 실행 권한 허용
- `onOpen()` 적용 위해 시트 새로고침

## 3) 트리거 설정
- Apps Script 좌측 Triggers → Add Trigger
  - Function: `sendToSlack`
  - Event: Time-driven / Day timer / 07:00
  - Timezone: Project Settings → Asia/Seoul

## 4) 수동 발송
- 시트 메뉴: **📤 Daily English → Slack으로 보내기**

## 5) 문제 해결
- Webhook 403/404: URL 만료 → 새로 발급
- 날짜 매칭 안 됨: Date 컬럼 실제 입력 확인(빈칸 X)
- 시트명 오타: 정확히 일치해야 함
````

### 2.4 `docs/workflow.md`

```markdown
# Daily Workflow

1) 전날 또는 아침에 `Daily Expressions` 5개, `Grammar Focus` 1개를 입력
2) 07:00 자동 발송 (Settings=ON)
3) 필요 시 수동 발송(메뉴 버튼)
4) 주말에 `Weekly Review` 작성
5) `My Story Practice`로 자기 생각/일 설명 훈련 기록
```

### 2.5 `sheets/headers.md`

```markdown
# Sheet Headers (정의)

## Daily Expressions
- Date / Expression / Meaning / Example Sentence / 번역 / Note

## Grammar Focus
- Date / Grammar Point / Rule / Example 1 / Example 1 번역 / Example 2 / Example 2 번역 / Common Mistake

## Weekly Review
- Week / Expression Review / Grammar Quiz / My Answer / Correct Answer

## My Story Practice
- Date / Topic / My Draft (영어) / Corrected / 번역

## Settings (Key / Value)
- SendToSlack | ON
- WebhookURL | https://hooks.slack.com/services/...
```

### 2.6 `scripts/apps_script/sendToSlack.gs`

```javascript
/**
 * Google Sheet → Slack 07:00 영어 학습 발송
 * - Settings 시트(Key/Value): SendToSlack=ON, WebhookURL=...
 * - 안전한 날짜 처리(getDisplayValues), 최신 날짜 fallback
 */
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu("📤 Daily English")
    .addItem("🔹 Slack으로 보내기", "sendToSlack")
    .addToUi();
}

function sendToSlack() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var expSheet = ss.getSheetByName("Daily Expressions");
  var gramSheet = ss.getSheetByName("Grammar Focus");
  var settings = ss.getSheetByName("Settings");

  if (!expSheet || !gramSheet) {
    throw new Error("시트명을 확인하세요: 'Daily Expressions', 'Grammar Focus'");
  }

  // Settings
  var cfg = getSettings(settings);
  if ((cfg.SendToSlack || "ON").toString().toUpperCase() !== "ON") {
    Logger.log("SendToSlack=OFF");
    return;
  }
  var url = cfg.WebhookURL || "https://hooks.slack.com/services/REPLACE/ME"; // fallback

  var today = Utilities.formatDate(new Date(), "Asia/Seoul", "yyyy-MM-dd");

  // Daily Expressions
  var expValues = expSheet.getDataRange().getDisplayValues();
  var expRows = expValues.slice(1);
  var targetDate = pickTargetDate(expRows.map(r => r[0]), today);
  var items = expRows.filter(r => (r[0] || "").toString().trim() === targetDate).slice(0,5);

  // Grammar Focus
  var gramValues = gramSheet.getDataRange().getDisplayValues();
  var gramRows = gramValues.slice(1);
  var gTarget = pickTargetDate(gramRows.map(r => r[0]), today);
  var grammar = gramRows.find(r => (r[0] || "").toString().trim() === gTarget);

  // Message
  var msg = "☀️ *오늘의 영어 표현 (" + targetDate + ")*\n\n";
  if (items.length === 0) {
    msg += "_표현 데이터가 없습니다. 시트에 입력해주세요._\n";
  } else {
    items.forEach(function(r, i){
      var expr = r[1] || "";   // Expression
      var mean = r[2] || "";   // Meaning
      var ex   = r[3] || "";   // Example Sentence
      var tr   = r[4] || "";   // 번역
      msg += (i+1) + ". *" + expr + "* → " + mean + "\n";
      if (ex) msg += "   ex) " + ex + (tr ? " (" + tr + ")" : "") + "\n\n";
    });
  }

  if (grammar) {
    msg += "📌 *오늘의 문법*: " + (grammar[1]||"") + "\n";
    msg += "- Rule: " + (grammar[2]||"") + "\n";
    if (grammar[3]) msg += "Ex) " + grammar[3] + (grammar[4] ? " ("+grammar[4]+")" : "") + "\n";
    if (grammar[5]) msg += "Ex) " + grammar[5] + (grammar[6] ? " ("+grammar[6]+")" : "") + "\n";
    if (grammar[7]) msg += "⚠️ 주의: " + grammar[7] + "\n";
  } else {
    msg += "📌 *오늘의 문법*: _데이터가 없습니다._\n";
  }

  UrlFetchApp.fetch(url, {method: "post", contentType: "application/json", payload: JSON.stringify({text: msg})});
}

function pingSlack() {
  var url = (getSettings(SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Settings")).WebhookURL) || "https://hooks.slack.com/services/REPLACE/ME";
  UrlFetchApp.fetch(url, {method: "post", contentType: "application/json", payload: JSON.stringify({text: "✅ Webhook OK: Apps Script에서 보낸 테스트"})});
}

// Utils
function getSettings(sheet) {
  var cfg = {};
  if (!sheet) return cfg;
  var values = sheet.getRange(1,1,sheet.getLastRow(),2).getDisplayValues();
  // 기대 형태: 1행: Key | Value (헤더), 2행부터 데이터
  for (var i=1; i<values.length; i++) {
    var k = (values[i][0]||"").toString().trim();
    var v = (values[i][1]||"").toString().trim();
    if (k) cfg[k] = v;
  }
  return cfg;
}

function pickTargetDate(col, today) {
  if (col.some(function(s){return (s||"").toString().trim()===today;})) return today;
  for (var i=col.length-1; i>=0; i--) {
    var v = (col[i]||"").toString().trim();
    if (v && v.toLowerCase() !== "date") return v; // 최신(아래행) 사용
  }
  return today; // fallback
}
```

### 2.7 `scripts/apps_script/README.md`

```markdown
# Apps Script Guide

## 붙여넣기 & 권한
1) 시트 → `확장 프로그램 → App Script`
2) `sendToSlack.gs` 전체 붙여넣기 → 저장
3) `sendToSlack()` 실행 → 권한 허용(고급 → 안전하지 않음 이동 → 허용)

## 트리거
- Time-driven / Day / 07:00 / Asia-Seoul

## 테스트
- `pingSlack()` 실행 → Slack에 테스트 메시지 도착 확인
```

### 2.8 `.gitignore`

```gitignore
# macOS
.DS_Store

# Editors
.vscode/
.idea/

# Credentials
credentials.json
clasp.json
```

### 2.9 `LICENSE` (MIT)

```text
MIT License

Copyright (c) 2025 Min

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
```

### 2.10 `.github/ISSUE_TEMPLATE.md`

```markdown
## 요약
-

## 재현 절차
1.
2.

## 기대 결과 / 실제 결과
- 기대:
- 실제:

## 스크린샷/로그
-
```

### 2.11 `.github/PULL_REQUEST_TEMPLATE.md`

```markdown
## 요약
-

## 변경사항
-

## 체크리스트
- [ ] 로컬 테스트 통과
- [ ] 문서 업데이트 (`docs/`, `README.md`)
- [ ] 시트/스크립트 명 일치 확인
```

### 2.12 `devlog/2025-08-29.md`

```markdown
# Devlog — 2025-08-29

## Planner (목표/설계)
- Slack 07:00 자동 발송 파이프라인 v1
- Settings 기반 ON/OFF, WebhookURL 외부화
- 수동 발송 메뉴 추가

## Executor (구현)
- `sendToSlack.gs` 작성: getDisplayValues, 최신 날짜 fallback
- onOpen 메뉴, pingSlack 테스트
- docs/README/headers 정리

## Reviewer (점검/다음)
- [ ] 날짜 포맷 변동 테스트(yyyy-mm-dd vs locale)
- [ ] 에러 핸들링/로그(빈 데이터, Webhook 실패)
- [ ] 주차별 Weekly Review 자동 합본(향후 v2)

### Conventional Commits (예시)
- `feat(apps-script): add sendToSlack with Settings toggle`
- `docs: add architecture and setup guides`
- `chore: add .gitignore and license`
```

---

## 3) Git 초기화 가이드 (로컬)

```bash
# 1) 프로젝트 폴더 생성
mkdir daily-english-slack && cd daily-english-slack

# 2) 위 파일/폴더 생성 후
git init
git add .
git commit -m "feat(apps-script): initial pipeline with docs"

# 3) 리모트 연결
# 예: github.com/min-omniai/daily-english-slack.git
git remote add origin git@github.com:min-omniai/daily-english-slack.git

git push -u origin main
```

---

## 4) KPI / 리스크

* **KPI**:

  * D+7 기준 발송 성공률 100%, 일 평균 표현 5건 학습 완료률 ≥ 80%
* **리스크/대응**:

  * Webhook 만료 → Settings 교체 가이드 문서화
  * 날짜 미일치 → getDisplayValues로 최소화, 입력 누락 알림 추가 예정(v2)
  * Slack 채널 혼용 → 채널명 고정, 템플릿 헤더에 날짜/챕터 표기

---

### 2.13 `docs/slack-webhook.md`

````markdown
# Slack Webhook 발급 가이드

## 목적
Google Apps Script가 Slack 채널로 메시지를 보내기 위한 **Incoming Webhook URL** 발급 절차.

## 사전 준비
- Slack 워크스페이스 접근 권한
- 메시지를 보낼 채널(예: #daily-english)

## 발급 절차 (5분)
1) 브라우저에서 https://api.slack.com/messaging/webhooks → **Create your Slack app**
2) **From scratch** 선택 → App 이름: `Daily English Bot` → 워크스페이스 선택 → **Create App**
3) 왼쪽 메뉴 **Incoming Webhooks** → 상단 토글 **On** (Activate)
4) **Add New Webhook to Workspace** → 보낼 채널 선택 → **Allow**
5) 발급된 **Webhook URL** 복사 (형태: `https://hooks.slack.com/services/T…/B…/X…`)
6) Google Sheet **Settings 탭**에 입력
   - `WebhookURL | https://hooks.slack.com/services/...`

## 테스트
터미널/포스트맨 중 하나로:
```bash
curl -X POST -H 'Content-type: application/json' \
--data '{"text":"Hello from Daily English Bot 👋"}' \
https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
````

채널에 메시지가 보이면 성공.

## 문제 해결

* **invalid\_url / 403**: URL 오타 또는 만료 → 새 Webhook 발급
* **not\_in\_channel**: (API 방식일 때) 봇이 채널에 미초대 → `/invite @앱이름`
* **조직 보안 정책**: 회사 워크스페이스 제한 시, 개인 Gmail 워크스페이스에서 진행

## 보안/운영 팁

* Webhook URL은 비밀정보 → 리포에 커밋 금지 (`Settings` 시트에만 저장)
* 유출 의심 시 즉시 **Revoke** 후 재발급
* API 확장 계획이 있으면 `docs/slack-api-token.md` 참고(추가 예정)

```
```
