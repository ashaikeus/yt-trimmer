# POST /downloads - send a downloading request
# Body params:
# * youtube_link
# - start_trim
# - end_trim

from fastapi import APIRouter

import services
from schemas.downloads import DownloadCreate, DownloadCreated

router = APIRouter()


@router.post("/downloads")
async def post_downloads(download: DownloadCreate) -> DownloadCreated:
    result = await services.post_downloads_service(
        youtube_link=download.youtube_link,
        trim_start=download.trim_start,
        trim_end=download.trim_end,
    )
    return result
