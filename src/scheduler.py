from datetime import datetime

from rq_scheduler import Scheduler

from configs import redis_client, settings
from tasks.cleanup import clean_expired_files


def start_scheduler():
    scheduler = Scheduler(connection=redis_client)

    scheduler.schedule(
        scheduled_time=datetime.now(),
        func=clean_expired_files,
        interval=settings.cleanup_interval,
    )


if __name__ == "__main__":
    start_scheduler()
