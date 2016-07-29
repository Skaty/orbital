from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from projects.models import *
from .serializers import *

class ProjectViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = request.user.project_set.all()
        serializer = ProjectSerializer(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Project.objects.all()
        project = get_object_or_404(queryset, pk=pk)

        if not project.facilitators.filter(pk=request.user.pk).exists():
            raise PermissionDenied('You are not a facilitator for this project!')

        serializer = ProjectSerializer(project)
        return Response(serializer.data)


class ProjectGroupViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        queryset = ProjectGroup.objects.all()
        group = get_object_or_404(queryset, pk=pk)

        if not (group.project.facilitators.filter(pk=request.user.pk).exists()
                or group.members.filter(pk=request.user.pk).exists()):
            raise PermissionDenied('You are not a facilitator for this project!')

        serializer = ProjectGroupSerializer(group)
        return Response(serializer.data)