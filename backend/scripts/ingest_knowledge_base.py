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
    for book in BOOKS:
        if os.path.exists(book["path"]):
            logger.info("starting_ingestion", source=book["source_name"])
            ingest_pdf(book["path"], book["role"], book["source_name"])
        else:
            logger.warning("file_not_found", path=book["path"])
