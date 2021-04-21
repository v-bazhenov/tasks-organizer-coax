from django import forms
from django.forms import ModelForm

from tasks.models import Task


class TaskForm(ModelForm):
    """Create form for new task"""
    remind_at = forms.DateTimeField(required=False,
                                   widget=forms.TextInput(
                                    attrs={'type': 'datetime-local'}
                                   ))

    class Meta:
        model = Task
        fields = ['title', 'memo', 'image', 'is_important', 'remind_at']
