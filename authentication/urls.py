from django.contrib.auth.views import LogoutView
from django.urls import path

from authentication.views import SignUpView, LoginViewCustom


urlpatterns = [

    path('signup/', SignUpView.as_view(), name='signupuser'),
    path('login/', LoginViewCustom.as_view(), name='loginuser'),
    path('logout/', LogoutView.as_view(), name='logoutuser'),
]