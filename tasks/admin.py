from django.contrib import admin, messages
from django.utils import timezone
from django.utils.translation import ngettext

from tasks.models import Task


class TasksAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_important', 'date_completed_at']
    readonly_fields = ('created_at',)
    ordering = ['-created_at']
    actions = ['mark_important', 'mark_completed', 'mark_not_important', 'mark_not_completed']

    def mark_important(self, request, queryset):
        updated = queryset.update(is_important=True)
        self.message_user(request, ngettext(
            '%d task was successfully marked as important.',
            '%d tasks were successfully marked as important.',
            updated,
        ) % updated, messages.SUCCESS)
    mark_important.short_description = "Mark selected stories as important"

    def mark_not_important(self, request, queryset):
        updated = queryset.update(is_important=False)
        self.message_user(request, ngettext(
            '%d task was successfully marked as not important.',
            '%d tasks were successfully marked as not important.',
            updated,
        ) % updated, messages.SUCCESS)
    mark_not_important.short_description = "Mark selected stories as not important"

    def mark_completed(self, request, queryset):
        updated = queryset.update(date_completed_at=timezone.now())
        self.message_user(request, ngettext(
            '%d task was successfully marked as completed.',
            '%d tasks were successfully marked as completed.',
            updated,
        ) % updated, messages.SUCCESS)
    mark_completed.short_description = "Mark selected stories as completed"

    def mark_not_completed(self, request, queryset):
        updated = queryset.update(date_completed_at=None)
        self.message_user(request, ngettext(
            '%d task was successfully marked as not completed.',
            '%d tasks were successfully marked as not completed.',
            updated,
        ) % updated, messages.SUCCESS)
    mark_not_completed.short_description = "Mark selected stories as not completed"


admin.site.register(Task, TasksAdmin)
