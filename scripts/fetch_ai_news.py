import os
import argparse
import openai

def fetch_news(max_items):
    prompt = f"""
You are an expert AI news curator. Every day, select up to {max_items} high-quality AI news items published within the last 24 hours that match the user’s four interest topics:
1) Large Language Models & Conversational AI
2) Generative AI & AI Art Generators
3) Executive & Company News about AI firms and CEOs
4) Industry Insights & Thought Leadership (including insights from renowned AI and robotics books and related videos)

Source from TechCrunch, Ben’s Bites, VentureBeat, OpenAI Blog, and other reputable outlets. Do not group by category—just provide a single list sorted by recency.

Format each item as:
**[제목]**
[뉴스 시간 및 정확한 링크]
**분야**: [세부 분야]
**요약**: [1–2문장]
**설명**: [배경·핵심 내용을 자세히]
**인사이트**: [트렌드 해석]
**참고 링크/이미지**: [가능할 경우]
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1000,
    )
    return response.choices[0].message.content

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, help="Path to output markdown file")
    parser.add_argument("--max-items", type=int, default=10)
    args = parser.parse_args()

    openai.api_key = os.getenv("OPENAI_API_KEY")
    content = fetch_news(args.max_items)

    date = os.path.basename(args.output).replace('.md','')
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(f"# AI News Summary — {date}\n\n")
        f.write(content)

if __name__ == "__main__":
    main()
