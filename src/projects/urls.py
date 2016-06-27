from django.conf.urls import url

from projects.views import ProjectListView, ProjectCreateView, ProjectDetailView, ProjectGroupCreateView

urlpatterns = [
    url(r'^$', ProjectListView.as_view(), name='project-list'),
    url(r'^create/$', ProjectCreateView.as_view(), name='project-create'),
    url(r'^(?P<pk>[0-9]+)/$', ProjectDetailView.as_view(), name='project-detail'),
    url(r'^(?P<project_pk>[0-9]+)/groups/add/$', ProjectGroupCreateView.as_view(), name='group-create')
]