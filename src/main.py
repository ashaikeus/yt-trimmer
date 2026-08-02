from fastapi import FastAPI

from routers import download_router

app = FastAPI()

app.include_router(download_router)
