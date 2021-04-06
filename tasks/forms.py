from django import forms
from django.forms import ModelForm

from tasks.models import Task


class TaskForm(ModelForm):

    remind_at = forms.DateTimeField(required=False,
                                   widget=forms.TextInput(
                                    attrs={'type': 'datetime-local'}
                                   ))

    class Meta:
        model = Task
        fields = ['title', 'memo', 'image', 'important', 'remind_at']
