from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import crud
from app.schemas.session import SessionCreateRequest, SessionResponse
from app.utils.exceptions import SessionNotFoundError
import uuid

router = APIRouter()

@router.post("/start", response_model=SessionResponse)
def start_session(request: SessionCreateRequest, db: Session = Depends(get_db)):
    session = crud.create_session(
        db=db,
        role=request.role,
        resume_text=request.resume_text,
        extracted_skills=request.extracted_skills,
        candidate_name=request.candidate_name,
    )
    return session

@router.get("/{session_id}", response_model=SessionResponse)
def get_session(session_id: uuid.UUID, db: Session = Depends(get_db)):
    session = crud.get_session(db, session_id)
    if not session:
        raise SessionNotFoundError(f"Session {session_id} not found")
    return session
