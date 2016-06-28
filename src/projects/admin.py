from django.contrib import admin

from projects.models import Project, ProjectGroup
from targets.admin import TargetInlineAdmin, GoalInlineAdmin, MilestoneInlineAdmin


class ProjectGroupInlineAdmin(admin.TabularInline):
    model = ProjectGroup

@admin.register(Project)
class ProjectModelAdmin(admin.ModelAdmin):
    model = Project
    inlines = [
        GoalInlineAdmin,
        MilestoneInlineAdmin,
        ProjectGroupInlineAdmin
    ]

@admin.register(ProjectGroup)
class ProjectGroupModelAdmin(admin.ModelAdmin):
    model = ProjectGroup
    inlines = [
        TargetInlineAdmin
    ]

