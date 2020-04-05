import os
from dotenv import load_dotenv

load_dotenv()

SERVER_NAME = os.getenv('SERVER_NAME')
BASE_URL = os.getenv('BASE_URL')

API_PREFIX = '{}{}'.format(SERVER_NAME, BASE_URL)

DATABASE_URL = os.getenv('DATABASE_URL')

TEST_DB = os.getenv('TEST_DB')