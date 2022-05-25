import logging, os

if not os.path.exists('logs'):
    os.mkdir('logs')

logging_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(logging_formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


mongodump_logger = setup_logger('mongodump', 'logs/mongodump.log')

from ._mongodump import MongoDump

