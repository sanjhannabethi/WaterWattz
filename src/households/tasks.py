from celery import shared_task
from django.core.management import call_command

@shared_task
def generate_user_data():
    call_command('generate_data')