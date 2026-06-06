from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import crud
from app.core.report_generator import generate_report
from app.schemas.report import ReportResponse
from app.utils.exceptions import SessionNotFoundError
import uuid

router = APIRouter()

@router.get("/{session_id}", response_model=ReportResponse)
def get_report(session_id: uuid.UUID, db: Session = Depends(get_db)):
    session = crud.get_session(db, session_id)
    if not session:
        raise SessionNotFoundError(f"Session {session_id} not found")

    questions = crud.get_session_questions(db, session_id)
    answers = crud.get_session_answers(db, session_id)

    answer_map = {str(a.question_id): a.answer_text for a in answers}
    qa_pairs = [
        {"question": q.question_text, "answer": answer_map.get(str(q.id), "No answer provided")}
        for q in questions
    ]

    result = generate_report(
        role=session.role,
        skills=session.extracted_skills or [],
        qa_pairs=qa_pairs,
    )

    crud.complete_session(db, session_id)

    report = crud.create_report(
        db=db,
        session_id=session_id,
        summary_text=result["summary_text"],
        insights=result["insights"],
    )
    return report