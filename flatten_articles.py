import json
with open("britannica_articles.json","r") as f:
    articles = json.load(f)
articles_array = []
for topic in articles:
    for section in articles[topic]:
        articles_array.extend(articles[topic][section])

with open("articles_array.json","w") as f:
    json.dump(articles_array,f)