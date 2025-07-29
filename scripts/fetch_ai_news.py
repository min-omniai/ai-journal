# scripts/fetch_ai_news.py
import os
import argparse
import openai
import feedparser

def collect_urls(rss_urls, max_per_source=5):
    urls = []
    for rss in rss_urls:
        feed = feedparser.parse(rss)
        for entry in feed.entries[:max_per_source]:
            urls.append(entry.link)
    return urls

def fetch_news(max_items):
    # IT 매체 & AI 도구/인사이트용 RSS 피드 목록
    rss_sources = [
        # TechCrunch
        "https://techcrunch.com/feed/",
        "https://techcrunch.com/tag/artificial-intelligence/feed/",
        # VentureBeat
        "https://venturebeat.com/feed/",
        "https://venturebeat.com/category/ai/feed/",
        # OpenAI Blog
        "https://openai.com/blog/rss/",
        # Midjourney 블로그
        "https://midjourney.com/blog/rss/",
        # Google AI 블로그
        "https://ai.googleblog.com/feeds/posts/default?alt=rss",
        # Lex Fridman 팟캐스트
        "https://lexfridman.com/feed/podcast/",
        # Two Minute Papers (유튜브 동영상 RSS via twitRSS)
        "https://twitrss.com/TwoMinutePapers",
        # X (Twitter) OpenAI 공식 계정 RSS via twitRSS
        "https://twitrss.com/openai"
    ]

    # RSS에서 URL 수집
    all_urls = collect_urls(rss_sources, max_per_source=5)
    urls_to_summarize = all_urls[:max_items]

    # Markdown 리스트 형태로 프롬프트 생성
    url_list_markdown = "\n".join(f"- {url}" for url in urls_to_summarize)
    prompt = f"""
당신은 매일 최신 AI 뉴스를 한국어로 큐레이션하는 전문가입니다.
다음 URL들의 기사를 최신순으로 요약하고 두괄식 설명·인사이트를 포함하세요:

{url_list_markdown}

각 항목은 아래 형식으로 작성하세요:
**제목**: [한글 번역된 기사 제목]
**발표 시각**: [YYYY-MM-DD HH:MM]
**분야**: [세부 분야]
**요약**: [1–2문장으로 핵심 내용]
**설명**: [두괄식으로 핵심 결론 제시 후 배경·핵심 포인트 모두 자세히 설명]
**인사이트**: [트렌드 해석 및 시사점]
**원문 링크**: [읽으러 가기]({{url}})
**참고 이미지/영상 링크**: [이미지/영상 보기]({{image_url}})
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

    date = os.path.basename(args.output).replace(".md", "")
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(f"# AI 뉴스 요약 — {date}\n\n")
        f.write(news_content)

if __name__ == "__main__":
    main()
