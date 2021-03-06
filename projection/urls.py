"""projection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from miscellaneous.views import HomepageView

urlpatterns = [
    url(r'^$', HomepageView.as_view(), name='homepage'),
    url(r'^sso/', include('social.apps.django_app.urls', namespace='sso')),
    url(r'^admin/', admin.site.urls),
    url(r'^projects/', include('projects.urls', namespace='projects')),
    url(r'^achievements/', include('targets.urls', namespace='achievements')),
    url(r'^auth/', include('django.contrib.auth.urls', namespace='authentication')),
    url(r'^system/', include('miscellaneous.urls', namespace='system')),
    url(r'^profiles/', include('profiles.urls', namespace='profiles')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include([
        url('^projects/', include('projects.api.urls', namespace='projects_api')),
        url('^achievements/', include('targets.api.urls', namespace='achievements_api')),
    ])),
    url(r'^messaging/', include('postman.urls', namespace='postman')),
]
