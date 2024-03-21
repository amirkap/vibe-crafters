import logging


# Configure logging to write to a file
logging.basicConfig(
    filename='VibeCreatorsExceptions.log',
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)