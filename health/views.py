import profile
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import HealthProfile


@login_required
def onboarding_view(request):
    user = request.user

    # If onboarding already completed, skip onboarding
    if hasattr(user, "health_profile") and request.method == "GET":
        profile = user.health_profile
        if profile.onboarding_completed:
            return redirect("dashboard")

    if request.method == "POST":
        profile, created = HealthProfile.objects.get_or_create(user=user)

        # -------- BASIC INFO --------
        profile.age = int(request.POST.get("age", 18))
        profile.height_cm = float(request.POST.get("height", 170))
        profile.weight_kg = float(request.POST.get("weight", 60))
        profile.gender = request.POST.get("gender")

        # -------- GOALS --------
        profile.goal = request.POST.get("goal")
        profile.target_weight_kg = float(request.POST.get("target_weight", 60))
        profile.goal_timeframe_months = int(request.POST.get("timeframe", 3))

        # -------- ACTIVITY & FITNESS --------
        profile.activity_level = request.POST.get("activity")
        profile.fitness_experience = request.POST.get("experience")
        profile.workout_days_per_week = int(request.POST.get("workout_days", 3))
        profile.workout_duration_minutes = int(request.POST.get("workout_duration", 45))

        profile.workout_preferences = request.POST.getlist("workout_type[]")

        # -------- NUTRITION --------
        profile.diet_type = request.POST.get("diet")
        profile.meals_per_day = int(request.POST.get("meals_per_day", 3))
        profile.water_intake = request.POST.get("water_intake")
        profile.food_allergies = request.POST.getlist("allergies[]")

        # -------- HEALTH & LIFESTYLE --------
        profile.sleep_hours = request.POST.get("sleep_hours")
        profile.stress_level = request.POST.get("stress_level")
        profile.health_conditions = request.POST.getlist("conditions[]")
        profile.additional_notes = request.POST.get("additional_notes")
        profile.onboarding_completed = True 
        # Save (BMI auto-calculates here)
        profile.save()

        # After onboarding, send user to action_center to generate plans
        return redirect("action_center")

    return render(request, "onboarding.html")
