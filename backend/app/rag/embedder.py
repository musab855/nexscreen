from sentence_transformers import SentenceTransformer
from functools import lru_cache

@lru_cache()
def get_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str) -> list:
    model = get_embedding_model()
    return model.encode(text).tolist()

def embed_texts(texts: list) -> list:
    model = get_embedding_model()
    return model.encode(texts).tolist()