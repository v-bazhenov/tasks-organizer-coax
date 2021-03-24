from django.forms import ModelForm

from tasks.models import Task
from authentication.forms import BootstrapModelForm


class TaskForm(BootstrapModelForm, ModelForm):

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update()
        self.fields['memo'].widget.attrs.update()
        self.fields['image'].widget.attrs.update()

    class Meta:
        model = Task
        fields = ['title', 'memo', 'image']
