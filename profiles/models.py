from django.db import models
from django.conf import settings
from pytz import common_timezones

# Create your models here.
class Preferences(models.Model):
    TZ_CHOICES = [(x, x.replace('_', ' ')) for x in common_timezones]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE)
    timezone = models.CharField(
        max_length=255,
        choices=TZ_CHOICES,
        default='UTC'
    )