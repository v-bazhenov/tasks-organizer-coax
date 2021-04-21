import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tasks_organizer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

User = get_user_model()



class TestAuthenticationViews(TestCase):
	def test_user_singup(self):
		response = self.client.post(reverse("authentication:signupuser"),
											{'username': 'Jack', 
											'email': 'a@a.com'})

		self.assertEqual(response.status_code, HTTPStatus.OK)

	def test_user_login(self):
		response = self.client.post(reverse("authentication:loginuser"),
											{'username': 'Jack', 
											'email': 'a@a.com'})

		self.assertEqual(response.status_code, HTTPStatus.OK)

	def test_user_logout(self):
		response = self.client.post(reverse("authentication:logoutuser"),
											{'username': 'Jack', 
											'email': 'a@a.com'})

		self.assertEqual(response.status_code, HTTPStatus.OK)