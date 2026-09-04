from functools import lru_cache
import time
import fitz
from pinecone import Pinecone
from google import genai
from google.genai import types
from google.genai.errors import ClientError
from app.config import get_settings
from app.utils.logger import logger

settings = get_settings()

@lru_cache()
def get_pinecone_index():
    pc = Pinecone(api_key=settings.pinecone_api_key)
    return pc.Index(settings.pinecone_index)

@lru_cache()
def get_gemini_client():
    return genai.Client(api_key=settings.gemini_api_key)

def embed_texts(texts: list[str], task_type: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    client = get_gemini_client()
    for attempt in range(10):
        try:
            result = client.models.embed_content(
                model="gemini-embedding-001",
                contents=texts,
                config=types.EmbedContentConfig(
                    task_type=task_type,
                    output_dimensionality=768,
                ),
            )
            return [e.values for e in result.embeddings]
        except ClientError as e:
            if "429" in str(e) and attempt < 9:
                wait = 30 * (attempt + 1)
                logger.warning("rate_limited", wait=wait, attempt=attempt+1)
                time.sleep(wait)
            else:
                raise

def is_already_ingested(source_name: str, role: str) -> bool:
    index = get_pinecone_index()
    results = index.query(
        vector=[0.1] * 768,
        top_k=1,
        namespace=role,
        include_metadata=True,
        filter={"source": source_name},
    )
    return len(results.matches) > 0

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
    if is_already_ingested(source_name, role):
        logger.info("skipping_already_ingested", source=source_name)
        return

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

    batch_size = 5
    total_batches = (len(all_chunks) + batch_size - 1) // batch_size

    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i:i+batch_size]
        texts = [c["text"] for c in batch]
        batch_num = i // batch_size + 1

        try:
            embeddings = embed_texts(texts)
        except ClientError:
            logger.error("quota_exhausted", source=source_name, failed_batch=f"{batch_num}/{total_batches}", resume_msg="Run script again tomorrow to continue from this point")
            return

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
        index.upsert(vectors=vectors, namespace=batch[0]["role"])
        logger.info("batch_upserted", source=source_name, batch=f"{batch_num}/{total_batches}")
        time.sleep(2.5)

    logger.info("ingestion_complete", chunks=len(all_chunks), role=role)
