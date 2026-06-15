import fitz
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from app.config import get_settings
from app.utils.logger import logger

settings = get_settings()
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_pinecone_index():
    pc = Pinecone(api_key=settings.pinecone_api_key)
    return pc.Index(settings.pinecone_index)

def extract_text_from_pdf(pdf_path: str) -> list[str]:
    doc = fitz.open(pdf_path)
    pages = []
    for page in doc:
        text = page.get_text().strip()
        if text:
            pages.append(text)
    return pages

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def ingest_pdf(pdf_path: str, role: str, source_name: str):
    logger.info("ingesting_pdf", path=pdf_path, role=role)
    index = get_pinecone_index()
    pages = extract_text_from_pdf(pdf_path)

    all_chunks = []
    for page_num, page_text in enumerate(pages):
        chunks = chunk_text(page_text)
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "id": f"{source_name}_p{page_num+1}_{i}",
                "text": chunk,
                "source": source_name,
                "page": page_num + 1,
                "role": role,
            })

    batch_size = 96
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i:i+batch_size]
        texts = [c["text"] for c in batch]
        embeddings = model.encode(texts).tolist()
        vectors = [
            {
                "id": c["id"],
                "values": emb,
                "metadata": {
                    "text": c["text"],
                    "source": c["source"],
                    "page": c["page"],
                    "role": c["role"],
                }
            }
            for c, emb in zip(batch, embeddings)
        ]
        index.upsert(vectors=vectors, namespace=role)

    logger.info("ingestion_complete", chunks=len(all_chunks), role=role)