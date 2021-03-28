from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model()

user = User.objects.last()


@shared_task()
def send_email():
	send_mail(
		'You have been successfully signed up!',
		'Welcome to Task Organizer',
		[settings.EMAIL_HOST_USER],
		[user.email])