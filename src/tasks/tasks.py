from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from configs import YDL_LOGGING_OPTIONS, logger, redis_client
from enums import DownloadStatus
from schemas import DownloadDetail


def background_download(download_data: dict) -> None:
    download = DownloadDetail(**download_data)
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
