from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from notifications.signals import notify

from targets.models import TargetAssignment, Target


@receiver(post_save, sender=TargetAssignment, dispatch_uid="target_assignment_post_save")
def target_assignment_post_save(sender, **kwargs):
    if kwargs['created']:
        msg = u'has been assigned to you'
        notify.send(kwargs['instance'].target, recipient=kwargs['instance'].assignee, verb=msg)

    is_completed_by_all = kwargs['instance'].target.targetassignment_set.filter(marked_completed_on=None).count() == 0
    if is_completed_by_all:
        target = kwargs['instance'].target
        target.completed_on = kwargs['instance'].marked_completed_on
        target.save()