from dotenv import load_dotenv
import os
from os.path import join, dirname
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = join(BASE_DIR, '.env')
load_dotenv(dotenv_path=dotenv_path)

username = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_DATABASE_NAME')
port = os.environ.get('DB_PORT')

# print(f'user: {username}, pwd: {password}, dbname: {db_name}, port: {port}')
print(dotenv_path)