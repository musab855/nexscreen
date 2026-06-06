from pydantic import BaseModel
from typing import List, Optional

class ResumeUploadResponse(BaseModel):
    candidate_name: Optional[str]
    extracted_skills: List[str]
    resume_text: str