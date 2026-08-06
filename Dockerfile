FROM python:3.14-slim

WORKDIR /yt-trimmer

COPY pyproject.toml uv.lock ./

RUN pip install uv && uv sync --frozen

RUN apt-get update && apt-get install -y ffmpeg

COPY src ./src

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]