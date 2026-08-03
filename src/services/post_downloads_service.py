from configs import logger, queue, redis_client
from schemas import DownloadDetail
from tasks import background_download


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

    queue.enqueue(background_download, download.model_dump(mode="json"))
    logger.info(f"[{download.request_id}]: task scheduled")

    return download
