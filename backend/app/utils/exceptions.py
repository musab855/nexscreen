from fastapi import HTTPException, status

class ResumeParsingError(Exception):
    pass

class RetrievalError(Exception):
    pass

class SessionNotFoundError(Exception):
    pass

class QuestionGenerationError(Exception):
    pass