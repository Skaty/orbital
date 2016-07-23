from django.conf.urls import url

from profiles.views import ProfileDetailView, PreferencesUpdateView

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', ProfileDetailView.as_view(), name='profile-detail'),
    url(r'^update/', PreferencesUpdateView.as_view(), name='preferences-update')
]