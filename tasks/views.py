from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.utils import timezone

from tasks.forms import TaskForm
from tasks.models import Task
from tasks.tasks import email_reminder


class TaskCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'createtask.html'
    success_url = reverse_lazy('tasks:currenttasks')
    success_message = 'The task has been successfully created!'

    def form_valid(self, form):
        newtask = form.save(commit=False)
        newtask.user = self.request.user
        newtask.save()
        remind_at = form.instance.remind_at
        if remind_at is not None:
            email = self.request.user.email
            task_name = form.instance.title
            task_memo = form.instance.memo
            email_reminder.apply_async((email, task_name, task_memo), eta=remind_at)
        return super(TaskCreateView, self).form_valid(form)


class TasksDetailView(LoginRequiredMixin, ListView):
    queryset = Task.objects.filter(date_completed_at__isnull=True).order_by('-created_at')
    context_object_name = 'tasks'
    template_name = 'currenttasks.html'
    paginate_by = 5


class CompletedTasksView(LoginRequiredMixin, ListView):
    queryset = Task.objects.filter(date_completed_at__isnull=False).order_by('-date_completed_at')
    context_object_name = 'tasks'
    template_name = 'completedtasks.html'
    paginate_by = 5


class TaskDetailView(LoginRequiredMixin, DetailView):
    queryset = Task.objects.all()
    context_object_name = 'task'
    template_name = 'viewtask.html'


class TaskUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'updatetask.html'
    success_url = reverse_lazy('tasks:currenttasks')
    success_message = 'The task has been successfully edited!'
    fields = ('title', 'memo', 'image', 'important')


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    login_url = '/authentication/login/'
    model = Task
    success_url = reverse_lazy('tasks:currenttasks')
    success_message = 'The task has been successfully deleted!'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteTaskView, self).delete(request, *args, **kwargs)


@login_required
def completetask(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.date_completed_at = timezone.now()
        task.save()
        return redirect('tasks:currenttasks')
