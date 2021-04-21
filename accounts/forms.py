from django.forms import ModelForm

from accounts.models import Profile


class ProfileForm(ModelForm):
    """Create profile form"""

    class Meta:
        model = Profile
        fields = ['name', 'age', 'phone', 'profession', 'avatar']
