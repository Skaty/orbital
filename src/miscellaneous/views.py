from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.views.generic.base import TemplateView

from miscellaneous.forms import RegistrationForm


class HomepageView(TemplateView):
    template_name = 'miscellaneous/index.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('projects:project-list')
        
        return super(HomepageView, self).get(request, *args, **kwargs)

class RegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'miscellaneous/registration_form.html'
    success_url = reverse_lazy('projects:project-list')

    def form_valid(self, form):
        self.object = User.objects.create_user(form.instance.username, form.instance.email, form.instance.password,
                                               first_name=form.instance.first_name, last_name=form.instance.last_name)

        return HttpResponseRedirect(self.get_success_url())