from pathlib import Path

from configs import logger, settings


class YDLLogger:
    def debug(self, msg):
        logger.debug(msg)

    def warning(self, msg):
        logger.debug(msg)

    def error(self, msg):
        logger.debug(msg)


resolved_download_dir = Path(settings.download_dir).resolve()

YDL_SETTINGS = {
    "logger": YDLLogger(),
    "outtmpl": f"/{resolved_download_dir}/%(id)s.%(ext)s",
    "format": "mp4",
}
