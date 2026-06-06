from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import crud
from app.core.query_builder import build_retrieval_query, get_role_topics
from app.core.question_generator import generate_question
from app.rag.retriever import retrieve_context
from app.schemas.interview import QuestionResponse, AnswerSubmitRequest
from app.utils.exceptions import SessionNotFoundError
import uuid

router = APIRouter()

@router.get("/{session_id}/next", response_model=QuestionResponse)
def get_next_question(session_id: uuid.UUID, db: Session = Depends(get_db)):
    session = crud.get_session(db, session_id)
    if not session:
        raise SessionNotFoundError(f"Session {session_id} not found")

    previous_questions = crud.get_session_questions(db, session_id)
    question_order = len(previous_questions) + 1

    topics = get_role_topics(session.role)
    topic = topics[(question_order - 1) % len(topics)]
    skills = session.extracted_skills or []
    query = f"{topic} {' '.join(skills[:3])}"

    chunks = retrieve_context(query=query, role=session.role)
    prev_texts = [q.question_text for q in previous_questions]

    question_text = generate_question(
        role=session.role,
        skills=skills,
        context_chunks=chunks,
        previous_questions=prev_texts,
    )

    question = crud.create_question(
        db=db,
        session_id=session_id,
        question_text=question_text,
        retrieved_context=chunks[0]["text"] if chunks else "",
        question_order=question_order,
    )
    return question

@router.post("/{session_id}/answer")
def submit_answer(session_id: uuid.UUID, request: AnswerSubmitRequest, db: Session = Depends(get_db)):
    session = crud.get_session(db, session_id)
    if not session:
        raise SessionNotFoundError(f"Session {session_id} not found")

    answer = crud.create_answer(
        db=db,
        question_id=request.question_id,
        session_id=session_id,
        answer_text=request.answer_text,
    )
    return {"status": "ok", "answer_id": str(answer.id)}
