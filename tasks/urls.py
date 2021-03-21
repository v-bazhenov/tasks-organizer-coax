from django.urls import path
from tasks import views


urlpatterns = [
    path('create/', views.TaskCreateView.as_view(), name='createtask'),
    path('current/', views.TasksDetailView.as_view(), name='currenttasks'),
    path('completed/', views.CompletedTasksView.as_view(), name='completedtasks'),
    path('task/<int:pk>', views.TaskDetailView.as_view(), name='viewtask'),
    path('task/<int:pk>/complete/', views.completetask, name='completetask'),
    path('task/<int:pk>/delete', views.DeleteTaskView.as_view(), name='deletetask'),
]
