from django.conf.urls import url

from projects.views import ProjectListView, ProjectDetailView

urlpatterns = [
    url(r'^$', ProjectListView.as_view(), name='project-list'),
    url(r'^(?P<pk>[0-9]+)/', ProjectDetailView.as_view(), name='project-detail')
]