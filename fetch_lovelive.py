import feedparser
import json
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime

RSS_URL = "https://nitter.net/LoveLive_staff/rss"

JST = timezone(timedelta(hours=9))

def clean_text(text):
    text = text.replace("\n", " ")
    text = text.replace("  ", " ")
    return text.strip()

def fetch():
    feed = feedparser.parse(RSS_URL)

    now_jst = datetime.now(JST)
    cutoff_time = now_jst - timedelta(hours=24)

    news = []

    for entry in feed.entries:
        title = entry.title

        # 标记是否为转推
        is_retweet = title.startswith("RT by")

        # 解析发布时间
        dt_gmt = parsedate_to_datetime(entry.published)
        dt_jst = dt_gmt.astimezone(JST)

        # 只保留过去24小时
        if dt_jst < cutoff_time:
            continue

        news.append({
            "title": clean_text(title),
            "link": entry.link,
            "published": dt_jst.strftime("%Y-%m-%d %H:%M JST"),
            "is_retweet": is_retweet
        })

    return news

if __name__ == "__main__":
    news = fetch()

    data = {
        "updated": datetime.now(JST).strftime("%Y-%m-%d %H:%M JST"),
        "count": len(news),
        "news": news
    }

    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Fetched", len(news), "tweets in last 24 hours")
