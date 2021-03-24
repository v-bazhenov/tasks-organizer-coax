from django.urls import path
from authentication import views


urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
]