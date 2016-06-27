from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView

from miscellaneous.forms import RegistrationForm


class RegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'miscellaneous/registration_form.html'
    success_url = reverse_lazy('projects:project-list')

    def form_valid(self, form):
        self.object = User.objects.create_user(form.instance.username, form.instance.email, form.instance.password,
                                               first_name=form.instance.first_name, last_name=form.instance.last_name)

        return HttpResponseRedirect(self.get_success_url())