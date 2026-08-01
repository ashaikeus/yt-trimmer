# Goal for today: save YouTube video from a provided link

# API:
# - POST /downloads
#   send a downloading request
#   BODY PARAMS:
#   * youtube_link
#   - start_trim
#   - end_trim
# - GET /downloads/{request_id}
#   poll for status, returns download link
# - GET /files/{file_id}
#   the downloading endpoint when the request completes successfully


from fastapi import FastAPI

from routers import download_router

app = FastAPI()

app.include_router(download_router)
