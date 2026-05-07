from pathlib import Path
from fastapi import UploadFile

from app.services.uploads.saver import (
    save_upload_file
)

from app.services.medal.downloader import (
    download_medal_clip
)


def resolve_media_input(
    upload_file: UploadFile | None,
    medal_url: str | None
) -> Path:

    if upload_file:
        return save_upload_file(upload_file)

    if medal_url:
        return download_medal_clip(medal_url)

    raise ValueError(
        "Either upload_file or medal_url must be provided"
    )