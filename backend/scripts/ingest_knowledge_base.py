import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.rag.ingestion import ingest_pdf
from app.utils.logger import logger

BOOKS = [
    {"path": "knowledge_base/ml_tom_mitchell.pdf", "role": "ai_ml", "source_name": "ml_tom_mitchell"},
    {"path": "knowledge_base/hundred_page_ml.pdf", "role": "ai_ml", "source_name": "hundred_page_ml"},
    {"path": "knowledge_base/ml_absolute_beginners.pdf", "role": "ai_ml", "source_name": "ml_absolute_beginners"},
    {"path": "knowledge_base/intro_ml_python.pdf", "role": "data_science", "source_name": "intro_ml_python"},
    {"path": "knowledge_base/master_ml_algorithms.pdf", "role": "data_science", "source_name": "master_ml_algorithms"},
    {"path": "knowledge_base/pattern_recognition_bishop.pdf", "role": "ai_ml", "source_name": "pattern_recognition_bishop"},
    {"path": "knowledge_base/ai_ml_deep_learning.pdf", "role": "ai_ml", "source_name": "ai_ml_deep_learning"},
]

if __name__ == "__main__":
    completed = []
    skipped = []
    failed = []

    for book in BOOKS:
        if not os.path.exists(book["path"]):
            logger.warning("file_not_found", path=book["path"])
            failed.append(book["source_name"])
            continue

        logger.info("starting_ingestion", source=book["source_name"])
        try:
            ingest_pdf(book["path"], book["role"], book["source_name"])
            completed.append(book["source_name"])
        except Exception as e:
            logger.error("ingestion_failed", source=book["source_name"], error=str(e))
            failed.append(book["source_name"])
            break

    print(f"\nCompleted: {completed}")
    if skipped:
        print(f"Skipped (already ingested): {skipped}")
    if failed:
        print(f"Failed (resume tomorrow): {failed}")
