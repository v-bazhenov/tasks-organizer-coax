from django.contrib import admin
from django.urls import path, include
from tasks import views


urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('users/', include(('users.urls', 'users'))),
    path('tasks/', include(('tasks.urls', 'tasks')))
]