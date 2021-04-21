from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.template.loader import render_to_string

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.utils import timezone

from tasks.forms import TaskForm
from tasks.models import Task
from tasks.tasks import send_html_mail

import logging

logger = logging.getLogger('django')


class TaskCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """Create new task and send email reminder if this option was chosen"""
    model = Task
    form_class = TaskForm
    template_name = 'createtask.html'
    success_url = reverse_lazy('tasks:currenttasks')
    success_message = 'The task has been successfully created!'

    def form_valid(self, form):
        newtask = form.save(commit=False)
        newtask.user = self.request.user
        form.save()
        remind_at = form.instance.remind_at
        subject = 'Task Reminder'
        context = {'task_name': form.instance.title,
                    'task_memo': form.instance.memo,
                    'task_is_important': form.instance.is_important}
        if remind_at is not None:
            send_html_mail.apply_async((subject,
                                        render_to_string('email/task_reminder.txt', context=context),
                                        render_to_string('email/task_reminder.html', context=context),
                                        settings.EMAIL_HOST_USER,
                                        [self.request.user.email]), 
                                        eta=remind_at)
        return super(TaskCreateView, self).form_valid(form)



class TasksDetailView(LoginRequiredMixin, ListView):
    """View all created task"""
    queryset = Task.objects.filter(date_completed_at__isnull=True).order_by('-created_at')
    context_object_name = 'tasks'
    template_name = 'currenttasks.html'
    paginate_by = 5


class CompletedTasksView(LoginRequiredMixin, ListView):
    """View completed task"""
    queryset = Task.objects.filter(date_completed_at__isnull=False).order_by('-date_completed_at')
    context_object_name = 'tasks'
    template_name = 'completedtasks.html'
    paginate_by = 5


class TaskDetailView(LoginRequiredMixin, DetailView):
    """View specific task"""
    queryset = Task.objects.all()
    context_object_name = 'task'
    template_name = 'viewtask.html'


class TaskUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """Update existing task"""
    model = Task
    template_name = 'updatetask.html'
    success_url = reverse_lazy('tasks:currenttasks')
    success_message = 'The task has been successfully edited!'
    fields = ('title', 'memo', 'image', 'is_important')


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    """Delete existing task"""
    login_url = '/authentication/login/'
    model = Task
    success_url = reverse_lazy('tasks:currenttasks')
    success_message = 'The task has been successfully deleted!'

    def delete(self, request: HttpRequest, *args, **kwargs) -> None:
        messages.success(self.request, self.success_message)
        return super(DeleteTaskView, self).delete(request, *args, **kwargs)


@login_required
def completetask(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    """Complete existing task"""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.date_completed_at = timezone.now()
        task.save()
        return redirect('tasks:currenttasks')
