from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from configs import YDL_SETTINGS, logger, redis_client, settings
from enums import DownloadStatus
from schemas import DownloadDetail
from utils import trim_video, upload_file_azure


def background_download(download_data: dict) -> None:
    download = DownloadDetail(**download_data)
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
                ):  # todo: pydantic check that it's bigger than 0
                    local_path = trim_video(
                        input_path=local_path,
                        trim_start=download.trim_start,
                        trim_end=download.trim_end,
                    )
                else:
                    raise Exception(
                        "Invalid trim start/end values"
                    )  # todo: throw custom exception, another todo: return it to the user

            redis_client.hset(
                f"download:{download.request_id}", "file_link", local_path
            )  # todo: decompose it into a redis_helpers file too

            if settings.blob_enabled:
                blob_link = upload_file_azure(
                    local_path=local_path, request_id=str(download.request_id)
                )
                redis_client.hset(
                    f"download:{download.request_id}", "file_link", blob_link
                )

        redis_client.hset(
            f"download:{download.request_id}", "status", DownloadStatus.COMPLETED.value
        )  # todo: create repository
        logger.info(f"[{download.request_id}]: file downloaded")
    except DownloadError as exc:
        redis_client.hset(
            f"download:{download.request_id}", "status", DownloadStatus.FAILED.value
        )
        logger.exception(f"[{download.request_id}]: download failed - {exc}")
