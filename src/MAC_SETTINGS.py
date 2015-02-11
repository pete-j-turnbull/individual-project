DEBUG = True

MONGO_IP = None
MONGO_PORT = None
BLOOM_DIR = '/Users/pete/Development/individual_project/storage/bloomfilters'

LOG_DIR = '/Users/pete/Development/individual_project/storage/logs'

FAKE_DATABASE = '/Users/pete/Development/individual_project/storage/database.db'


# CELERY and rabbitmq BROKER settings
BROKER_URL = "amqp://guest:guest@127.0.0.1:5672//"
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS=("tasks",)