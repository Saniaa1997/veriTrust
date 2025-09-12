import requests

NEWS_API_KEY = "0b81860a23a24383bf0e605ca2ef8bf7"  # replace with your NewsAPI key

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

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_similarity_score(input_text, articles):
    """Return similarity scores between input and list of articles."""
    if not articles:
        return []
    documents = [input_text] + articles
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    return similarity

