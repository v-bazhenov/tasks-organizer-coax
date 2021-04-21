import os
import datetime
import pytz
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tasks_organizer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.contrib.auth import get_user_model
from django.test import TestCase
from mixer.backend.django import mixer

from tasks.models import Task
from tasks.forms import TaskForm

User = get_user_model()


class TestTaskForms(TestCase):
	def setUp(self):
		self.user = mixer.blend(User, username='jack', email='a@gmail.com', password='12345678aa')
		self.task = mixer.blend(Task,
								user=self.user, 
								title='example', 
								memo='example', 
								image='images/user.png', 
								is_important=False, 
								remind_at=datetime.datetime(2021, 4, 18, 14, tzinfo=pytz.UTC))

	def test_taskform_valid(self):
		form = TaskForm(data={'title': 'example', 
							'memo': 'example', 
							'image': 'images/user.png', 
							'is_important': False, 
							'remind_at': datetime.datetime(2021, 4, 18, 14, tzinfo=pytz.UTC)})
		self.assertTrue(form.is_valid())
