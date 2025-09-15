import requests
import os
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_latest_articles(location="India", limit=10000):
    """
    Fetch latest news articles filtered by location (dynamic input from user)
    using NewsAPI.
    """
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={location}&"
        f"language=en&"
        f"pageSize={limit}&"
        f"sortBy=publishedAt&"
        f"apiKey={NEWS_API_KEY}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        articles = [
            {
                "title": a.get("title", ""),
                "description": a.get("description", ""),
                "text": f"{a.get('title','')} {a.get('description','')}",
                "url": a.get("url")
            }
            for a in data.get("articles", [])
            if a.get("title") and a.get("url")
        ]
        return articles
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []
