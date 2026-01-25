# health/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import HealthProfile

@receiver(post_save, sender=User)
def create_health_profile(sender, instance, created, **kwargs):
    if created:
        HealthProfile.objects.create(user=instance)
