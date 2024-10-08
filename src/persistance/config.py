import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# Database configuration
db = {
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "host": os.getenv("MYSQL_HOST"),
    "database": os.getenv("MYSQL_DATABASE"),
}
