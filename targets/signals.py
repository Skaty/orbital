from django.db.models.signals import post_save
from django.dispatch import receiver
from targets.models import TargetAssignment

@receiver(post_save, sender=TargetAssignment, dispatch_uid="target_assignment_post_save")
def target_assignment_post_save(sender, **kwargs):
    is_completed_by_all = kwargs['instance'].target.targetassignment_set.filter(marked_completed_on=None).count() == 0
    print(is_completed_by_all)
    if is_completed_by_all:
        target = kwargs['instance'].target
        target.completed_on = kwargs['instance'].marked_completed_on
        target.save()