from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class SessionCreateRequest(BaseModel):
    role: str
    resume_text: str
    extracted_skills: List[str]
    candidate_name: Optional[str] = None

class SessionResponse(BaseModel):
    id: UUID
    role: str
    candidate_name: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True