from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from .forms import OrganizerForm, UserRegisterForm
from .models import Organizer


def home(request):
    return render(request, 'home.html')


class SignUpView(CreateView):
  template_name = 'signupuser.html'
  success_url = reverse_lazy('loginuser')
  form_class = UserRegisterForm


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'loginuser.html', {'form': AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttasks')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Organizer
    form_class = OrganizerForm
    template_name = 'createtask.html'
    success_url = reverse_lazy('currenttasks')

    def form_valid(self, form):
        newtask = form.save(commit=False)
        newtask.user = self.request.user
        newtask.save()
        return super(TaskCreateView, self).form_valid(form)


class TasksDetailView(LoginRequiredMixin, ListView):
    queryset = Organizer.objects.filter(datecompleted__isnull=True)
    context_object_name = 'tasks'
    template_name = 'currenttasks.html'


class CompletedTasksView(LoginRequiredMixin, ListView):
    queryset = Organizer.objects.filter(datecompleted__isnull=False).order_by('-datecompleted')
    context_object_name = 'tasks'
    template_name = 'completedtasks.html'


class TaskDetailView(LoginRequiredMixin, DetailView):
    queryset = Organizer.objects.all()
    context_object_name = 'task'
    template_name = 'viewtask.html'

    def post(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Organizer, pk=pk, user=request.user)
        form = OrganizerForm(request.POST, instance=task)
        form.save()
        return redirect('currenttasks')


@login_required
def completetask(request, pk):
    task = get_object_or_404(Organizer, pk=pk, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('currenttasks')


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Organizer
    success_url = reverse_lazy('currenttasks')
