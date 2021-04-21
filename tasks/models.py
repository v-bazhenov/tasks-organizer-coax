from django.db import models
from django.conf import settings
from django.core.validators import MaxLengthValidator, validate_image_file_extension

from PIL import Image
from tasks.utils import validate_image_size


class Task(models.Model):
    title = models.CharField(max_length=100, validators=[MaxLengthValidator])
    memo = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True, validators=[validate_image_file_extension,
                                                                                      validate_image_size])
    created_at = models.DateTimeField(auto_now_add=True)
    date_completed_at = models.DateTimeField(null=True, blank=True)
    is_important = models.BooleanField(default=False)
    remind_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tasks_task'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        app_label = 'tasks'

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.image.path)

            if img.height > 400 or img.width > 400:
                new_img = (400, 400)
                img.thumbnail(new_img)
                img.save(self.image.path)
        except Exception:
            return
