# POST /downloads - send a downloading request
# Body params:
# * youtube_link
# - start_trim
# - end_trim

from fastapi import APIRouter

router = APIRouter()
