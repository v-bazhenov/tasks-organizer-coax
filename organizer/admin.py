from django.contrib import admin

from .models import Organizer


class OrganizerAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


admin.site.register(Organizer, OrganizerAdmin)
