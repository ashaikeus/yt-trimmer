from pathlib import Path

from configs import logger, redis_client, settings


def clean_expired_files() -> None:
    active_file_addresses = {
        Path(redis_client.hget(key, "file_link"))
        for key in list(redis_client.keys("download:*"))
        if redis_client.hget(key, "file_link") != None
    }
    current_dir_contents = list(settings.resolved_download_dir.iterdir())
    destroyed: int = 0
    for current_file in current_dir_contents:
        if current_file not in active_file_addresses:
            destroyed += 1
            current_file.unlink()
    logger.info(f"Cleanup task done! Removed {destroyed} files")
