from app.core.resume_parser import extract_skills, extract_candidate_name

def test_extract_skills_found():
    text = "Experienced in Python, FastAPI, PostgreSQL and machine learning"
    skills = extract_skills(text)
    assert "python" in skills
    assert "fastapi" in skills
    assert "postgresql" in skills

def test_extract_skills_empty():
    skills = extract_skills("")
    assert skills == []

def test_extract_candidate_name():
    text = "John Smith\nSoftware Engineer\nPython | FastAPI"
    name = extract_candidate_name(text)
    assert name == "John Smith"