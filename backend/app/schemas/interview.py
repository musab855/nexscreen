from pydantic import BaseModel, ConfigDict
from uuid import UUID

class QuestionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    question_text: str
    question_order: int

class AnswerSubmitRequest(BaseModel):
    question_id: UUID
    answer_text: str