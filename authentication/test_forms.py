import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tasks_organizer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

from authentication.forms import UserRegisterForm
from django.contrib.auth import get_user_model
User = get_user_model()


class TestRegisterForm(TestCase):
	
	def test_user_singup(self):
		response = self.client.post(reverse("authentication:signupuser"))
		self.assertEqual(response.status_code, HTTPStatus.OK)

	# def setUp(self):
	# 	self.user = User.objects.create_user(username='testclient', email='sponge@gmail.com')

	# def test_user_already_exists(self):
	# 	data = {
	# 		'username': 'testclient',
	# 		'email': 'sponge@gmail.com'
	# 		}
	# 	form = UserRegisterForm(data)
	# 	print(form)
	# 	self.assertTrue(form.is_valid())
