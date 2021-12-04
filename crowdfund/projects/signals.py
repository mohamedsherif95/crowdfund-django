from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Donation, Rating


@receiver(post_save, sender=Donation)
def update_current(sender, instance, created, **kwargs):
    if created:
        instance.project.current += instance.amount
        instance.project.save()

@receiver(post_save,sender=Rating)
def update_avg_rate(sender, instance, created, **kwargs):
    if created:
        instance.project.total_rates += int(instance.rate)
        instance.project.calc_avg_rate()
        instance.project.save()