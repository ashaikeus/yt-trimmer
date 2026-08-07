from datetime import datetime, timezone

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from configs import YDL_SETTINGS, logger, redis_client, settings
from enums import DownloadStatus
from schemas import DownloadDetail
from utils import trim_video, upload_file_azure


def background_download(download_data: dict) -> None:
    download = DownloadDetail(**download_data)
    key = f"download:{download.request_id}"
    try:
        with YoutubeDL(YDL_SETTINGS) as ydl:  # todo: isolate download
            file_info = ydl.extract_info(
                str(download.youtube_link),
                download=True,
            )
            local_path = ydl.prepare_filename(file_info)[1:]

            if download.trim_start is not None and download.trim_end is not None:
                duration = file_info["duration"]
                if (0 <= download.trim_start < duration) and (
                    0 < download.trim_end <= duration
                ):  # todo: add pydantic check that it's bigger than 0
                    local_path = trim_video(
                        input_path=local_path,
                        trim_start=download.trim_start,
                        trim_end=download.trim_end,
                    )
                else:
                    raise Exception(
                        "Invalid trim start/end values"
                    )  # todo: throw custom exception, another todo: return it to the user

            download.file_link = local_path

            if settings.blob_enabled:
                blob_link = upload_file_azure(
                    local_path=local_path, request_id=str(download.request_id)
                )
                redis_client.hset(key, "file_link", blob_link)

        download.status = DownloadStatus.COMPLETED
        download.completed_at = datetime.now(timezone.utc)
        redis_client.hset(key, mapping=download.model_dump(mode="json"))
        redis_client.expire(key, settings.file_ttl)

        logger.info(f"[{download.request_id}]: file downloaded")
    except DownloadError as exc:
        redis_client.hset(key, "status", DownloadStatus.FAILED.value)
        logger.exception(f"[{download.request_id}]: download failed - {exc}")
