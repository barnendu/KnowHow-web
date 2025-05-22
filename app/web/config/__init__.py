import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SESSION_PERMANENT = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    ACCOUNT_NAME = os.getenv('ACCOUNT_NAME')
    ACCOUNT_KEY = os.getenv('ACCOUNT_KEY')
    CONTAINER_NAME = os.getenv('CONTAINER_NAME')
    CELERY = {
        "broker_url": os.getenv("REDIS_URI", False),
        "task_ignore_result": True,
        "broker_connection_retry_on_startup": False,
    }


