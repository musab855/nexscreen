from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

@patch("app.api.routes.interview.retrieve_context")
@patch("app.api.routes.interview.generate_question")
def test_full_interview_workflow(mock_generate, mock_retrieve):
    mock_retrieve.return_value = [{"text": "Machine learning is a subset of AI.", "source": "test", "page": 1, "score": 0.1}]
    mock_generate.return_value = "What is the difference between supervised and unsupervised learning?"

    session_resp = client.post("/api/v1/session/start", json={
        "role": "ai_ml",
        "resume_text": "Python machine learning deep learning tensorflow",
        "extracted_skills": ["python", "machine learning", "tensorflow"],
        "candidate_name": "Test Candidate",
    })
    assert session_resp.status_code == 200
    session_id = session_resp.json()["id"]

    for i in range(5):
        q_resp = client.get(f"/api/v1/interview/{session_id}/next")
        assert q_resp.status_code == 200
        question_id = q_resp.json()["id"]

        a_resp = client.post(f"/api/v1/interview/{session_id}/answer", json={
            "question_id": question_id,
            "answer_text": f"Test answer {i+1}",
        })
        assert a_resp.status_code == 200

    with patch("app.api.routes.report.generate_report") as mock_report:
        mock_report.return_value = {
            "summary_text": "Good performance.",
            "insights": {
                "overall_summary": "Good performance.",
                "strengths": ["Python"],
                "areas_for_improvement": ["Math"],
                "technical_score": 7,
                "recommendation": "hire",
            }
        }
        report_resp = client.get(f"/api/v1/report/{session_id}")
        assert report_resp.status_code == 200
        assert report_resp.json()["insights"]["technical_score"] == 7