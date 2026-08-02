import asyncio

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from configs import YDL_LOGGING_OPTIONS, logger, redis_client
from enums import DownloadStatus
from schemas import DownloadDetail


async def post_downloads_service(
    youtube_link: str,  # todo: validation
    trim_start: int | None,
    trim_end: int | None,
) -> DownloadDetail:
    download = DownloadDetail(
        youtube_link=youtube_link,
        trim_start=trim_start,
        trim_end=trim_end,
    )

    redis_client.hset(
        f"download:{download.request_id}",
        mapping=download.model_dump(mode="json", exclude_none=True),
    )
    logger.debug(f"[{download.request_id}]: task saved to Redis")

    asyncio.create_task(
        asyncio.to_thread(background_download, download)
    )  # todo: redis queue
    logger.info(f"[{download.request_id}]: task scheduled")

    return download


def background_download(download: DownloadDetail) -> None:
    try:
        with YoutubeDL(YDL_LOGGING_OPTIONS) as ydl:
            ydl.download(str(download.youtube_link))
        redis_client.hset(
            f"download:{download.request_id}", "status", DownloadStatus.COMPLETED.value
        )  # todo: create repository
        logger.info(f"[{download.request_id}]: file downloaded")
    except DownloadError as exc:
        redis_client.hset(
            f"download:{download.request_id}", "status", DownloadStatus.FAILED.value
        )
        logger.exception(f"[{download.request_id}]: download failed - {exc}")
