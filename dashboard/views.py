from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from google.api_core.exceptions import ResourceExhausted
from health.models import HealthProfile
from planner.models import GeneratedPlan



@login_required
def dashboard_view(request):
    user = request.user

    # ✅ SAFE HealthProfile fetch
    profile, _ = HealthProfile.objects.get_or_create(user=user)
    plan = GeneratedPlan.objects.filter(user=user).first()
    error_message = None
    print(plan)
    # Dashboard should never trigger plan generation; only display existing
    # plans or guide users to Action Center.

    return render(request, "dashboard.html", {
        "profile": profile,
        "plan": plan,
        "error_message": error_message,
    })
