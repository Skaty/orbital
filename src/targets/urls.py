from django.conf.urls import url, include

from targets.views import TargetGoalCreateView

urlpatterns = [
    url(r'^targets/add/$', TargetGoalCreateView.as_view(), name="add-group-target"),
]
