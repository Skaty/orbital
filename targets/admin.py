from django.contrib import admin

from targets.models import Goal, Target, Milestone


class GoalInlineAdmin(admin.TabularInline):
    model = Goal

class MilestoneInlineAdmin(admin.TabularInline):
    model = Milestone

class TargetInlineAdmin(admin.TabularInline):
    model = Target