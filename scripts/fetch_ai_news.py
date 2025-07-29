# scripts/fetch_ai_news.py
import os
import argparse
import openai
import feedparser
from datetime import datetime, timedelta, timezone

# --- 최근 4시간 이내 발행된 항목만 수집하도록 변경 ---
def collect_recent_urls(rss_urls, hours=4, max_per_source=5):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    urls = []
    for rss in rss_urls:
        feed = feedparser.parse(rss)
        for entry in feed.entries:
            # published_parsed → datetime 변환
            if hasattr(entry, 'published_parsed'):
                published_dt = datetime.fromtimestamp(
                    int(datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).timestamp()),
                    tz=timezone.utc
                )
                if published_dt < cutoff:
                    continue
            else:
                # published 정보 없으면 건너뛰기
                continue

            urls.append(entry.link)
            if len(urls) >= max_per_source:
                break
    return urls

def fetch_news(urls_to_summarize):
    # (기존 fetch_news 로직을 urls_to_summarize만 받아 처리)
    url_list_markdown = "\n".join(f"- {url}" for url in urls_to_summarize)
    prompt = f"""
당신은 매일 최신 AI 뉴스를 한국어로 큐레이션하는 전문가입니다.
다음 URL들의 기사를 최신순으로 요약하고 두괄식 설명·인사이트를 포함하세요:

{url_list_markdown}

(이후 생략...)
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

    # ▶ 최근 4시간 이내 URL만 수집
    rss_sources = [ 
        # (RSS 목록 생략)
    ]
    recent_urls = collect_recent_urls(rss_sources, hours=4, max_per_source=args.max_items)
    if not recent_urls:
        print("최근 4시간 내 신규 뉴스가 없습니다. 스킵합니다.")
        return

    news_content = fetch_news(recent_urls)

    date = os.path.basename(args.output).replace(".md", "")
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(f"# AI 뉴스 요약 — {date}\n\n")
        f.write(news_content)

if __name__ == "__main__":
    main()
