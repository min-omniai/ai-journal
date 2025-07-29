# scripts/fetch_ai_news.py
import os
import argparse
import openai
import feedparser
from datetime import datetime, timedelta, timezone

# 1) RSS 피드 리스트
rss_sources = [
    # 기존 피드
    "https://techcrunch.com/tag/artificial-intelligence/feed/",          # AI 전반, LLM·챗봇 포함
    "https://venturebeat.com/category/ai/feed/",                         # AI 기업 전략·제품 소식
    "https://openai.com/blog/rss/",                                      # OpenAI 공식 블로그
    "https://midjourney.com/blog/rss/",                                  # Midjourney 업데이트
    "https://ai.googleblog.com/feeds/posts/default?alt=rss",             # Google AI 블로그
    "https://lexfridman.com/feed/podcast/",                              # Lex Fridman 팟캐스트
    "https://twitrss.com/TwoMinutePapers",                               # Two Minute Papers 트윗 요약
    "https://twitrss.com/openai",                                        # OpenAI 트위터 요약

    # 대형 언어 모델 & 대화형 AI
    "https://blog.google/products/gemini/feed/",                         # Google Gemini 소식
    "https://huggingface.co/blog/rss.xml",                               # Hugging Face 신제품·연구

    # 생성형 AI & AI 아트 생성기
    # (기존 Midjourney 외)
    "https://stable-diffusion-web.com/feed/",                             # Stable Diffusion 커뮤니티 업데이트
    "https://nightcafe.studio/blog/feed/",                                # NightCafe AI 아트 생성

    # AI 기업 및 CEO 경영진 동향·기업 소식
    "https://about.fb.com/news/category/ai/feed/",                       # Meta AI 소식
    "https://blogs.microsoft.com/feed/ai/",                              # Microsoft AI 블로그
    "https://blogs.nvidia.com/feed/",                                     # NVIDIA 기술·CEO 발표

    # 산업 인사이트 & 사고 리더십
    "https://www.technologyreview.com/feed/",                            # MIT Tech Review AI 섹션
    "https://arxiv.org/rss/cs.AI",                                       # arXiv AI 최신 논문
]

def collect_recent_urls(rss_urls, hours=4, per_source=5):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    urls = []
    for rss in rss_urls:
        feed = feedparser.parse(rss)
        count = 0
        for entry in feed.entries:
            # published_parsed 없으면 건너뛰기
            if not hasattr(entry, 'published_parsed'):
                continue
            published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            if published < cutoff:
                continue
            urls.append(entry.link)
            count += 1
            if count >= per_source:
                break
    return urls

def fetch_news(urls):
    md_list = "\n".join(f"- {u}" for u in urls)
    prompt = f"""
당신은 매일 최신 AI 뉴스를 한국어로 큐레이션하는 전문가입니다.  
다음 URL들의 기사를 최신순으로 요약하고 두괄식 설명·인사이트를 포함하세요:

{md_list}

각 항목은 아래 형식으로 작성하세요:

**제목**: [한글 번역된 기사 제목]  
**발표 시각**: [YYYY-MM-DD HH:MM]  
**분야**: [세부 분야]  
**요약**: [1–2문장으로 핵심 내용]  
**설명**: [두괄식으로 핵심 결론 제시 후 배경·핵심 포인트 모두 자세히 설명]  
**인사이트**: [트렌드 해석 및 시사점]  
**원문 링크**: [읽으러 가기](<기사 URL>)  
"""
    # resp = openai.ChatCompletion.create(
    #     model="gpt-4o-mini",
    #     messages=[{"role": "user", "content": prompt}],
    #     temperature=0.3,
    #     max_tokens=1500,
    # )

    # OpenAI Python SDK v1+ 용 호출 방식
    resp = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1500,
    )
    return resp.choices[0].message.content

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, help="출력할 마크다운 파일 경로")
    parser.add_argument("--max-items", type=int, default=10, help="피드당 최대 뉴스 개수")
    args = parser.parse_args()

    openai.api_key = os.getenv("OPENAI_API_KEY")

    # ▶ 디렉터리 보장
    output_dir = os.path.dirname(args.output)
    os.makedirs(output_dir, exist_ok=True)
    
    urls = collect_recent_urls(rss_sources, hours=4, per_source=args.max_items)
    if not urls:
        print("최근 4시간 내 신규 뉴스가 없습니다. 스킵합니다.")
        return

    news_md = fetch_news(urls)
    date = os.path.basename(args.output).replace(".md", "")
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(f"# AI 뉴스 요약 — {date}\n\n")
        f.write(news_md)

if __name__ == "__main__":
    main()
