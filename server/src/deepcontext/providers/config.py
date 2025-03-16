import os
from dotenv import load_dotenv

class ConfigProvider:
    def load_config():
        try:
            print("Loading ENV Variables...")
            load_dotenv("server/config/.env.development")
            print("ENV Variables Loaded")
        except Exception as e:
            raise e
    
    def get(key):
        try:
            if key not in os.environ:
                raise Exception(f"ENV Variable {key} does not exist")
            return os.environ[key]
        except Exception as e:
            raise e