import pytz
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tasks_organizer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.contrib.auth import get_user_model
from django.test import TestCase
from mixer.backend.django import mixer

from accounts.forms import ProfileForm

User = get_user_model()


class TestProfileForm(TestCase):
	def setUp(self):
		self.user = mixer.blend(User, username='jack', email='a@gmail.com', password='12345678aa')

	def test_profileform_valid(self):
		form = ProfileForm(data={'name': None, 'age': 18, 'phone': None, 'profession': None, 'avatar': ''})
		self.assertTrue(form.is_valid())