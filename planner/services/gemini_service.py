import json
import logging
import time
import traceback
from typing import List

import google.generativeai as genai
from django.conf import settings
from google.api_core.exceptions import ResourceExhausted

logger = logging.getLogger(__name__)

# -------------------------------------------------------------------
# Gemini configuration
# -------------------------------------------------------------------
genai.configure(api_key=settings.GEMINI_API_KEY)

MODEL_NAME = "models/gemini-2.5-flash"

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    generation_config={
        "response_mime_type": "application/json",
        "temperature": 0.7,
        "max_output_tokens": 2048,
    },
)



def safe_json_parse(text: str) -> dict:
    """
    Safely extract and parse JSON from Gemini response
    """
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start == -1 or end == -1:
            raise ValueError("No JSON object found")

        cleaned = text[start:end]
        return json.loads(cleaned)

    except Exception:
        logger.error("Failed to safely parse Gemini JSON")
        logger.error(f"Raw response:\n{text}")
        raise

def build_prompt_diet(profile) -> str:
    return (
        "Generate a 7-day fitness plan in STRICT JSON format with keys:\n"
        "diet_plan (list of {day, meals[]}),\n"
        "tips (list of strings).\n\n"
        f"User profile:\n"
        f"Goal: {profile.goal}\n"
        f"Weight (kg): {profile.weight_kg}\n"
        f"Height (cm): {profile.height_cm}\n"
        f"Diet: {profile.diet_type}\n"
        f"Meals per day: {profile.meals_per_day}\n"
        f"Health conditions: {', '.join(profile.health_conditions or [])}\n\n"
        "Return ONLY valid JSON. No markdown. No explanation."
    )


def build_prompt_workout(profile) -> str:
    return (
        "Generate a 7-day workout plan in STRICT JSON format with keys:\n"
        "workout_plan (list of {day, workout}),\n"
        "tips (list of strings).\n\n"
        f"User profile:\n"
        f"Goal: {profile.goal}\n"
        f"Weight (kg): {profile.weight_kg}\n"
        f"Height (cm): {profile.height_cm}\n"
        f"Activity level: {profile.activity_level}\n"
        f"Fitness experience: {profile.fitness_experience}\n"
        f"Workout days per week: {profile.workout_days_per_week}\n"
        f"Workout duration (minutes): {profile.workout_duration_minutes}\n"
        f"Health conditions: {', '.join(profile.health_conditions or [])}\n\n"
        "Return ONLY valid JSON. No markdown. No explanation."
    )

def generate_diet_plan(profile):
    prompt = build_prompt_diet(profile)
    try:
        model_response = model.generate_content(prompt)
        print("Gemini raw response:", model_response.text)
        response=safe_json_parse(model_response.text)
        print("Gemini response data:", response)
        return response

       
    except ResourceExhausted:
        logger.error(
            "Gemini API rate limit exceeded after retries. "
            "Consider implementing request throttling or upgrading API quota."
        )
        return get_fallback_plan()
    except Exception:
        return get_fallback_plan()
    

def generate_workout_plan(profile):
    prompt = build_prompt_workout(profile)
    try:
        model_response = model.generate_content(prompt)
        print("Gemini raw response:", model_response.text)
        response=safe_json_parse(model_response.text)
        print("Gemini response data:", response)
        return response

       
    except ResourceExhausted:
        logger.error(
            "Gemini API rate limit exceeded after retries. "
            "Consider implementing request throttling or upgrading API quota."
        )
        return get_fallback_plan()
    except Exception:
        return get_fallback_plan()


def get_fallback_plan() -> dict:
    """Safe fallback plan when API calls fail."""
    return {
        "diet_plan": [
            {"day": "Monday", "meals": ["Oatmeal with fruits", "Grilled chicken with rice", "Salmon with vegetables"]},
            {"day": "Tuesday", "meals": ["Eggs and toast", "Turkey sandwich", "Pasta with lean meat"]},
            {"day": "Wednesday", "meals": ["Smoothie bowl", "Tuna salad", "Grilled steak with potatoes"]},
            {"day": "Thursday", "meals": ["Yogurt and granola", "Chicken wrap", "Fish with brown rice"]},
            {"day": "Friday", "meals": ["Pancakes", "Beef tacos", "Shrimp with noodles"]},
            {"day": "Saturday", "meals": ["French toast", "Pork chops with vegetables", "Homemade pizza"]},
            {"day": "Sunday", "meals": ["Pancakes", "Roasted chicken", "Vegetable curry with rice"]},
        ],
        "workout_plan": [
            {"day": "Monday", "workout": "Chest & Triceps (45 min)"},
            {"day": "Tuesday", "workout": "Back & Biceps (45 min)"},
            {"day": "Wednesday", "workout": "Rest or light cardio"},
            {"day": "Thursday", "workout": "Legs (45 min)"},
            {"day": "Friday", "workout": "Shoulders & Core"},
            {"day": "Saturday", "workout": "HIIT cardio"},
            {"day": "Sunday", "workout": "Rest"},
        ],
        "tips": [
            "Stay hydrated",
            "Sleep 7–9 hours",
            "Warm up before workouts",
            "Be consistent",
        ],
    }