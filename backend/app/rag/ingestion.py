import fitz
import chromadb
from pathlib import Path
from app.rag.embedder import embed_texts
from app.config import get_settings
from app.utils.logger import logger

settings = get_settings()

def get_chroma_client():
    return chromadb.PersistentClient(path=settings.chroma_persist_dir)

def get_collection(role: str):
    client = get_chroma_client()
    return client.get_or_create_collection(name=f"nexscreen_{role}")

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
    pages = extract_text_from_pdf(pdf_path)
    all_chunks = []
    for page_num, page_text in enumerate(pages):
        chunks = chunk_text(page_text)
        all_chunks.extend([
            {"text": c, "page": page_num + 1}
            for c in chunks
        ])

    collection = get_collection(role)
    texts = [c["text"] for c in all_chunks]
    embeddings = embed_texts(texts)
    ids = [f"{source_name}_p{c['page']}_{i}" for i, c in enumerate(all_chunks)]
    metadatas = [{"source": source_name, "page": c["page"], "role": role} for c in all_chunks]

    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas,
    )
    logger.info("ingestion_complete", chunks=len(all_chunks), role=role)