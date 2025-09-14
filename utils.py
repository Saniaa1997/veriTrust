from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def similarity_score(input_text, articles):
    """
    Computes similarity between input_text and each article['title']
    Returns list of (title, url, similarity)
    """
    titles = [a["title"] for a in articles]
    embeddings = model.encode([input_text] + titles, convert_to_tensor=True)
    input_embedding = embeddings[0]
    article_embeddings = embeddings[1:]

    scores = util.pytorch_cos_sim(input_embedding, article_embeddings)[0].cpu().numpy()

    results = []
    for i in range(len(articles)):
        results.append({
            "title": articles[i]["title"],
            "url": articles[i]["url"],
            "score": float(scores[i])
        })
    
    # Sort by descending similarity
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results
