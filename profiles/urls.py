from django.conf.urls import url, include

from profiles.views import ProfileDetailView, PreferencesUpdateView, PasswordUpdateView, PreferencesDisplay, \
    ProfileUpdateView

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', ProfileDetailView.as_view(), name='profile-detail'),
    url(r'^update/', include([
        url(r'^$', PreferencesDisplay.as_view(), name='preferences-display'),
        url(r'^password/$', PasswordUpdateView.as_view(), name='password-update'),
        url(r'^preferences/$', PreferencesUpdateView.as_view(), name='preferences-update'),
        url(r'^profile/$', ProfileUpdateView.as_view(), name='profile-update'),
    ]))
]