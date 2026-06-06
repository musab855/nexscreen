from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.resume_parser import parse_resume
from app.schemas.resume import ResumeUploadResponse
from app.config import get_settings

settings = get_settings()
router = APIRouter()

@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")
    
    size = 0
    file_bytes = await file.read()
    size = len(file_bytes)
    
    if size > settings.max_upload_size_mb * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")
    
    result = parse_resume(file_bytes)
    return ResumeUploadResponse(**result)
