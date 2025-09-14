import requests
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_latest_articles():
    url = (
        f"https://newsapi.org/v2/top-headlines?"
        f"language=en&"
        f"pageSize=50&"
        f"apiKey={NEWS_API_KEY}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Return both title and URL
        articles = [
            {
                "title": f"{article['title']} - {article.get('description', '')}",
                "url": article.get("url")
            }
            for article in data.get("articles", [])
            if article.get("title") and article.get("url")
        ]
        return articles
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []
