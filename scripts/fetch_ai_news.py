# scripts/fetch_ai_news.py
import os
import argparse
import openai

def fetch_news(max_items):
    prompt = f"""
당신은 매일 최신 AI 뉴스를 한국어로 큐레이션하는 전문가입니다. 지난 24시간 동안 발표된 AI 관련 고품질 기사 및 컨텐츠 중 최대 {max_items}건을 다음 네 가지 관심 주제에 맞춰 선택하세요.
1) 대형 언어 모델 & 대화형 AI  
2) 생성형 AI & AI 아트 생성기  
3) AI 기업 및 CEO 관련 경영진 동향·기업 소식  
4) 산업 인사이트 & 사고 리더십(유명 AI·로봇 학술서 인사이트 및 영상)

특히 주로 활용하는 다음 AI 도구—
ChatGPT, Google Gemini, Grok, OpenAI API(Assistants), Google Cloud Console, Google AI Studio, Canva, NotebookLM, Maskara ai, DeepL, Make, Midjourney, Higgsfield, Hailuo AI, Kling AI, Flow—
와 관련된 대표 발표, 핵심 업데이트, 유명 인사 전망 및 인사이트를 우선적으로 포함하세요.

정보 출처는 TechCrunch, Ben’s Bites, VentureBeat, OpenAI Blog 등 IT 전문 매체와  
주요 유튜브 채널(예: Lex Fridman, Two Minute Papers), X(트위터), 링크드인 공식 블로그 등  
신뢰할 수 있는 SNS 콘텐츠를 폭넓게 활용합니다.

카테고리별로 그룹화하지 말고, 발표 시각 순(최신순)으로 단일 목록을 제공합니다.

각 항목은 아래 형식으로 작성하세요:

**제목**: [한글 번역된 기사 제목]  
**발표 시각**: [YYYY-MM-DD HH:MM]  
**분야**: [세부 분야]  
**요약**: [1–2문장으로 핵심 내용]  
**설명**: [두괄식으로 핵심 결론 제시 후 세부 배경·핵심 포인트를 자세히 설명]  
**인사이트**: [트렌드 해석 및 시사점]  
**원문 링크**: [읽으러 가기](<기사의 실제 원문 URL을 여기에 삽입>)
**참고 이미지/영상 링크**: [이미지/영상 보기](<기사 내 실제 이미지 또는 영상 URL을 여기에 삽입>)
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1500,
    )
    return response.choices[0].message.content

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, help="출력할 마크다운 파일 경로")
    parser.add_argument("--max-items", type=int, default=10, help="최대 뉴스 개수")
    args = parser.parse_args()

    openai.api_key = os.getenv("OPENAI_API_KEY")
    news_content = fetch_news(args.max_items)

    date = os.path.basename(args.output).replace('.md','')
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(f"# AI 뉴스 요약 — {date}\n\n")
        f.write(news_content)

if __name__ == "__main__":
    main()
