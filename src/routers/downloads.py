from uuid import UUID

from fastapi import APIRouter, HTTPException, status

import services
from schemas.downloads import DownloadCreate, DownloadCreated, DownloadDetail

router = APIRouter()


@router.post("/downloads")
async def post_downloads(download: DownloadCreate) -> DownloadCreated:
    result = await services.post_downloads_service(
        youtube_link=download.youtube_link,
        trim_start=download.trim_start,
        trim_end=download.trim_end,
    )
    return result


@router.get("/downloads/{request_id}")
async def get_download(request_id: UUID) -> DownloadDetail:
    result = await services.get_download_service(request_id=request_id)
    if result is None:  # todo: add exception handler
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Download not found"
        )
    return result
