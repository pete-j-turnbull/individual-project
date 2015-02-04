BROKER_URL = "amqp://guest:guest@192.158.28.85:5672//"
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS=("tasks",)
