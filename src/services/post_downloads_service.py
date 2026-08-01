from datetime import datetime, timezone
from uuid import uuid4

from enums import DownloadStatus


async def post_downloads_service(
    youtube_link: str,  # todo: validation
    trim_start: int | None,
    trim_end: int | None,
) -> dict:
    # todo: For now I mock the response -- we'll focus on queueing logic later
    return {
        "request_id": uuid4(),
        "created_at": datetime.now(timezone.utc),
        "status": DownloadStatus.QUEUED,
    }
