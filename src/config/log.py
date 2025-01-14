import logging
import os
log_file = 'app.log'

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(log_file)),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("link_usage_logger")
