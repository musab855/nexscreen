from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from app.config import get_settings
from app.utils.exceptions import RetrievalError
from functools import lru_cache

settings = get_settings()

@lru_cache()
def get_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

def get_pinecone_index():
    pc = Pinecone(api_key=settings.pinecone_api_key)
    return pc.Index(settings.pinecone_index)

def retrieve_context(query: str, role: str, n_results: int = 5) -> list[dict]:
    try:
        model = get_embedding_model()
        query_embedding = model.encode(query).tolist()
        index = get_pinecone_index()
        results = index.query(
            vector=query_embedding,
            top_k=n_results,
            namespace=role,
            include_metadata=True,
        )
        chunks = []
        for match in results.matches:
            chunks.append({
                "text": match.metadata.get("text", ""),
                "source": match.metadata.get("source", ""),
                "page": match.metadata.get("page", 0),
                "score": match.score,
            })
        return chunks
    except Exception as e:
        raise RetrievalError(str(e))