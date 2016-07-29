from rest_framework import serializers

from targets.models import *


class TargetSerializer(serializers.ModelSerializer):
    completed_by = serializers.SerializerMethodField()

    def get_completed_by(self, obj):
        return obj.targetassignment_set.filter(marked_completed_on__isnull=False).values_list('assignee', flat=True)

    class Meta:
        model = Target
        fields = ('id', 'name', 'created_on', 'completed_on', 'deadline', 'group', 'milestone', 'assigned_to', 'completed_by')


class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = ('id', 'name', 'created_on', 'completed_on', 'deadline', 'project')


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ('id', 'name', 'created_on', 'completed_on', 'deadline', 'project')