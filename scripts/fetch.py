import feedparser
import json
import os
from datetime import datetime
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")

# If no API key, skip AI processing safely
client = OpenAI(api_key=api_key) if api_key else None

feeds = [
    "https://techcrunch.com/tag/artificial-intelligence/feed/",
    "https://www.producthunt.com/feed"
]

def analyze_for_pm(text):
    if not client:
        return {
            "summary": text[:200],
            "category": "General",
            "skills": [],
            "why_pm_care": "AI key not configured."
        }

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"""
Analyze this for product managers.

Return STRICT JSON only:
{{
  "summary": "3 bullet summary",
  "category": "AI / Strategy / Infra / Startup",
  "skills": ["skill1","skill2"],
  "why_pm_care": "short insight"
}}

Content:
{text}
"""
                }
            ]
        )

        content = response.choices[0].message.content.strip()
        return json.loads(content)

    except Exception as e:
        return {
            "summary": text[:200],
            "category": "General",
            "skills": [],
            "why_pm_care": f"AI processing failed: {str(e)}"
        }

articles = []

for url in feeds:
    feed = feedparser.parse(url)

    for entry in feed.entries[:3]:
        analysis = analyze_for_pm(entry.summary[:1500])

        articles.append({
            "title": entry.title,
            "link": entry.link,
            "summary": analysis["summary"],
            "category": analysis["category"],
            "skills": analysis["skills"],
            "why_pm_care": analysis["why_pm_care"],
            "date": str(datetime.now())
        })

output = {
    "articles": articles
}

with open("data.json", "w") as f:
    json.dump(output, f, indent=2)