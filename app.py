from flask import Flask
import string
import random
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)

def get_base_url():
    """returns the url of britannica website"""
    return "https://www.britannica.com"

def query_random_category():
    """This function returns the html query of a random category on the britannica.com website."""
    categories = ["0-9"] + list(string.ascii_lowercase)
    choice = random.choice(categories)
    return requests.get(get_base_url() + "/sitemap/"+ choice)

def query_random_topic(category):
    soup = BeautifulSoup(category.content, "html.parser")
    links_section = soup.find("ul",class_="list-unstyled md-az-browse-content")
    links = links_section.find_all("li")
    random_link = random.choice(links).find("a", href=True)['href']
    return requests.get(get_base_url() + random_link)

def get_random_article_link(topic):
    soup = BeautifulSoup(topic.content, "html.parser")
    links_section = soup.find("ul", class_="list-unstyled md-az-browse-content")
    links = links_section.find_all("li")
    random_link = random.choice(links).find("a", href=True)['href']
    link = get_base_url() + random_link

    return "<a href="+link+">"+random_link[1:]+"</a>"
@app.route('/')
def main():  # put application's code here
    return "SANITY CHECK"
    category = query_random_category()
    topic = query_random_topic(category)
    article = get_random_article_link(topic)
    return article

if __name__ == '__main__':
    app.run()
