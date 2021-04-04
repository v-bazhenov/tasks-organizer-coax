from django.db import models
from django.conf import settings
from django.core.validators import MaxLengthValidator, validate_image_file_extension


class Task(models.Model):
    title = models.CharField(max_length=100, validators=[MaxLengthValidator])
    memo = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True, validators=[validate_image_file_extension])
    created_at = models.DateTimeField(auto_now_add=True)
    date_completed_at = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    reminder = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
