import logging
from datetime import datetime
import os

def get_logger(name, args):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logger = logging.getLogger('my_logger')

    logger.setLevel(logging.DEBUG)

    os.makedirs('log',exist_ok=True)
    if 'beamsearch' not in name:
        os.makedirs(f'log/induction',exist_ok=True)
        file_handler = logging.FileHandler(f'log/induction/{name}_{current_time}.log')
    else:
        os.makedirs(f'log/transduction',exist_ok=True)
        file_handler = logging.FileHandler(f'log/transduction/{name}_{current_time}.log')
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    for arg, value in vars(args).items():
        logger.info(f"{arg}: {value}")
    return logger
