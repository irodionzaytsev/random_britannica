from flask import Flask
import string
import random
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

BASE_URL = "https://www.britannica.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; RandomArticleBot/1.0)"
}

def query_random_category():
    categories = ["0-9"] + list(string.ascii_lowercase)
    choice = random.choice(categories)

    return requests.get(
        f"{BASE_URL}/sitemap/{choice}",
        headers=HEADERS,
        timeout=5
    )

def query_random_topic(category):
    soup = BeautifulSoup(category.content, "html.parser")
    ul = soup.find("ul", class_="list-unstyled md-az-browse-content")

    if ul is None:
        return None

    links = ul.find_all("li")
    if not links:
        return None

    href = random.choice(links).find("a", href=True)["href"]
    return requests.get(
        BASE_URL + href,
        headers=HEADERS,
        timeout=5
    )

def get_random_article_link(topic):
    if topic is None:
        return "Failed to fetch topic."

    soup = BeautifulSoup(topic.content, "html.parser")
    ul = soup.find("ul", class_="list-unstyled md-az-browse-content")

    if ul is None:
        return "No articles found."

    links = ul.find_all("li")
    if not links:
        return "No articles found."

    href = random.choice(links).find("a", href=True)["href"]
    return f'<a href="{BASE_URL + href}">{href[1:]}</a>'

@app.route("/")
def main():
    category = query_random_category()
    topic = query_random_topic(category)
    return get_random_article_link(topic)
