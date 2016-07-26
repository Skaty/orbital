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
    completed_on = models.DateTimeField(default=None, null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def is_due(self):
        return self.deadline and (self.deadline < timezone.now())

    def has_permission(self, user):
        return user == self.created_by

    class Meta:
        abstract = True


class Target(AbstractTarget):
    """
    Target represents a Goal for a particular ProjectGroup.
    Unlike a Goal, a ProjectGroup can have multiple Targets
    """
    group = models.ForeignKey('projects.ProjectGroup', on_delete=models.CASCADE)
    milestone = models.ForeignKey('targets.Milestone', default=None, null=True, blank=True, on_delete=models.SET_NULL)
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, through='TargetAssignment',
                                         related_name="assigned_targets")

    def __str__(self):
        return self.name


class TargetAssignment(models.Model):
    """
    Representation of an Assignment of Target to a User.

    Contains metadata regarding the assignment - such as whether the Target has been marked completed by the user
    """
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    target = models.ForeignKey(Target, on_delete=models.CASCADE)
    marked_completed_on = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return '{target} metadata for {user}'.format(target=self.target, user=self.assignee)


class Milestone(AbstractTarget):
    """
    Representation of a Milestone - a 'project-wide' goal.
    Kinda like Orbital's Milestone system :(

    Unlike Goals, there can be multiple Milestones per project
    """
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Goal(AbstractTarget):
    """
    Representation of a Goal - a singular, ultimate target
    for a Project. All ProjectGroups will be assigned to this goal
    """
    project = models.OneToOneField('projects.Project', on_delete=models.CASCADE)

    def __str__(self):
        return self.name