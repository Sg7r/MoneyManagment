from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
import os


@shared_task
def send_confirmation_email(username, password, email):
    send_mail(
        subject='Registration confirmation',
        message='Here is your registration information',
        # from_email=settings.EMAIL_HOST_USER,
        from_email=os.environ['EMAIL_HOST_USER'],
        recipient_list=[email],
        html_message='{} / {} / {}'.format(
            username, password, email
        )
    )
