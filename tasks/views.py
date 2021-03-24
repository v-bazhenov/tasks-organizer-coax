from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.utils import timezone

from tasks.forms import TaskForm
from tasks.models import Task


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'createtask.html'
    success_url = reverse_lazy('tasks:currenttasks')

    def form_valid(self, form):
        newtask = form.save(commit=False)
        newtask.user = self.request.user
        newtask.save()
        return super(TaskCreateView, self).form_valid(form)


class TasksDetailView(LoginRequiredMixin, ListView):
    queryset = Task.objects.filter(date_completed__isnull=True)
    context_object_name = 'tasks'
    template_name = 'currenttasks.html'
    paginate_by = 5


class CompletedTasksView(LoginRequiredMixin, ListView):
    queryset = Task.objects.filter(date_completed__isnull=False).order_by('-date_completed')
    context_object_name = 'tasks'
    template_name = 'completedtasks.html'
    paginate_by = 5


class TaskDetailView(LoginRequiredMixin, DetailView):
    queryset = Task.objects.all()
    context_object_name = 'task'
    template_name = 'viewtask.html'

    def post(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        form = TaskForm(request.POST, instance=task)
        form.save()
        return redirect('tasks:currenttasks')


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    login_url = '/authentication/login/'
    model = Task
    success_url = reverse_lazy('tasks:currenttasks')


@login_required
def completetask(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.date_completed = timezone.now()
        task.save()
        return redirect('tasks:currenttasks')
