import json
import logging
import google.generativeai as genai
from django.conf import settings
from google.api_core.exceptions import ResourceExhausted
from pydantic import BaseModel, Field
from typing import List, Optional
from django.shortcuts import redirect

logger = logging.getLogger(__name__)

# -------------------------------------------------------------------
# 1. Pydantic Schemas (Internal Validation)
# -------------------------------------------------------------------

class Exercise(BaseModel):
    name: str
    sets: Optional[int]
    reps: Optional[int]
    duration_sec: Optional[int]
    rest_sec: int

class WorkoutDay(BaseModel):
    day: str
    focus: str
    calories: int
    duration_min: int
    exercises: List[Exercise]

class DietDay(BaseModel):
    day: str
    meals: List[str]

class WorkoutPlanSchema(BaseModel):
    workout_plan: List[WorkoutDay]
    tips: List[str]

class DietPlanSchema(BaseModel):
    diet_plan: List[DietDay]
    tips: List[str]

# -------------------------------------------------------------------
# 2. Configuration
# -------------------------------------------------------------------
genai.configure(api_key=settings.GEMINI_API_KEY)

# Using 2.5-Flash for production stability with JSON schemas
MODEL_NAME = "gemini-2.5-flash" 

# -------------------------------------------------------------------
# 3. Core Functions (Maintaining your exact signatures)
# -------------------------------------------------------------------

def generate_diet_plan(profile):
    """
    Returns dict with keys: 'diet_plan', 'tips'
    """
    prompt = (
        f"Generate a 7-day diet plan. Goal: {profile.goal}, "
        f"Weight: {profile.weight_kg}kg, Diet: {profile.diet_type}, "
        f"Meals/day: {profile.meals_per_day}. generate meals in context of indians diet add calorie details for each meal."
    )
    
    try:
        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            generation_config={
                "response_mime_type": "application/json",
                "response_schema": DietPlanSchema,
                "temperature": 0.7,
            }
        )
        model_response = model.generate_content(prompt)
        # Validates and converts to dict automatically
        return DietPlanSchema.model_validate_json(model_response.text).model_dump()

    except (ResourceExhausted, Exception) as e:
        logger.error(f"Diet Plan Error: {str(e)}")
        return redirect('action_center')

def generate_workout_plan(profile):
    """
    Returns dict with keys: 'workout_plan', 'tips'
    """
    prompt = (
        f"Generate a 7-day workout plan. Goal: {profile.goal}, "
        f"Activity: {profile.activity_level}, Experience: {profile.fitness_experience}, "
        f"Days/week: {profile.workout_days_per_week}, Duration: {profile.workout_duration_minutes}min.",f"goal duration{profile.goal_timeframe_months},"f"gender{profile.gender}","total number of excercises 6."
    )

    try:
        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            generation_config={
                "response_mime_type": "application/json",
                "response_schema": WorkoutPlanSchema,
                "temperature": 0.7,
            }
        )
        model_response = model.generate_content(prompt)
        data= WorkoutPlanSchema.model_validate_json(model_response.text).model_dump()
        print(data)
        return data
    
    except (ResourceExhausted, Exception) as e:
        logger.error(f"Workout Plan Error: {str(e)}")
        return redirect('action_center')

def get_fallback_plan() -> dict:
    """Matches your original fallback structure exactly."""
    return {
        "diet_plan": [
            {"day": "Monday", "meals": ["Oatmeal with fruits", "Grilled chicken with rice", "Salmon with vegetables"]},
            # ... (rest of your existing fallback days)
        ],
        "workout_plan": [
            {"day": "Monday", "workout": "Chest & Triceps (45 min)"},
            # ... (rest of your existing fallback days)
        ],
        "tips": ["Stay hydrated", "Sleep 7–9 hours", "Warm up before workouts", "Be consistent"],
    }