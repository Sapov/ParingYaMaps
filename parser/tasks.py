from celery import shared_task

from .core.maps import Parse


@shared_task
def run_parser(category:str, location:str, order_id):
    Parse(category, location, order_id).run()
