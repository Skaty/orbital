from django.conf.urls import url, include

from miscellaneous.views import RegistrationView

urlpatterns = [
    url(r'^register/$', RegistrationView.as_view(), name='register'),
]
