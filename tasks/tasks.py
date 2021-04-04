from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task()
def send_email(email, user):
	send_mail(
		'You have been successfully signed up!',
		f'Welcome to Task Organizer, {user}!\nWe hope this handy web tool will help you to organizer your tasks!',
		settings.EMAIL_HOST_USER,
		[email])


@shared_task()
def email_reminder(email, task_name, task_memo):
	send_mail(
		'Do not forget about your task',
		f"We would like to kindly remind you that you have a task to be done on Task Organizer.\nTask name: {task_name}.\nTask memo: {task_memo}.\nPlease don't forget about it!",
		settings.EMAIL_HOST_USER,
		[email])