from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name="home.html"), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include(('accounts.urls', 'accounts'))),
    path('authentication/', include(('authentication.urls', 'authentication'))),
    path('tasks/', include(('tasks.urls', 'tasks')))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
