MONGO_IP = '146.169.47.50'
MONGO_PORT = '27017'
BLOOM_DIR = '/home/pt1812/individual_project/storage/bloomfilters'

LOG_DIR = '/home/pt1812/individual_project/storage/logs'


# CELERY and rabbitmq BROKER settings
BROKER_URL = "amqp://guest:guest@146.169.46.139:5672//"
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS=("tasks",)