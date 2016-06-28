from django.conf import settings
from django.db import models
from django.utils import timezone


class AbstractTarget(models.Model):
    """
    AbstractTarget - an abstract model with fields that are common amongst
    all types of targets
    """
    name = models.CharField(max_length=255)
    description = models.TextField()

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True)

    def is_due(self):
        if not self.deadline:
            return False

        return self.deadline < timezone.now()

    class Meta:
        abstract = True


class Target(AbstractTarget):
    """
    Target represents a Goal for a particular ProjectGroup.
    Unlike a Goal, a ProjectGroup can have multiple Targets
    """
    group = models.ForeignKey('projects.ProjectGroup', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name


class Milestone(AbstractTarget):
    """
    Representation of a Milestone - a 'project-wide' goal.
    Kinda like Orbital's Milestone system :(

    Unlike Goals, there can be multiple Milestones per project
    """
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name


class Goal(AbstractTarget):
    """
    Representation of a Goal - a singular, ultimate target
    for a Project. All ProjectGroups will be assigned to this goal
    """
    project = models.OneToOneField('projects.Project', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name