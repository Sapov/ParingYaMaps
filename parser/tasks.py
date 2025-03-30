from celery import shared_task

from .core.maps import Parse


@shared_task
def run_parser(organisation:str, location:str):
    Parse(organisation, location).run()
