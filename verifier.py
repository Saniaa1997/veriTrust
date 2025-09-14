import requests
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_latest_headlines():
    url = (
        f"https://newsapi.org/v2/top-headlines?"
        f"language=en&"
        f"pageSize=30&"
        f"apiKey={NEWS_API_KEY}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        headlines = [article["title"] for article in data.get("articles", []) if article.get("title")]
        return headlines
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []
