from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.conf import settings

from authentication.forms import UserRegisterForm
from tasks.tasks import send_html_mail

import logging

logger = logging.getLogger('django')


class SignUpView(SuccessMessageMixin, CreateView):
    """Register new user and send congratulation email"""
    template_name = 'signupuser.html'
    success_url = reverse_lazy('authentication:loginuser')
    form_class = UserRegisterForm
    success_message = 'You have been successfully signed up!'

    def form_valid(self, form):
        subject = 'You have been successfully signed up!'
        context = {'username': form.instance.username}
        form.save()
        send_html_mail.delay(subject=subject, 
                            html_content=render_to_string('email/signup_email.html', context=context),
                            text_content = render_to_string('email/signup_email.txt', context=context),
                            from_email=settings.EMAIL_HOST_USER,
                            to_mail=[form.instance.email])
        return super().form_valid(form)


class LoginViewCustom(SuccessMessageMixin, LoginView):
    """Login registered user"""
    template_name = "registration/login.html"
    success_message = 'You have been successfully logged in!'
