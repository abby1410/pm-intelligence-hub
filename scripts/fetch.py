import feedparser
import json
from datetime import datetime

feeds = [
    "https://techcrunch.com/tag/artificial-intelligence/feed/",
    "https://www.producthunt.com/feed"
]

articles = []

for url in feeds:
    feed = feedparser.parse(url)
    for entry in feed.entries[:5]:
        articles.append({
            "title": entry.title,
            "summary": entry.summary[:200],
            "link": entry.link
        })

with open("data.json", "w") as f:
    json.dump(articles, f, indent=2)