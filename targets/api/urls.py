from rest_framework import routers

from targets.api.views import *

router = routers.DefaultRouter()
router.register(r'targets', TargetViewSet, base_name='targets')
router.register(r'milestones', MilestoneViewSet, base_name='milestones')
router.register(r'goals', GoalViewSet, base_name='goals')

urlpatterns = router.urls