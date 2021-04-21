import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tasks_organizer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.contrib.auth import get_user_model
from django.test import TestCase
from mixer.backend.django import mixer

User = get_user_model()


class TestUserCreation(TestCase):
	def setUp(self):
		self.user = mixer.blend(User, username='jon', email='example@mail.com')

	def test_user_creation(self):
		username = User.objects.get(username='jon')
		email = User.objects.get(email='example@mail.com')
		self.assertEqual(username.username, 'jon')
		self.assertEqual(email.email, 'example@mail.com')
