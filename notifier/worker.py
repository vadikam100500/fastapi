import requests
from celery import Celery

from db import REDIS_URL
from token_handler import create_access_token

celery_app = Celery('worker', backend=REDIS_URL, broker=REDIS_URL)


@celery_app.task()
def send_later(client_id, message, send_date):
    """
    Encode user_id to token and send post request to /reg_confirm endpoint
    (optionaly, by logic we cant change it.)
    """
    token = create_access_token({'client_id': int(client_id)})
    data = {'message': message, 'date': send_date}
    requests.post('http://web:8000/reg_confirm',
                  json=data, params={'token': token})
