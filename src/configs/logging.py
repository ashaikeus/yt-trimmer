import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("yt-trimmer")


class YDLLogger:
    def debug(self, msg):
        logger.debug(msg)

    def warning(self, msg):
        logger.debug(msg)

    def error(self, msg):
        logger.debug(msg)


YDL_LOGGING_OPTIONS = {"logger": YDLLogger()}
