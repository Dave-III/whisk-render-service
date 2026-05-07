from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.services.youtube.uploader import upload_video
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

    clip1: UploadFile | None = File(None),
    clip2: UploadFile | None = File(None),

    clip1_url: str | None = Form(None),
    clip2_url: str | None = Form(None)
):

    allowed_types = ["video/mp4"]


    if clip1 and clip1_url:
        raise HTTPException(
            status_code=400,
            detail="Provide either clip1 upload OR clip1_url, not both"
        )

    if not clip1 and not clip1_url:
        raise HTTPException(
            status_code=400,
            detail="clip1 upload or clip1_url is required"
        )


    if clip2 and clip2_url:
        raise HTTPException(
            status_code=400,
            detail="Provide either clip2 upload OR clip2_url, not both"
        )

    if not clip2 and not clip2_url:
        raise HTTPException(
            status_code=400,
            detail="clip2 upload or clip2_url is required"
        )

    if clip1:

        if clip1.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail="clip1 must be an MP4 file"
            )

        clip1_path = save_upload_file(clip1)

    else:
        clip1_path = download_medal_clip(
            clip1_url
        )


    if clip2:

        if clip2.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail="clip2 must be an MP4 file"
            )

        clip2_path = save_upload_file(clip2)

    else:
        clip2_path = download_medal_clip(
            clip2_url
        )

    try:

        output_path = render_side_by_side(
            clip1_path,
            clip2_path
        )

        youtube_url = upload_video(
            output_path
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return {
        "message": "Render completed successfully",
        "output_video": str(output_path),
        "download_url": f"/download/{output_path.name}",
        "youtube_url": youtube_url
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