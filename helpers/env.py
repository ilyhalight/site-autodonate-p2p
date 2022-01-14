import os
from dotenv import load_dotenv

env_name = '.env'
dotenv_path = os.path.join(os.path.dirname(__file__), '../', env_name)

def get_env():
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)