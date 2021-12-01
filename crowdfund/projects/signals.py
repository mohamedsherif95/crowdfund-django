from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Project, Donation


@receiver(post_save, sender=Donation)
def update_current(sender, instance, created, **kwargs):
    if created:
        instance.project.current += instance.amount
        instance.project.save()