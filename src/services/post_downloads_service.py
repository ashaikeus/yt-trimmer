import asyncio
from datetime import datetime, timezone
from uuid import UUID, uuid4

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from configs import YDL_LOGGING_OPTIONS, logger
from enums import DownloadStatus


async def post_downloads_service(
    youtube_link: str,  # todo: validation
    trim_start: int | None,
    trim_end: int | None,
) -> dict:
    request_id = uuid4()
    asyncio.create_task(
        asyncio.to_thread(background_download, str(youtube_link), request_id)
    )
    # todo: For now I mock the response -- we'll focus on queueing logic later
    logger.info(f"[{request_id}]: task scheduled")
    status = DownloadStatus.QUEUED
    return {
        "request_id": request_id,
        "created_at": datetime.now(timezone.utc),
        "status": status,
    }


def background_download(youtube_link: str, request_id: UUID) -> None:
    try:
        with YoutubeDL(YDL_LOGGING_OPTIONS) as ydl:
            ydl.download(youtube_link)
        status = DownloadStatus.COMPLETED  # todo: persist status
        logger.info(f"[{request_id}]: file downloaded")
    except DownloadError as exc:
        status = DownloadStatus.FAILED
        logger.exception(f"[{request_id}]: download failed - {exc}")
