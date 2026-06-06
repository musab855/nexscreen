import chromadb
from app.rag.embedder import embed_text
from app.rag.ingestion import get_chroma_client
from app.config import get_settings
from app.utils.exceptions import RetrievalError

settings = get_settings()

def retrieve_context(query: str, role: str, n_results: int = 5) -> list[dict]:
    try:
        client = get_chroma_client()
        collection = client.get_collection(name=f"nexscreen_{role}")
        query_embedding = embed_text(query)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
        )
        chunks = []
        for i, doc in enumerate(results["documents"][0]):
            chunks.append({
                "text": doc,
                "source": results["metadatas"][0][i]["source"],
                "page": results["metadatas"][0][i]["page"],
                "score": results["distances"][0][i],
            })
        return chunks
    except Exception as e:
        raise RetrievalError(str(e))