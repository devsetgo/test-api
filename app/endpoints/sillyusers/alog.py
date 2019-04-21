from datetime import datetime
from loguru import logger

logger.debug("That's it, beautiful and simple logging!")
logger.add(
    "file_1.log", rotation="100 MB", retention="14 days", enqueue=True
)  # Automatically rotate too big file and dispose after 14 days
