from django.urls import path
from accounts import views

urlpatterns = [

    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/<int:pk>/update/', views.ProfileUpdateView.as_view(), name='profile_update')
]