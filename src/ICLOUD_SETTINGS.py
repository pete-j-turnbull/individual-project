DEBUG = False

MONGO_IP = '146.169.47.50'
MONGO_PORT = '27017'
BLOOM_DIR = '/home/guest/Development/individual_project/storage/bloomfilters'

LOG_DIR = '/home/guest/Development/individual_project/storage/logs'


# CELERY and rabbitmq BROKER settings
BROKER_URL = "amqp://guest:guest@146.169.47.6:5672//"
#BROKER_URL = "amqp://guest:guest@146.169.46.139:5672//"
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS=("tasks",)
