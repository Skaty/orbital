from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from profiles.models import Preferences


@receiver(post_save, sender=User, dispatch_uid="user_post_save")
def target_assignment_post_save(sender, **kwargs):
    user = kwargs['instance']
    if kwargs['created']:
        preferences = Preferences(user=user)
        preferences.save()