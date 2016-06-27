from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView

from projects.models import Project, ProjectGroup


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


@method_decorator(login_required, name='dispatch')
class ProjectGroupCreateView(CreateView):
    model = ProjectGroup
    fields = ['name', 'members']

    def dispatch(self, request, *args, **kwargs):
        project_pk = self.kwargs.get('project_pk')
        try:
            self.project = Project.objects.get(pk=project_pk)
            if request.user not in self.project.facilitators.all():
                messages.error(request, 'You are not authorised to perform this action!')
                return redirect('/')
        except ObjectDoesNotExist:
            return redirect('/')

        self.success_url = reverse_lazy('projects:project-detail', kwargs={'pk': self.project.pk})

        return super(ProjectGroupCreateView, self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.project = self.project
        return super(ProjectGroupCreateView, self).form_valid(form)