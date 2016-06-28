from django.conf.urls import url, include

from projects.views import *

urlpatterns = [
    url(r'^$', ProjectListView.as_view(), name='project-list'),
    url(r'^create/$', ProjectCreateView.as_view(), name='project-create'),
    url(r'^(?P<pk>[0-9]+)/$', ProjectDetailView.as_view(), name='project-detail'),
    url(r'^(?P<project_pk>[0-9]+)/', include('targets.urls', namespace='achievements')),
    url(r'^(?P<project_pk>[0-9]+)/groups/add/$', ProjectGroupCreateView.as_view(), name='group-create'),
    url(r'^(?P<project_pk>[0-9]+)/groups/(?P<pk>[0-9]+)/edit/$', ProjectGroupUpdateView.as_view(), name='group-edit'),
    url(r'^(?P<project_pk>[0-9]+)/groups/(?P<pk>[0-9]+)/delete/$', ProjectGroupDeleteView.as_view(), name='group-delete')
]