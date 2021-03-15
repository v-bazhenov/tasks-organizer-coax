from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Organizer


class BootstrapModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class OrganizerForm(ModelForm):
    class Meta:
        model = Organizer
        fields = ['title', 'memo', 'important']


class UserRegisterForm(UserCreationForm, BootstrapModelForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
            super(UserRegisterForm, self).__init__(*args, **kwargs)
            self.fields['username'].widget.attrs.update()
            self.fields['email'].widget.attrs.update()
            self.fields['password1'].widget.attrs.update()
            self.fields['password2'].widget.attrs.update()

    class Meta:
        model = User
        fields = ['username', 'email']

