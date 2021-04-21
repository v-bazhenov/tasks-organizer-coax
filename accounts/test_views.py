from http import HTTPStatus
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tasks_organizer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.contrib.auth import get_user_model
from django.test import TestCase
from mixer.backend.django import mixer
from django.urls import reverse

User = get_user_model()


class TestProfileViews(TestCase):

	def setUp(self):
		self.user = mixer.blend(User, username='jack', email='a@gmail.com', password='12345678aa')
		self.client.login(email='a@gmail.com', password='12345678aa')

	def test_profile_detail(self):
		response = self.client.get(reverse("accounts:profile_detail", kwargs={'pk': self.user.profile.id}))
		self.assertEqual(response.status_code, HTTPStatus.FOUND)

	def test_profile_update(self):
		response = self.client.post(reverse("accounts:profile_update", kwargs={'pk': self.user.profile.id}), 
											{'name': 'Petro', 'age': 20,
											'avatar': '/image/user.png',
											'phone': +15129092213,
											'profession': 'coder'})
		self.assertEqual(response.status_code, HTTPStatus.FOUND)