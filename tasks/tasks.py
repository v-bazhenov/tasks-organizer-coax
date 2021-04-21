from celery import shared_task
from django.core.mail import EmailMultiAlternatives

import logging

logger = logging.getLogger('celery')


@shared_task()
def send_html_mail(subject: str, text_content: str, html_content: str, from_email: str, to_mail:str) -> None:
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_mail)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
