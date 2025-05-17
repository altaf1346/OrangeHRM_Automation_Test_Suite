import logging
import os
from datetime import datetime


class Logger:
    """
    Custom logger for test execution
    """

    @staticmethod
    def get_logger(name):
        """
        Configure and return a logger instance

        :param name: Name for the logger
        :return: Configured logger instance
        """
        # Create logs directory if it doesn't exist
        log_dir = "reports/logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Configure logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        # Create file handler
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_handler = logging.FileHandler(f"{log_dir}/test_run_{timestamp}.log")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        # Add handlers to logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger


# Initialize global logger
logger = Logger.get_logger("OrangeHRM_Automation")