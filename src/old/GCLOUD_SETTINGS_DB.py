MONGO_IP = '10.240.113.54'
MONGO_PORT = '27017'
BLOOM_DIR = '/home/pete/Development/individual_project/storage/bloomfilters_debug'

LOG_DIR = '/home/pete/Development/individual_project/storage/logs_debug'


# CELERY and rabbitmq BROKER settings
BROKER_URL = "amqp://guest:guest@192.158.28.85:5672//"
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS=("tasks",)