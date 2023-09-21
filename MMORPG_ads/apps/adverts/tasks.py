from celery import shared_task
from apps.adverts.utils import send_emails_on_monday


@shared_task
def monday_emailing():
    send_emails_on_monday()
