from pydantic import BaseModel
from uuid import UUID

class QuestionResponse(BaseModel):
    id: UUID
    question_text: str
    question_order: int

    class Config:
        from_attributes = True

class AnswerSubmitRequest(BaseModel):
    question_id: UUID
    answer_text: str