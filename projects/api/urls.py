from rest_framework import routers

from projects.api.views import *

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, base_name='projects')
router.register(r'groups', ProjectGroupViewSet, base_name='groups')

urlpatterns = router.urls