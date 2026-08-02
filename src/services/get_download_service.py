from uuid import UUID

from configs import redis_client
from schemas import DownloadDetail


async def get_download_service(request_id: UUID) -> DownloadDetail | None:
    download = redis_client.hgetall(
        name=f"download:{request_id}"
    )  # todo: isolate it into a helper, i just spent three minutes debugging only to realize i misremembered the name
    return download or None
