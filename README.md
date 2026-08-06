# yt-trimmer

API for downloading and processing YouTube videos.

## Features:
- Download videos from YouTube
- Trim videos before downloading
- Process downloads asynchronously
- Track download progress by request ID
- Download processed files from Azure Blob Storage (with local Docker mounted volume fallback)
- Automatic expiration of old files

## Stack:
- Python
- FastAPI
- Redis
- Redis Queue (RQ)
- Docker
- Azure Blob Storage
- ffmpeg
- uv

## Installation

1. Install dependencies: 
```
uv sync
```
2. Create an `.env` file, copying the contents of `.env.example`
3. ***Optional**: specify Azure Blob Storage secrets in `.env`*
4. Start the application:
```
docker compose up
```
