from django.contrib import admin

from tasks.models import Task


class TasksAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


admin.site.register(Task, TasksAdmin)
