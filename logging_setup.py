import logging
import sys
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def setup_console_logger(name, level):
    handler = logging.StreamHandler(sys.stdout)     
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# first file logger
general_logger = setup_logger('general', 'output.log')
general_logger.info('Program Booting Up')

# second file logger
debug_logger = setup_logger('second_logger', logging.DEBUG)
debug_logger.error('This is an error message')