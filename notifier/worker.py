import requests
from celery import Celery

from db.pool import MAIN_URL, REDIS_URL

celery_app = Celery('worker', backend=REDIS_URL, broker=REDIS_URL)


@celery_app.task()
def send_later(client_id, message, send_date):
    """Send message to user by /delay endpoint."""
    data = {'client_id': client_id, 'message': message, 'date': send_date}
    requests.post(MAIN_URL, json=data)
