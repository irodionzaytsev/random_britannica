import requests
import string
import random
import json
import time
from bs4 import BeautifulSoup

BASE = "https://www.britannica.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

articles = []

# Scrape each category
for c in ["0-9"] + list(string.ascii_lowercase):
    try:
        r = requests.get(f"{BASE}/sitemap/{c}", headers=HEADERS, timeout=10)
        if r.status_code != 200:
            continue
        soup = BeautifulSoup(r.text, "html.parser")
        ul = soup.find("ul", class_="list-unstyled md-az-browse-content")
        if not ul:
            continue
        for li in ul.find_all("li"):
            href = li.find("a", href=True)["href"]
            articles.append(BASE + href)
        time.sleep(1)
    except Exception as e:
        print(f"Category {c} failed: {e}")

# Save to JSON
with open("topics.json", "w") as f:
    json.dump(articles, f, indent=2)

print(f"Scraped {len(articles)} articles.")
