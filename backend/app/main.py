from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import get_settings
from app.utils.logger import logger
from app.utils.exceptions import (
    ResumeParsingError,
    RetrievalError,
    SessionNotFoundError,
    QuestionGenerationError,
)

settings = get_settings()

app = FastAPI(
    title="NexScreen API",
    version="1.0.0",
    docs_url="/docs" if settings.app_env == "development" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(ResumeParsingError)
async def resume_parsing_handler(request: Request, exc: ResumeParsingError):
    return JSONResponse(status_code=422, content={"error": str(exc), "code": "RESUME_PARSE_ERROR"})

@app.exception_handler(RetrievalError)
async def retrieval_handler(request: Request, exc: RetrievalError):
    return JSONResponse(status_code=500, content={"error": str(exc), "code": "RETRIEVAL_ERROR"})

@app.exception_handler(SessionNotFoundError)
async def session_handler(request: Request, exc: SessionNotFoundError):
    return JSONResponse(status_code=404, content={"error": str(exc), "code": "SESSION_NOT_FOUND"})

@app.exception_handler(QuestionGenerationError)
async def question_handler(request: Request, exc: QuestionGenerationError):
    return JSONResponse(status_code=500, content={"error": str(exc), "code": "QUESTION_GEN_ERROR"})

@app.get("/health")
async def health():
    return {"status": "ok", "env": settings.app_env}


from app.api.routes import resume, session, interview, report

app.include_router(resume.router, prefix="/api/v1/resume", tags=["resume"])
app.include_router(session.router, prefix="/api/v1/session", tags=["session"])
app.include_router(interview.router, prefix="/api/v1/interview", tags=["interview"])
app.include_router(report.router, prefix="/api/v1/report", tags=["report"])