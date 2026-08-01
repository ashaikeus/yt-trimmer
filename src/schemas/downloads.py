from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, HttpUrl

from enums import DownloadStatus


class DownloadCreate(BaseModel):
    youtube_link: HttpUrl
    trim_start: int | None
    trim_end: int | None


class DownloadCreated(BaseModel):
    request_id: UUID
    created_at: datetime
    status: DownloadStatus


class DownloadDetail(DownloadCreate, DownloadCreated):
    completed_at: datetime | None
    file_link: HttpUrl | None
