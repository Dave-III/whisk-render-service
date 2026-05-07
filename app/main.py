from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import uuid
import subprocess

app = FastAPI(
    title="Whisk Render Service",
    version="0.1.0"
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

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

    output_filename = f"{uuid.uuid4()}.mp4"
    output_path = OUTPUT_DIR / output_filename

    ffmpeg_command = [
        "ffmpeg",
        "-y",
        "-i", str(clip1_path),
        "-i", str(clip2_path),
        "-filter_complex",
        (
            "[0:v]scale=960:1080[left];"
            "[1:v]scale=960:1080[right];"
            "[left][right]hstack=inputs=2[v]"
        ),
        "-map", "[v]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        str(output_path)
    ]

    subprocess.run(ffmpeg_command, check=True)

    return {
        "message": "Render completed successfully",
        "output_video": str(output_path)
    }
