from django.contrib.auth import models
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView

from profiles.models import Preferences


class ProfileDetailView(DetailView):
    model = models.User
    template_name = 'profiles/profile_detail.html'


@method_decorator(login_required, name='dispatch')
class PreferencesUpdateView(UpdateView):
    model = Preferences
    fields = ['timezone']
    success_url = reverse_lazy('projects:project-list')

    def get_object(self, queryset=None):
        obj, created = Preferences.objects.get_or_create(user=self.request.user)
        return obj

    def form_valid(self, form):
        form.instance.user = self.request.user
        
        return super(PreferencesUpdateView, self).form_valid(form)