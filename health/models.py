from django.db import models
from django.contrib.auth.models import User


class HealthProfile(models.Model):

    # ------------------
    # BASIC INFO
    # ------------------
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="health_profile"
    )

    age = models.PositiveIntegerField(default=18)
    height_cm = models.FloatField(default=170)
    weight_kg = models.FloatField(default=60)
    bmi = models.FloatField(blank=True, null=True)

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default="other"
    )

    # ------------------
    # GOALS
    # ------------------
    GOAL_CHOICES = [
        ("weight_loss", "Weight Loss"),
        ("muscle_gain", "Muscle Gain"),
        ("general_fitness", "General Fitness"),
        ("endurance", "Endurance"),
    ]

    goal = models.CharField(
        max_length=30,
        choices=GOAL_CHOICES,
        default="general_fitness"
    )

    target_weight_kg = models.FloatField(default=60)

    goal_timeframe_months = models.PositiveIntegerField(
        default=3,
        help_text="Time to achieve goal in months"
    )

    # ------------------
    # ACTIVITY & FITNESS
    # ------------------
    ACTIVITY_LEVEL_CHOICES = [
        ("sedentary", "Sedentary"),
        ("light", "Light Active"),
        ("moderate", "Moderate"),
        ("very_active", "Very Active"),
    ]

    EXPERIENCE_LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    activity_level = models.CharField(
        max_length=20,
        choices=ACTIVITY_LEVEL_CHOICES,
        default="sedentary"
    )

    fitness_experience = models.CharField(
        max_length=20,
        choices=EXPERIENCE_LEVEL_CHOICES,
        default="beginner"
    )

    workout_days_per_week = models.PositiveIntegerField(default=3)
    workout_duration_minutes = models.PositiveIntegerField(default=45)

    workout_preferences = models.JSONField(
        blank=True,
        null=True,
        help_text="gym, home, cardio, strength, yoga, hiit"
    )

    # ------------------
    # NUTRITION
    # ------------------
    DIET_CHOICES = [
        ("vegetarian", "Vegetarian"),
        ("non_vegetarian", "Non Vegetarian"),
        ("vegan", "Vegan"),
    ]

    WATER_INTAKE_CHOICES = [
        ("less_1", "Less than 1L"),
        ("1_2", "1-2 Liters"),
        ("2_3", "2-3 Liters"),
        ("more_3", "More than 3 Liters"),
    ]

    diet_type = models.CharField(
        max_length=20,
        choices=DIET_CHOICES,
        default="vegetarian"
    )

    meals_per_day = models.PositiveIntegerField(default=3)

    water_intake = models.CharField(
        max_length=10,
        choices=WATER_INTAKE_CHOICES,
        default="1_2"
    )

    food_allergies = models.JSONField(blank=True, null=True)

    # ------------------
    # HEALTH & LIFESTYLE
    # ------------------
    SLEEP_CHOICES = [
        ("less_5", "< 5 hours"),
        ("5_6", "5-6 hours"),
        ("6_7", "6-7 hours"),
        ("7_8", "7-8 hours"),
        ("more_8", "> 8 hours"),
    ]

    STRESS_CHOICES = [
        ("low", "Low"),
        ("moderate", "Moderate"),
        ("high", "High"),
    ]

    sleep_hours = models.CharField(
        max_length=10,
        choices=SLEEP_CHOICES,
        default="7_8"
    )

    stress_level = models.CharField(
        max_length=10,
        choices=STRESS_CHOICES,
        default="moderate"
    )

    health_conditions = models.JSONField(blank=True, null=True)

    additional_notes = models.TextField(blank=True, null=True)
    onboarding_completed = models.BooleanField(default=False)

    # ------------------
    # SYSTEM FIELDS
    # ------------------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    onboarding_completed = models.BooleanField(default=False)

    # ------------------
    # METHODS
    # ------------------
    def calculate_bmi(self):
        height_cm = float(self.height_cm)
        weight_kg = float(self.weight_kg)
        height_m = height_cm / 100
        return round(weight_kg / (height_m ** 2), 2)

    def save(self, *args, **kwargs):
        self.bmi = self.calculate_bmi()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} | Health Profile"
    class Meta:
        app_label = "health"