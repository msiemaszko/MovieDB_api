import os
from dotenv import load_dotenv

load_dotenv()
DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'myappdb')
DB_USER = os.environ.get('DB_USER', 'myappuser')
DB_PASS = os.environ.get('DB_PASS', '1qaz2wsx')

DB_TYPE = os.environ.get('DB_TYPE', 'sqlite')
# DB_TYPE = "sqlite"
# DB_TYPE = "postgres"
