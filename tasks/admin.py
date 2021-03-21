from django.contrib import admin

from .models import Task


class TasksAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


admin.site.register(Task, TasksAdmin)
