import os
import datetime
import pytz
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tasks_organizer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer

from tasks.models import Task

User = get_user_model()


class TestTasksViews(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='jack', email='a@gmail.com', password='12345678aa')
		self.client.login(email='a@gmail.com', password='12345678aa')
		self.task = mixer.blend(Task, user=self.user, title='exa')
		

	def test_task_creation(self):
		response = self.client.post(reverse("tasks:createtask"), 
											{'title': 'example', 
											'memo': 'example',
											'image': '/image/user.png',
											'remind_at': datetime.datetime(2021, 4, 18, 14, tzinfo=pytz.UTC),
											'is_important': False})
		self.assertEqual(response.status_code, HTTPStatus.FOUND)

	def test_task_view(self):
		response = self.client.get(reverse("tasks:currenttasks"))

		self.assertEqual(response.status_code, HTTPStatus.OK)

	def test_completedtasks_view(self):
		response = self.client.get(reverse("tasks:completedtasks"))
		self.assertEqual(response.status_code, HTTPStatus.OK)

	def test_task_detailview(self):
		response = self.client.get(reverse("tasks:viewtask", kwargs={'pk': self.task.id}))
		self.assertEqual(response.status_code, HTTPStatus.OK)

	def test_updatetask(self):
		response = self.client.post(reverse("tasks:updatetask", kwargs={'pk': self.task.id}), 
											{'title': 'update', 
											'memo': 'update',
											'image': '/image/logo.png',
											'remind_at': datetime.datetime(2021, 4, 18, 13, tzinfo=pytz.UTC),
											'is_important': True})
		self.assertEqual(response.status_code, HTTPStatus.FOUND)

	def test_task_delete(self):
		response = self.client.post(reverse("tasks:deletetask", kwargs={'pk': self.task.id}))
		self.assertEqual(response.status_code, HTTPStatus.FOUND)

	def test_task_complete(self):
		response = self.client.post(reverse("tasks:completetask", kwargs={'pk': self.task.id}))
		self.assertEqual(response.status_code, HTTPStatus.FOUND)


