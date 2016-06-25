from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def home_view(request, project_id):
    project_group = request.user.projectgroup_set.filter(project_id=project_id)

    if len(project_group) == 0:
        return redirect('/')

    project_group = project_group[0]

    return render(request, 'dashboard/main.html', {'projectgroup': project_group})