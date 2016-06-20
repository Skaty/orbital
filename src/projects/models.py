from django.conf import settings
from django.db import models
from django.utils import timezone


class Project(models.Model):
    name = models.CharField(max_length=255)
    facilitators = models.ManyToManyField(settings.AUTH_USER_MODEL)
    created_on = models.DateTimeField(auto_now_add=True)
    ends_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    def is_active(self):
        "Checks if the project has ended"
        return self.ends_on >= timezone.now() if self.ends_on else True


class ProjectGroup(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
