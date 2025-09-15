from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def similarity_score(input_text, articles, top_n=10):
    if not articles:
        return []

    texts = [a["text"] for a in articles]
    embeddings = model.encode([input_text] + texts, convert_to_tensor=True)
    input_emb = embeddings[0]
    article_embs = embeddings[1:]

    scores = util.cos_sim(input_emb, article_embs)[0]

    results = []
    for i, score in enumerate(scores):
        results.append({
            "title": articles[i]["title"],
            "description": articles[i]["description"],
            "url": articles[i]["url"],
            "score": float(score)
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]
