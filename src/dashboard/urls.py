from django.conf.urls import url, include

from dashboard import views

urlpatterns = [
    url(r'^(?P<project_id>[0-9]+)/$', views.home_view, name='home'),
]
