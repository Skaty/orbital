from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView

from targets.models import Target


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