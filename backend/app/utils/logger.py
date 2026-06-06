import structlog
import logging
import sys
from app.config import get_settings

settings = get_settings()

logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=getattr(logging, settings.log_level),
)

logger = structlog.get_logger()