import os
from dotenv import load_dotenv
from deepcontext.constants.main import CONFIG_FILE_LOCATION

class ConfigProvider:
    """
    A utility class to load and retrieve environment variables.
    """
    
    @staticmethod
    def load_config():
        """
        Loads environment variables from a .env file.
        """
        try:
            print("Loading ENV Variables...")
            load_dotenv(CONFIG_FILE_LOCATION)  # Load .env file
            print("ENV Variables Loaded")
        except Exception as e:
            raise e
    
    @staticmethod
    def get(key: str) -> str:
        """
        Retrieves the value of an environment variable.
        
        Args:
            key (str): The name of the environment variable.
        
        Returns:
            str: The value of the environment variable.
        
        Raises:
            Exception: If the environment variable does not exist.
        """
        try:
            if key not in os.environ:
                raise Exception(f"ENV Variable {key} does not exist")  # Raise if key not found
            return os.environ[key]  # Return env variable value
        except Exception as e:
            raise e