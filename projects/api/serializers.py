from rest_framework import serializers

from projects.models import *


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'created_on', 'ends_on', 'projectgroup_set', 'goal', 'milestone_set')


class ProjectGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectGroup
        fields = ('name', 'members', 'project')