import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

URL = "https://www.lovelive-anime.jp/yuigaoka/topics/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

res = requests.get(URL, headers=headers)
res.encoding = "utf-8"

soup = BeautifulSoup(res.text, "html.parser")

items = []

for a in soup.select("a"):
    href = a.get("href", "")
    if "/yuigaoka/topics/" in href and href != "/yuigaoka/topics/":
        title = a.text.strip()
        if title:
            items.append({
                "title": title,
                "url": "https://www.lovelive-anime.jp" + href
            })

# 去重
unique = {item["url"]: item for item in items}
news_list = list(unique.values())[:5]

data = {
    "updated": datetime.now().isoformat(),
    "news": news_list
}

with open("news.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("News saved.")
