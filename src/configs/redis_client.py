from redis import Redis
from rq import Queue

from .settings import settings

redis_client = Redis(
    host=settings.redis_host, port=settings.redis_port, decode_responses=True
)
queue = Queue(connection=redis_client)
