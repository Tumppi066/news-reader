import xml.etree.ElementTree as ET
from classes import Article
import requests
import time


# RSS feeds to monitor for news
feeds = [
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml", # World News
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml", # Tech
    "https://feeds.bbci.co.uk/news/world/rss.xml" # World News
]


def get_feed_for(hours: int = 24) -> list[Article]:
    since = time.time() - hours * 3600
    articles = []   
    for feed in feeds:
        print(f"Fetching feed: {feed}")
        response = requests.get(feed)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for item in root.findall(".//item"):
                pub_date = item.find("pubDate")
                if pub_date is not None:
                    if "nytimes" in feed or "yle" in feed:
                        # For NYT <pubDate>Wed, 11 Jun 2025 09:00:00 +0000</pubDate>
                        pub_date_time = time.mktime(time.strptime(pub_date.text, "%a, %d %b %Y %H:%M:%S %z"))
                    elif "bbc" in feed:
                        # For BBC <pubDate>Wed, 11 Jun 2025 09:00:00 GMT</pubDate>
                        pub_date_time = time.mktime(time.strptime(pub_date.text, "%a, %d %b %Y %H:%M:%S GMT"))
                    else:
                        # Fallback for other feeds
                        pub_date_time = time.mktime(time.strptime(pub_date.text, "%a, %d %b %Y %H:%M:%S %Z"))
                        
                    if pub_date_time > since:
                        if item.find("title") is not None and item.find("description") is not None and item.find("link") is not None:
                            article = Article(
                                title=item.find("title").text,
                                description=item.find("description").text,
                                url=item.find("link").text
                            )
                            articles.append(article)
        time.sleep(1)
        
    return articles