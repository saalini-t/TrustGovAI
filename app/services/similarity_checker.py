from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")


def semantic_similarity(answer, context):

    emb1 = model.encode([answer])
    emb2 = model.encode([context])

    score = cosine_similarity(emb1, emb2)[0][0]

    return score