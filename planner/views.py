from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from google.api_core.exceptions import ResourceExhausted

from .models import UserPlanStatus
from health.models import HealthProfile
from planner.models import GeneratedPlan
from planner.services.gemini_service import generate_diet_plan, generate_workout_plan

@login_required
def action_center(request):
    plan_status, _ = UserPlanStatus.objects.get_or_create(
        user=request.user
    )

    return render(request, 'action_center.html', {
        'plan_status': plan_status
    })





@login_required
def generate_diet(request):
    if request.method != "POST":
        return redirect('action_center')
    
    user = request.user
    plan_status, _ = UserPlanStatus.objects.get_or_create(user=user)

    # Check onboarding completeness
    profile, _ = HealthProfile.objects.get_or_create(user=user)
    if not profile.onboarding_completed:
        messages.info(request, "Please complete your profile first.")
        return redirect('onboarding')

    # Get or create plan object
    plan, created = GeneratedPlan.objects.get_or_create(user=user)
    
    # Generate diet plan only if not already generated
    if not plan.diet_plan:
        try:
            data = generate_diet_plan(profile)
            plan.diet_plan = data.get("diet_plan", [])
            if not plan.safety_tips:  # Add tips if not already present
                plan.safety_tips = data.get("tips", [])
            plan.save()
            messages.success(request, "Diet plan generated successfully.")
        except ResourceExhausted:
            messages.error(request, "AI quota exceeded. Please try again in a few minutes.")
            return redirect('action_center')
        except Exception as e:
            messages.error(request, f"Error generating diet plan: {str(e)}")
            return redirect('action_center')
    else:
        messages.info(request, "Using your existing diet plan.")

    # Mark diet flag and go to dashboard
    if not plan_status.has_diet_plan:
        plan_status.has_diet_plan = True
        plan_status.save()
    
    return redirect('dashboard')


@login_required
def generate_workout(request):
    if request.method != "POST":
        return redirect('action_center')
    
    user = request.user
    plan_status, _ = UserPlanStatus.objects.get_or_create(user=user)

    # Check onboarding completeness
    profile, _ = HealthProfile.objects.get_or_create(user=user)
    if not profile.onboarding_completed:
        messages.info(request, "Please complete your profile first.")
        return redirect('onboarding')

    # Get or create plan object
    plan, created = GeneratedPlan.objects.get_or_create(user=user)
    
    # Generate workout plan only if not already generated
    if not plan.workout_plan:
        try:
            data = generate_workout_plan(profile)
            plan.workout_plan = data.get("workout_plan", [])
            if not plan.safety_tips:  # Add tips if not already present
                plan.safety_tips = data.get("tips", [])
            plan.save()
            messages.success(request, "Workout plan generated successfully.")
        except ResourceExhausted:
            messages.error(request, "AI quota exceeded. Please try again in a few minutes.")
            return redirect('action_center')
        except Exception as e:
            messages.error(request, f"Error generating workout plan: {str(e)}")
            return redirect('action_center')
    else:
        messages.info(request, "Using your existing workout plan.")

    # Mark workout flag and go to dashboard
    if not plan_status.has_workout_plan:
        plan_status.has_workout_plan = True
        plan_status.save()
    
    return redirect('dashboard')


@login_required
def diet(request):
    return redirect('dashboard')


@login_required
def workout(request):
    return redirect('dashboard')
from django.http import JsonResponse
from django.views.decorators.http import require_GET

import json
import google.generativeai as genai
from django.conf import settings


@require_GET
def gemini_api_test(request):
    """
    Super simple Gemini API test endpoint
    """

    try:
        # Configure Gemini
        genai.configure(api_key="AIzaSyDgUgidYWcKW90Wd6S76C-T789kFepoPeE")

        model = genai.GenerativeModel(
        model_name="models/gemini-2.5-flash",
        generation_config={
            "response_mime_type": "application/json",
            "temperature": 0.7,
            "max_output_tokens": 512,
        },
        )


        # VERY simple prompt
        prompt = """
        Return STRICT JSON only.

        {
          "status": "ok",
          "message": "Gemini API is working",
          "sample_plan": {
            "day": "Monday",
            "workout": "Full body workout"
          }
        }
        """

        response = model.generate_content(prompt)

        # Parse Gemini JSON
        data = json.loads(response.text)
        print("Gemini response data:", data)
        return JsonResponse({
            "success": True,
            "gemini_response": data
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)
