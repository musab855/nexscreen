import uuid
from sqlalchemy.orm import Session
from app.db.models import InterviewSession, Question, Answer, Report, SessionStatus
from datetime import datetime


def create_session(db: Session, role: str, resume_text: str, extracted_skills: list, candidate_name: str = None):
    session = InterviewSession(
        id=uuid.uuid4(),
        role=role,
        resume_text=resume_text,
        extracted_skills=extracted_skills,
        candidate_name=candidate_name,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_session(db: Session, session_id: uuid.UUID):
    return db.query(InterviewSession).filter(InterviewSession.id == session_id).first()


def create_question(db: Session, session_id: uuid.UUID, question_text: str, retrieved_context: str, question_order: int):
    question = Question(
        id=uuid.uuid4(),
        session_id=session_id,
        question_text=question_text,
        retrieved_context=retrieved_context,
        question_order=question_order,
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def create_answer(db: Session, question_id: uuid.UUID, session_id: uuid.UUID, answer_text: str):
    answer = Answer(
        id=uuid.uuid4(),
        question_id=question_id,
        session_id=session_id,
        answer_text=answer_text,
    )
    db.add(answer)
    db.commit()
    db.refresh(answer)
    return answer


def get_session_questions(db: Session, session_id: uuid.UUID):
    return db.query(Question).filter(Question.session_id == session_id).order_by(Question.question_order).all()


def get_session_answers(db: Session, session_id: uuid.UUID):
    return db.query(Answer).filter(Answer.session_id == session_id).all()


def complete_session(db: Session, session_id: uuid.UUID):
    session = get_session(db, session_id)
    session.status = SessionStatus.completed
    session.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(session)
    return session


def create_report(db: Session, session_id: uuid.UUID, summary_text: str, insights: dict):
    report = Report(
        id=uuid.uuid4(),
        session_id=session_id,
        summary_text=summary_text,
        insights=insights,
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report