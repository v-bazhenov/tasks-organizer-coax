from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from authentication.forms import UserRegisterForm
from tasks.tasks import send_email


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'signupuser.html'
    success_url = reverse_lazy('authentication:loginuser')
    form_class = UserRegisterForm
    success_message = 'You have been successfully signed up!'

    def form_valid(self, form):
        form.save()
        send_email.delay()
        return super().form_valid(form)


class LoginViewCustom(SuccessMessageMixin, LoginView):
    template_name = "registration/login.html"
    success_message = 'You have been successfully logged in!'
