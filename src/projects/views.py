from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from projects.models import Project, ProjectGroup


@method_decorator(login_required, name='dispatch')
class ProjectListView(ListView):
    model = Project


@method_decorator(login_required, name='dispatch')
class ProjectCreateView(CreateView):
    model = Project
    fields = ['name', 'facilitators', 'ends_on']
    success_url = reverse_lazy('projects:project-list')

    def get_form(self, form_class=None):
        form = super(ProjectCreateView, self).get_form(form_class)
        form.initial['facilitators'] = [self.request.user]
        return form

    def form_valid(self, form):
        self.object = form.save()
        if self.object.facilitators.filter(pk=self.request.user.pk).count() <= 0:
            self.object.facilitators.add(self.request.user)
        return HttpResponseRedirect(reverse_lazy('projects:project-detail', kwargs={'pk': self.object.pk}))


@method_decorator(login_required, name='dispatch')
class ProjectDetailView(DetailView):
    model = Project

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        if not (context.get('is_facilitator') or context.get('is_member')):
            messages.error(request, "You are not a member or facilitator of this project!")
            return redirect('/')

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        kwargs['is_facilitator'] = self.request.user in self.object.facilitators.all()
        kwargs['is_member'] = (self.request.user.projectgroup_set.filter(project=self.object).count() > 0)

        try:
            kwargs['projectgroup'] = self.request.user.projectgroup_set.get(project=self.object)
        except ObjectDoesNotExist:
            kwargs['projectgroup'] = None

        return super(ProjectDetailView, self).get_context_data(**kwargs)


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

    def get_form(self, form_class=None):
        form = super(ProjectGroupCreateView, self).get_form(form_class)
        form.fields['members'].queryset = User.objects.exclude(project__pk=self.project.pk)
        return form
    
    def form_valid(self, form):
        form.instance.project = self.project
        return super(ProjectGroupCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProjectGroupUpdateView(UpdateView):
    model = ProjectGroup
    fields = ['name', 'members']

    def dispatch(self, request, *args, **kwargs):
        project_pk = self.kwargs.get('project_pk')
        try:
            self.project = Project.objects.get(pk=project_pk)
            if self.project.facilitators.filter(pk=request.user.pk).count() <= 0:
                messages.error(request, 'You are not authorised to perform this action!')
                return redirect('/')
        except ObjectDoesNotExist:
            return redirect('/')

        self.success_url = reverse_lazy('projects:project-detail', kwargs={'pk': self.project.pk})

        return super(ProjectGroupUpdateView, self).dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ProjectGroupDeleteView(DeleteView):
    model = ProjectGroup
    success_url = ''

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.success_url = reverse_lazy('projects:project-detail', kwargs={'pk': self.object.project.pk})
        if self.object.project.facilitators.filter(pk=request.user.pk).count() <= 0:
            messages.error(request, 'You do not have permission to delete this target!')
            return HttpResponseRedirect(self.success_url)

        return super(ProjectGroupDeleteView, self).dispatch(request, *args, **kwargs)
