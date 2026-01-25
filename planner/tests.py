from django.db import models
from django.contrib.auth.models import User


class GeneratedPlan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    diet_plan = models.JSONField()
    workout_plan = models.JSONField()
    safety_tips = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Generated Plan"
