from flask import Flask
import string, random, requests
from bs4 import BeautifulSoup

app = Flask(__name__)

BASE = "https://www.britannica.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def query_random_category():
    categories = ["0-9"] + list(string.ascii_lowercase)
    choice = random.choice(categories)
    r = requests.get(f"{BASE}/sitemap/{choice}", headers=HEADERS, timeout=10)
    if r.status_code != 200: return None
    return r

def query_random_topic(category):
    if category is None: return None
    soup = BeautifulSoup(category.content, "html.parser")
    ul = soup.find("ul", class_="list-unstyled md-az-browse-content")
    if not ul: return None
    links = ul.find_all("li")
    if not links: return None
    href = random.choice(links).find("a", href=True)["href"]
    return requests.get(BASE + href, headers=HEADERS, timeout=10)

def get_random_article_link(topic):
    if topic is None: return "Failed to fetch topic."
    soup = BeautifulSoup(topic.content, "html.parser")
    ul = soup.find("ul", class_="list-unstyled md-az-browse-content")
    if not ul: return "No articles found."
    links = ul.find_all("li")
    if not links: return "No articles found."
    href = random.choice(links).find("a", href=True)["href"]
    return f'<a href="{BASE + href}">{href[1:]}</a>'

@app.route("/")
def main():
    category = query_random_category()
    topic = query_random_topic(category)
    return get_random_article_link(topic)
