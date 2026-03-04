# fetch_lovelive.py
import feedparser
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime

RSS_URL = "https://nitter.net/LoveLive_staff/rss"
JST = timezone(timedelta(hours=9))

def clean_text(text):
    return text.replace("\n", " ").replace("  ", " ").strip()

def fetch():
    feed = feedparser.parse(RSS_URL)
    now_jst = datetime.now(JST)
    cutoff_time = now_jst - timedelta(hours=24)
    messages = []

    for entry in feed.entries:
        title = entry.title
        if title.startswith("RT by"):  # 忽略转推
            continue
        dt_gmt = parsedate_to_datetime(entry.published)
        dt_jst = dt_gmt.astimezone(JST)
        if dt_jst < cutoff_time:
            continue
        messages.append(f"{dt_jst.strftime('%Y-%m-%d %H:%M JST')} {clean_text(title)}\n{entry.link}")

    return messages

if __name__ == "__main__":
    for msg in fetch():
        print(msg)
