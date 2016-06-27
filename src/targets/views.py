from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, UpdateView

from projects.models import Project
from targets.models import Target, Goal


class TargetGoalCreateView(CreateView):
    template_name_suffix = '_group_create_form'
    model = Target
    fields = ['name', 'description', 'deadline']

    def dispatch(self, request, *args, **kwargs):
        project_id = self.kwargs.get('project_id')
        try:
            self.projectgroup = request.user.projectgroup_set.get(project_id=project_id)
        except ObjectDoesNotExist:
            return redirect('/')
        return super(TargetGoalCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Adds projectgroup to template context
        """
        kwargs['projectgroup'] = self.projectgroup
        return super(TargetGoalCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.group = self.projectgroup
        form.instance.created_by = self.request.user
        return super(TargetGoalCreateView, self).form_valid(form)


class GoalCreateView(CreateView):
    model = Goal
    template_name_suffix = '_form'
    fields = ['name', 'description', 'deadline']
    success_url = ''

    def dispatch(self, request, *args, **kwargs):
        project_id = self.kwargs.get('project_id')
        try:
            self.project = Project.objects.get(id=project_id)
            if request.user not in self.project.facilitators.all():
                messages.error(request, 'You are not authorised to perform this action!')
                return redirect('/')
        except ObjectDoesNotExist:
            return redirect('/')

        self.success_url = reverse_lazy('projects:project-detail', kwargs={'pk': self.project.pk})

        return super(GoalCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Adds project instance to template context
        """
        kwargs['project'] = self.project
        return super(GoalCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.project = self.project
        form.instance.created_by = self.request.user
        return super(GoalCreateView, self).form_valid(form)


class GoalUpdateView(UpdateView):
    model = Goal
    template_name_suffix = '_form'
    fields = ['name', 'description', 'deadline']

    def dispatch(self, request, *args, **kwargs):
        project_id = self.kwargs.get('project_id')
        try:
            self.project = Project.objects.get(id=project_id)
            if request.user not in self.project.facilitators.all():
                messages.error(request, 'You are not authorised to perform this action!')
                return redirect('/')
        except ObjectDoesNotExist:
            return redirect('/')

        self.success_url = reverse_lazy('projects:project-detail', kwargs={'pk': self.project.pk})

        return super(GoalUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Adds project instance to template context
        """
        kwargs['project'] = self.project
        return super(GoalUpdateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.project = self.project
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Goal for {project} has been successfuly modified!'.format(project=self.project))
        return super(GoalUpdateView, self).form_valid(form)


class TargetDeleteView(DeleteView):
    model = Target
    success_url = ''

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.success_url = reverse_lazy('dashboard:home', kwargs={'project_id': self.object.group.project.id})
        if self.object.created_by != request.user:
            messages.error(request, 'You do not have permission to delete this target!')
            return HttpResponseRedirect(self.success_url)

        return super(TargetDeleteView, self).dispatch(request, *args, **kwargs)