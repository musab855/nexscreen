from pydantic import BaseModel, ConfigDict
from typing import Any
from uuid import UUID
from datetime import datetime

class ReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    session_id: UUID
    summary_text: str
    insights: Any
    created_at: datetime