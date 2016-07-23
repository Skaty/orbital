from django.conf.urls import url

from profiles.views import ProfileDetailView

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', ProfileDetailView.as_view(), name='project-detail'),
]