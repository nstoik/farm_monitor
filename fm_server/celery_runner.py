""" main celery module """
from celery import Celery, signals


app = Celery()

app.config_from_object('fm_server.settings:CeleryConfig')

# @signals.setup_logging.connect
def setup_celery_logging(sender, **kwargs):
    for key in kwargs:
        print("keyword arg: %s: %s" % (key, kwargs[key]))
