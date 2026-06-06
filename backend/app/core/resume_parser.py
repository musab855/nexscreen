import fitz  # type: ignore
import re
from app.utils.exceptions import ResumeParsingError

SKILLS_KEYWORDS = [
    "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust",
    "fastapi", "flask", "django", "express", "nextjs", "react", "vue", "angular",
    "postgresql", "mysql", "mongodb", "redis", "sqlite",
    "docker", "kubernetes", "aws", "gcp", "azure", "git", "github",
    "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
    "machine learning", "deep learning", "nlp", "computer vision",
    "langchain", "llamaindex", "chromadb", "pinecone",
    "hugging face", "transformers", "rag", "llm",
    "rest api", "graphql", "microservices", "ci/cd",
]

def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text.strip()
    except Exception as e:
        raise ResumeParsingError(f"Failed to parse resume: {str(e)}")

def extract_skills(text: str) -> list[str]:
    text_lower = text.lower()
    found = [skill for skill in SKILLS_KEYWORDS if skill in text_lower]
    return list(set(found))

def extract_candidate_name(text: str) -> str | None:
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if lines:
        first_line = lines[0]
        if len(first_line.split()) <= 4 and first_line.istitle():
            return first_line
    return None

def parse_resume(file_bytes: bytes) -> dict:
    text = extract_text_from_pdf(file_bytes)
    skills = extract_skills(text)
    name = extract_candidate_name(text)
    return {
        "resume_text": text,
        "extracted_skills": skills,
        "candidate_name": name,
    }
