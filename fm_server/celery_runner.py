""" main celery module """
from celery import Celery

app = Celery('fm_server_celery',
             broker='amqp://fm:farm_monitor@localhost/farm_monitor',
             backend='rpc://',
             include=['fm_server.device.tasks'])
