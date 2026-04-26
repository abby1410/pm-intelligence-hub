import feedparser
import json
import os
from datetime import datetime
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

news_feeds = [
    "https://techcrunch.com/tag/artificial-intelligence/feed/",
    "https://www.producthunt.com/feed"
]

job_feed = "https://remoteok.com/remote-product-manager-jobs.rss"

def analyze_article(text):
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

Return STRICT JSON:
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

        return json.loads(response.choices[0].message.content.strip())

    except:
        return {
            "summary": text[:200],
            "category": "General",
            "skills": [],
            "why_pm_care": "AI processing failed."
        }

def extract_job_skills(text):
    if not client:
        return []

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"""
Extract professional skills/tools from this job description.
Return JSON array only.

{text}
"""
                }
            ]
        )

        return json.loads(response.choices[0].message.content.strip())

    except:
        return []

articles = []
jobs = []
skill_counter = {}

# FETCH ARTICLES
for url in news_feeds:
    feed = feedparser.parse(url)

    for entry in feed.entries[:3]:
        analysis = analyze_article(entry.summary[:1500])

        articles.append({
            "title": entry.title,
            "link": entry.link,
            "summary": analysis["summary"],
            "category": analysis["category"],
            "skills": analysis["skills"],
            "why_pm_care": analysis["why_pm_care"],
            "date": str(datetime.now())
        })

# FETCH JOBS
feed = feedparser.parse(job_feed)

for entry in feed.entries[:5]:
    skills = extract_job_skills(entry.summary[:1500])

    for skill in skills:
        skill_counter[skill] = skill_counter.get(skill, 0) + 1

    jobs.append({
        "title": entry.title,
        "link": entry.link,
        "skills": skills
    })

output = {
    "articles": articles,
    "jobs": jobs,
    "trending_skills": sorted(
        skill_counter.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]
}

with open("data.json", "w") as f:
    json.dump(output, f, indent=2)