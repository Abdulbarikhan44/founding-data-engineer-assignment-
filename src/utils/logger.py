import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("pipeline_logger")

# logger.setLevel(logging.DEBUG)  # enable later if needed
