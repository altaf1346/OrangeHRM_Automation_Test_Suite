import json
import csv
import os
from utils.logger import logger


class DataReader:
    """
    Utility class to read test data from various file formats
    """

    @staticmethod
    def read_json(file_path):
        """
        Read data from a JSON file

        :param file_path: Path to the JSON file
        :return: Dictionary containing the JSON data
        """
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            logger.error(f"Error reading JSON file {file_path}: {e}")
            return None

    @staticmethod
    def read_csv(file_path):
        """
        Read data from a CSV file

        :param file_path: Path to the CSV file
        :return: List of dictionaries containing the CSV data
        """
        try:
            data_list = []
            with open(file_path, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    data_list.append(row)
            return data_list
        except Exception as e:
            logger.error(f"Error reading CSV file {file_path}: {e}")
            return None

    @staticmethod
    def get_test_data_path(file_name):
        """
        Get absolute path to a test data file

        :param file_name: Name of the file
        :return: Absolute path to the file
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, "data", file_name)

    @staticmethod
    def get_login_credentials():
        """
        Get login credentials from the CSV file

        :return: List of dictionaries containing username and password
        """
        file_path = DataReader.get_test_data_path("login_credentials.csv")
        return DataReader.read_csv(file_path)

    @staticmethod
    def get_user_data():
        """
        Get user data from the JSON file

        :return: Dictionary containing user data
        """
        file_path = DataReader.get_test_data_path("users.json")
        return DataReader.read_json(file_path)