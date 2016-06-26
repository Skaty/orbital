from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from projects.models import Project

@method_decorator(login_required, name='dispatch')
class ProjectListView(ListView):
    model = Project

@method_decorator(login_required, name='dispatch')
class ProjectDetailView(DetailView):
    model = Project

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user not in self.object.facilitators.all():
            messages.error(request, "You are not the facilitator for this project!")
            return redirect('/')
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)