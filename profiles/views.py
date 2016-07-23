from django.contrib.auth import models
from django.views.generic import DetailView


class ProfileDetailView(DetailView):
    model = models.User
    template_name = 'profiles/profile_detail.html'