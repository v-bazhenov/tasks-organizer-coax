from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models.signals import post_save
from phonenumber_field.modelfields import PhoneNumberField

from accounts.utils import validate_max_age

User = get_user_model()


class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
	avatar = models.ImageField(upload_to='images/', blank=True, null=True)
	age = models.PositiveSmallIntegerField(verbose_name='age', default=18, blank=True, null=True, validators=[validate_max_age])
	name = models.CharField(max_length=150, blank=True, null=True)
	phone = PhoneNumberField(blank=True, null=True)
	profession = models.CharField(max_length=150, blank=True, null=True)

	class Meta:
		verbose_name = 'Profile'
		verbose_name_plural = 'Profiles'
		app_label = 'accounts'

	def __str__(self):
		return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
	if created:
		profile = Profile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)