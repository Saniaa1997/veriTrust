import requests
import streamlit as st
from dotenv import load_dotenv
import os
from utils import similarity_score


load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")



@st.cache_data(show_spinner=False)
def fetch_related_articles(query):
    """Fetch top 5 related news article titles from NewsAPI."""
    url = (
        f"https://newsapi.org/v2/everything?q={query}"
        f"&sortBy=relevancy&pageSize=5&apiKey={NEWS_API_KEY}"
    )
    response = requests.get(url)
    if response.status_code != 200:
        print("❌ Error fetching articles:", response.status_code)
        return []
    articles = response.json().get("articles", [])
    return [article["title"] for article in articles]



def verify_news(input_text):
     """
    Verifies a news headline or snippet by fetching relevant articles
    and calculating similarity scores.

    Args:
        input_text (str): The news headline or text snippet to verify.

    Returns:
        tuple: (label, similarity_scores, articles)
            label (str): "Likely True", "Likely False", or "Needs Verification"
            similarity_scores (list): List of similarity scores
            articles (list): List of fetched article summaries
    """
    articles = fetch_related_articles(input_text)
    if not articles:
        print("No articles found — skipping similarity.")
        return ("Needs Verification", [], [])

    similarity_scores = similarity_score(input_text, articles)

    if not similarity_scores.any():
        return "Needs Verification", [], []

    avg_score = sum(similarity_scores) / len(similarity_scores)

    if avg_score > 0.5:
        label = "Likely True"
    elif avg_score < 0.2:
        label = "Likely False"
    else:
        label = "Needs Verification"

    return label, similarity_scores, articles


