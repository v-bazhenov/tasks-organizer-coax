import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tasks_organizer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.contrib.auth import get_user_model
from django.test import TestCase
from mixer.backend.django import mixer

from accounts.models import Profile

User = get_user_model()


class TestProfileCreation(TestCase):
	def setUp(self):
		self.user = mixer.blend(User, username='Jack', email='example@gmail.com')
	 	#self.profile = Profile.objects.create(user=self.user, name='a', phone='+15123321144', profession='driver')

	def test_name(self):
		name = Profile.objects.get(name=None)
		self.assertEqual(name.name, None)

	def test_avatar(self):
		avatar = Profile.objects.get(avatar='')
		self.assertEqual(avatar.avatar, '')

	def test_age(self):
		age = Profile.objects.get(age=18)
		self.assertEqual(age.age, 18)

	def test_phone(self):
		phone = Profile.objects.get(phone=None)
		self.assertEqual(phone.phone, None)

	def test_profession(self):
		profession = Profile.objects.get(profession=None)
		self.assertEqual(profession.profession, None)