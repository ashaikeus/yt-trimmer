from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, HttpUrl

from enums import DownloadStatus


class DownloadCreate(BaseModel):
    youtube_link: HttpUrl
    trim_start: int | None
    trim_end: int | None


class DownloadCreated(BaseModel):
    request_id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: DownloadStatus = DownloadStatus.QUEUED


class DownloadDetail(DownloadCreate, DownloadCreated):
    completed_at: datetime | None = None
    file_link: HttpUrl | None = None
