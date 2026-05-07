from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import uuid

app = FastAPI(
    title="Whisk Render Service",
    version="0.1.0"
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
def root():
    return {
        "status": "running",
        "service": "Whisk Render Service"
    }

@app.get("/health")
def health_check():
    return {
        "healthy": True
    }

@app.post("/render")
async def render_video(
    clip1: UploadFile = File(...),
    clip2: UploadFile = File(...)
):
    
    allowed_types = ["video/mp4"]

    if clip1.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="clip1 must be an MP4 file"
        )

    if clip2.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="clip2 must be an MP4 file"
        )

    clip1_filename = f"{uuid.uuid4()}_{clip1.filename}"
    clip2_filename = f"{uuid.uuid4()}_{clip2.filename}"

    clip1_path = UPLOAD_DIR / clip1_filename
    clip2_path = UPLOAD_DIR / clip2_filename

    with clip1_path.open("wb") as buffer:
        shutil.copyfileobj(clip1.file, buffer)

    with clip2_path.open("wb") as buffer:
        shutil.copyfileobj(clip2.file, buffer)

    return {
        "message": "Files uploaded successfully",
        "clip1": str(clip1_path),
        "clip2": str(clip2_path)
    }