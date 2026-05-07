from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.services.medal.downloader import download_medal_clip
from app.services.rendering.renderer import (
    render_side_by_side,
    OUTPUT_DIR
)
from app.services.uploads.saver import save_upload_file

app = FastAPI(
    title="Whisk Render Service",
    version="0.1.0"
)

class MedalRenderRequest(BaseModel):
    clip1_url: str
    clip2_url: str

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
    clip1_path = save_upload_file(clip1)
    clip2_path = save_upload_file(clip2)

    output_path = render_side_by_side(
        clip1_path,
        clip2_path
    )

    return {
    "message": "Render completed successfully",
    "output_video": str(output_path),
    "download_url": f"/download/{output_path.name}"
    }

@app.post("/render-medal")
async def render_medal_video(
    request: MedalRenderRequest
):

    clip1_path = download_medal_clip(
        request.clip1_url
    )

    clip2_path = download_medal_clip(
        request.clip2_url
    )

    output_path = render_side_by_side(
        clip1_path,
        clip2_path
    )

    return {
        "message": "Medal render completed successfully",
        "output_video": str(output_path),
        "download_url": f"/download/{output_path.name}"
    }

@app.get("/download/{filename}")
async def download_video(filename: str):

    file_path = OUTPUT_DIR / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    return FileResponse(
        path=file_path,
        media_type="video/mp4",
        filename=filename
    )