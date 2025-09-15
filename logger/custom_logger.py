import logging
from datetime import datetime
import os

class CustomLogger:
    def __init__(self, log_dir="logs"):
        # Create logs directory if it doesn't exist
        self.logs_dir = os.path.join(os.getcwd(), log_dir)
        os.makedirs(self.logs_dir, exist_ok=True)

        # Create a log file with the current timestamp
        log_file = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
        log_file_path = os.path.join(self.logs_dir, log_file)

        # Configure logging
        logging.basicConfig(
            filename=log_file_path,
            level=logging.INFO,
            format='[%(asctime)s] %(levelname)s %(name)s (line:%(lineno)d) - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        )

    def get_logger(self, name=__file__):
        return logging.getLogger(os.path.basename(name))

if __name__ == "__main__":
    custom_logger = CustomLogger()
    logger = custom_logger.get_logger(__file__)
    logger.info("Testing logger class.")