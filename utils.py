from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def similarity_score(input_text, article_titles):
    """Compute similarity score between input and article titles."""
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([input_text] + article_titles)
    scores = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    return scores
 
