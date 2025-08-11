import os
from celery import Celery
broker = os.getenv("CELERY_BROKER_URL") or os.getenv("REDIS_URL")
backend = os.getenv("CELERY_RESULT_BACKEND") or os.getenv("REDIS_URL")
celery = Celery("autodocs", broker=broker, backend=backend, include=["apps.worker.tasks"])
