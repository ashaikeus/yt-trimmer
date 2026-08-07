from .logging_config import logger
from .settings import settings


class YDLLogger:
    def debug(self, msg):
        logger.debug(msg)

    def warning(self, msg):
        logger.debug(msg)

    def error(self, msg):
        logger.debug(msg)


YDL_SETTINGS = {
    "logger": YDLLogger(),
    "outtmpl": f"/{settings.resolved_download_dir}/%(id)s.%(ext)s",
    "format": "mp4",
}
