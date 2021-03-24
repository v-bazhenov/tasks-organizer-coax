from django.contrib import admin
from authentication.models import User


class UsersAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UsersAdmin)