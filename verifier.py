# verifier.py

import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Replace this with your NewsAPI key
NEWS_API_KEY = "YOUR_NEWS_API_KEY"

def fetch_related_articles(query):
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&pageSize=5&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        articles = response.json()["articles"]
        titles = [article["title"] for article in articles]
        return titles
    else:
        print("❌ Error fetching articles:", response.status_code)
        return []

def get_similarity_score(input_text, article_titles):
    texts = [input_text] + article_titles
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    # Compare input (index 0) with the others
    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    return similarities[0]  # returns a list of similarity scores

def verify_news(input_headline):
    articles = fetch_related_articles(input_headline)

    if not articles:
        return "Needs Verification", [], []

    scores = get_similarity_score(input_headline, articles)
    avg_score = sum(scores) / len(scores)

    if avg_score > 0.5:
        label = "Likely True"
    elif avg_score > 0.2:
        label = "Needs Verification"
    else:
        label = "Likely False"

    return label, scores, articles
