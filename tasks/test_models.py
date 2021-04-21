import datetime
import os
import pytz
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tasks_organizer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.contrib.auth import get_user_model
from django.test import TestCase
from mixer.backend.django import mixer

from tasks.models import Task

User = get_user_model()


class TestTask(TestCase):

	def setUp(self):
		self.user = mixer.blend(User, username='jon', email='example@mail.com')
		self.task = mixer.blend(Task,
								title='example', 
								memo='example', 
								image='images/user.png',
								is_important=False,
								remind_at=datetime.datetime(2021, 4, 18, 14, tzinfo=pytz.UTC),
								user=self.user)

	def test_title(self):
		title = Task.objects.get(title='example')
		self.assertEqual(title.title, 'example')

	def test_memo(self):
		memo = Task.objects.get(memo='example')
		self.assertEqual(memo.memo, 'example')

	def test_image(self):
		image = Task.objects.get(image='images/user.png')
		self.assertEqual(image.image, 'images/user.png')

	def test_remind_at(self):
		remind_at = Task.objects.get(remind_at=datetime.datetime(2021, 4, 18, 14, tzinfo=pytz.UTC))
		self.assertEqual(remind_at.remind_at, datetime.datetime(2021, 4, 18, 14, tzinfo=pytz.UTC))

	def test_is_important(self):
		is_important = Task.objects.get(is_important=False)
		self.assertEqual(is_important.is_important, False)

	def test_str(self):
		title = Task.objects.get(title='example')
		expected_title = title.title
		self.assertEqual(expected_title, str(title))

