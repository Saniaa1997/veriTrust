from sentence_transformers import SentenceTransformer, util

# Load model once globally
model = SentenceTransformer('all-MiniLM-L6-v2')

def similarity_score(input_text, article_titles):
    """
    Computes semantic similarity (BERT-based) between input and real news articles.
    """
    # Combine input + articles
    embeddings = model.encode([input_text] + article_titles, convert_to_tensor=True)
    
    input_embedding = embeddings[0]
    article_embeddings = embeddings[1:]

    scores = util.pytorch_cos_sim(input_embedding, article_embeddings)[0]
    return scores.cpu().numpy()  # return as list of floats
