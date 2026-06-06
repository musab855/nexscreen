from pydantic import BaseModel
from typing import Any
from uuid import UUID
from datetime import datetime

class ReportResponse(BaseModel):
    id: UUID
    session_id: UUID
    summary_text: str
    insights: Any
    created_at: datetime

    class Config:
        from_attributes = True