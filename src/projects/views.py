from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from projects.models import Project


class ProjectListView(ListView):
    model = Project


class ProjectDetailView(DetailView):
    model = Project

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user not in self.object.facilitators.all():
            messages.error(request, "You are not the facilitator for this project!")
            return redirect('/')
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)