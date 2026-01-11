import requests
from bs4 import BeautifulSoup
import json
import time

BASE = "https://www.britannica.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": BASE
}

# Load your existing JSON of topic URLs
with open("topics.json") as f:  # this should have z -> 22 links etc.
    topics = json.load(f)
# read articles that were already loaded
with open("britannica_articles.json") as f:
    all_articles = json.load(f)

for link in topics:
    letter, topic = link.split('/')[-2:]
    if letter not in all_articles:
        all_articles[letter] = {}
    if topic in all_articles[letter]:
        continue
    topic_url = f'{BASE}/sitemap/{letter}/{topic}'
    print(f"Scraping topic: {topic_url}")
    try:
        r = requests.get(topic_url, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            print(f"Failed to fetch {topic_url}")
            continue
        soup = BeautifulSoup(r.text, "html.parser")
        ul = soup.find("ul", class_="list-unstyled md-az-browse-content")
        if not ul:
            print(f"No article list found on {topic_url}")
            continue
        links = [BASE + a['href'] for a in ul.find_all("a", href=True)]
        all_articles[letter][topic] = links
        time.sleep(0.5)  # be polite
    except Exception as e:
        print(f"Error scraping {topic_url}: {e}")
        continue

# Save hierarchical JSON
with open("britannica_articles.json", "w") as f:
    json.dump(all_articles, f, indent=2)

print("Scraping complete.")
# currently we got letters up to t. To be continued from there