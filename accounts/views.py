from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, DetailView
from django.urls import reverse_lazy

from accounts.models import Profile
from accounts.forms import ProfileForm


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    fields = ['name', 'avatar', 'age', 'phone', 'profession']
    template_name = 'accounts/profile_detail.html'

    def get_object(self):
        try:
            return self.request.user.profile
        except Profile.DoesNotExist:
            raise Exception(
                "User doesn't have an associated profile")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('home')