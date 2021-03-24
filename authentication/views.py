from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from authentication.forms import UserRegisterForm


class SignUpView(CreateView):
    template_name = 'signupuser.html'
    success_url = reverse_lazy('authentication:loginuser')
    form_class = UserRegisterForm


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'loginuser.html', {'form': AuthenticationForm(),
                                                      'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('tasks:currenttasks')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
