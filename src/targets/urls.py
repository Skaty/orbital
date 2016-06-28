from django.conf.urls import url, include

from targets.views import *

urlpatterns = [
    url(r'^targets/add/$', TargetGoalCreateView.as_view(), name="add-group-target"),
    url(r'^targets/(?P<pk>[0-9]+)/delete/$', TargetDeleteView.as_view(), name="delete-group-target"),
    url(r'^goals/add/$', GoalCreateView.as_view(), name="add-goal"),
    url(r'^goals/(?P<pk>[0-9]+)/$', GoalUpdateView.as_view(), name="update-goal"),
    url(r'^milestones/add/$', MilestoneCreateView.as_view(), name="add-milestone"),
    url(r'^milestones/(?P<pk>[0-9]+)/$', MilestoneUpdateView.as_view(), name="update-milestone"),
    url(r'^milestones/(?P<pk>[0-9]+)/delete/$', MilestoneDeleteView.as_view(), name="delete-milestone"),
]
