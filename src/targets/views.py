import inspect

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import View, CreateView, DeleteView, UpdateView

from projects.models import Project
from targets.models import Target, Goal, Milestone, AbstractTarget


@method_decorator(login_required, name='dispatch')
class CompleteAchievementView(View):
    type = None
    object = None

    def post(self, request, *args, **kwargs):
        if not inspect.isclass(self.type) or not issubclass(self.type, AbstractTarget):
            print(kwargs)
            return redirect('/')

        try:
            self.object = self.type.objects.get(pk=self.kwargs.get('pk', None))
        except ObjectDoesNotExist:
            messages.error(request, 'Sorry, we are unable to process your request at the moment!')
            return redirect('/')

        if not self.object.has_permission(request.user):
            messages.error(request, 'You are not authorised to perform this action!')
            return redirect('/')

        self.object.completed_on = timezone.now()
        self.object.save()

        messages.info(request, 'You have marked {} as completed'.format(self.object))

        return redirect('projects:project-detail',kwargs={'pk': self.kwargs.get('project_pk')})

class TargetGoalCreateView(CreateView):
    template_name_suffix = '_group_create_form'
    model = Target
    fields = ['name', 'milestone', 'description', 'deadline']
    success_url = reverse_lazy('projects:project-list')

    def dispatch(self, request, *args, **kwargs):
        self.project_pk = self.kwargs.get('project_pk')
        try:
            self.projectgroup = request.user.projectgroup_set.get(project__pk=self.project_pk)
        except ObjectDoesNotExist:
            return redirect('/')

        self.success_url = reverse_lazy('projects:project-detail',kwargs={'pk': self.project_pk})

        return super(TargetGoalCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Adds projectgroup to template context
        """
        kwargs['projectgroup'] = self.projectgroup
        return super(TargetGoalCreateView, self).get_context_data(**kwargs)

    def get_form(self, form_class=None):
        form = super(TargetGoalCreateView, self).get_form(form_class)
        form.fields['milestone'].queryset = Milestone.objects.filter(project__pk=self.project_pk)
        return form

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
        project_pk = self.kwargs.get('project_pk')
        try:
            self.project = Project.objects.get(id=project_pk)
            if request.user not in self.project.facilitators.all():
                messages.error(request, 'You are not authorised to perform this action!')
                return redirect('/')
        except ObjectDoesNotExist:
            return redirect('/')

        self.success_url = reverse_lazy('projects:project-detail', pk=self.project.pk)

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
        project_pk = self.kwargs.get('project_pk')
        try:
            self.project = Project.objects.get(pk=project_pk)
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
        self.success_url = reverse_lazy('projects:project-detail', kwargs={'pk': self.object.group.project.pk})
        if self.object.created_by != request.user:
            messages.error(request, 'You do not have permission to delete this target!')
            return HttpResponseRedirect(self.success_url)

        return super(TargetDeleteView, self).dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class MilestoneCreateView(CreateView):
    model = Milestone
    template_name_suffix = '_form'
    fields = ['name', 'description', 'deadline']
    success_url = ''

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

        return super(MilestoneCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Adds project instance to template context
        """
        kwargs['project'] = self.project
        return super(MilestoneCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.project = self.project
        form.instance.created_by = self.request.user
        return super(MilestoneCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class MilestoneUpdateView(UpdateView):
    model = Milestone
    template_name_suffix = '_form'
    fields = ['name', 'description', 'deadline']

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

        return super(MilestoneUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Adds project instance to template context
        """
        kwargs['project'] = self.project
        return super(MilestoneUpdateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.project = self.project
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Milestone for {project} has been successfuly modified!'.format(project=self.project))
        return super(MilestoneUpdateView, self).form_valid(form)


class MilestoneDeleteView(DeleteView):
    model = Milestone
    success_url = ''

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.success_url = reverse_lazy('projects:project-detail', kwargs={'pk': self.object.project.pk})
        if self.object.project.facilitators.filter(pk=request.user.pk).count() <= 0:
            messages.error(request, 'You do not have permission to delete this target!')
            return HttpResponseRedirect(self.success_url)

        return super(MilestoneDeleteView, self).dispatch(request, *args, **kwargs)