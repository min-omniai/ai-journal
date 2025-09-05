# 📡 AI 뉴스 자동화 프로젝트

## 프로젝트 개요
- **프로젝트명**: AI 업계 뉴스 자동화 시스템  
- **개발 기간**: 2025년 9월 5일  
- **플랫폼**: Make.com + Perplexity API + Slack  
- **목적**:  
  - 매일 아침 7시 AI 업계 최신 동향 자동 수집  
  - **관심 분야**: OpenAI, Anthropic, Google AI, Apple, xAI, Android/iOS, 크리에이티브 AI 툴들  
  - **우선순위**: 신기술 발표 > 기업 동향/투자 > 규제  
  - **형태**: 헤드라인 + 간단 요약 + 출처 링크  

---

## 💰 예상 비용 분석
### 초기 옵션
- Perplexity Pro: 월 $20 + API $5-10 → **월 $25-30**
- 무료 RSS + 번역: **월 $0** (품질 제한)
- 직접 개발: **월 $300-800** (비현실적)

### 최종 선택
- Perplexity API: **월 250원** (30회 × Sonar 모델)  
- Make.com: **무료 플랜 (월 1,000 ops)**  
- **총 비용: 월 250원**

---

## 🎯 기대 효과
- 매일 30분 수동 검색 절약  
- 일관된 AI 뉴스 큐레이션  
- 주요 기술 트렌드 누락 방지  
- 모바일 알림으로 즉시 확인  

---

## ⚙️ 기술 구조
```bash
Schedule (매일 7시)
↓
Perplexity AI (Sonar 모델)
↓
Slack (Create Message)
```

---

**프롬프트 예시**  
```bash
Latest news from OpenAI, Anthropic, Google AI, Apple, xAI, Android/iOS,
App Store/Google Play Store policies, Midjourney, Kling, Higgsfield, Veo3,
Nano Banana, and Big Tech CEO updates from today and yesterday.

IMPORTANT:

- Only include companies/topics with actual news

- Skip if no updates

- Provide complete website URLs, not citation numbers

Slack markdown rules:

- text for bold

- Blank lines between items

- Company names bolded [OpenAI]
```

---

## 🚧 주요 장애물 & 해결
1. **Gmail OAuth 실패**  
   - 문제: redirect_uri_mismatch  
   - 시도: 도메인 추가, 다양한 URI 적용 → 실패  
   - 결론: Gmail OAuth 복잡성 → **Slack으로 대체**

2. **출처 인용 문제**  
   - 문제: [1][5] 숫자 인용  
   - 해결: “Always provide complete website URLs” 프롬프트 추가

3. **Slack 서식 문제**  
   - 문제: `**text**` 미지원  
   - 해결: `*text*` 사용

4. **가독성 문제**  
   - 해결: 항목 간 공백 추가

---

## 🔄 대안 방안
- **Slack 선택 이유**  
  - OAuth 불필요, 모바일 즉시 알림, 링크 미리보기 지원  

- **포기한 기능**  
  - Gmail 이메일 전송  
  - RSS 집계  
  - 고급 필터링  

---

## ✅ 최종 결과
- 성공 기능:
  - 매일 자동 실행
  - Perplexity API 뉴스 수집
  - 한국어 요약
  - 실제 URL 포함
  - Slack 전송
  - 초저비용 운영 (월 250원)

**실제 출력 예시**
```bash
[OpenAI] GPT-5 출시 및 맞춤형 AI 칩 개발
OpenAI가 GPT-5를 공식 출시했으며, 더 빠르고 정교한 추론 능력을 제공.
출처: https://ts2.tech/en/ai-revolution-in-overdrive-gpt-5-debut-billion-dollar-bets-global-crackdowns-sept-4-5-2025/

[Anthropic] API 매출 662% 폭증·$13B 투자 유치
Anthropic의 API 비즈니스가 662% 성장, AWS 매출에도 기여.
출처: https://www.ainvest.com/news/anthropic-api-business-surges-662-driving-aws-growth-2509/
```

---

## 📈 개선 가능 영역
- 중요도 기반 뉴스 필터링  
- 다중 채널 확장 (Discord, Teams 등)  
- Gmail 연동 (OAuth 해결 시)  
- 주간/월간 트렌드 분석 기능  

---

## 📝 프로젝트 평가
- **목표 달성도**: 85%  
- **성공**: 자동화, 비용 효율, 정보 품질  
- **부분 성공**: Slack 단일 채널  
- **실패**: Gmail 연동, 고급 필터링  

---

## 📚 학습한 점
- Make.com의 장점과 한계  
- Google OAuth 복잡성  
- API 비용 현실적 계산  
- 프롬프트 엔지니어링의 중요성  

---

## 🔖 권장사항
- Gmail OAuth는 개인 프로젝트에 비효율적  
- Slack/Discord 등 웹훅 우선 고려  
- Perplexity API는 뉴스 수집에 효과적  
- Make.com 무료 플랜으로도 충분  

---

**작성일**: 2025년 9월 5일  
**최종 업데이트**: 시스템 안정화 완료  
