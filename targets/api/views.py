from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from targets.models import *
from .serializers import *


class TargetViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Target.objects.filter(group__members=request.user)
        serializer = TargetSerializer(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Target.objects.all()
        target = get_object_or_404(queryset, pk=pk)

        if not request.user.projectgroup_set.filter(target=target).exists():
            raise PermissionDenied('You are not a group member of the group with this target!')

        serializer = TargetSerializer(target)
        return Response(serializer.data)


class MilestoneViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        queryset = Milestone.objects.all()
        milestone = get_object_or_404(queryset, pk=pk)

        if not milestone.project.facilitators.filter(pk=request.user.pk).exists():
            raise PermissionDenied('You are not a facilitator for this project!')

        serializer = MilestoneSerializer(milestone)
        return Response(serializer.data)


class GoalViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        queryset = Goal.objects.all()
        goal = get_object_or_404(queryset, pk=pk)

        if not (request.user.project_set.filter(goal=goal).exists() or request.user.projectgroup_set.filter(project__goal=goal).exists()):
            raise PermissionDenied('You are not a facilitator for this project!')

        serializer = MilestoneSerializer(goal)
        return Response(serializer.data)