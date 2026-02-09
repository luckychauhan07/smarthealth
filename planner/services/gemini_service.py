import logging
import google.generativeai as genai
from django.conf import settings
from google.api_core.exceptions import ResourceExhausted
from pydantic import BaseModel, Field
from typing import List, Optional
from django.shortcuts import redirect

logger = logging.getLogger(__name__)

# -------------------------------------------------------------------
# 1. Pydantic Schemas (Enforcing Strict Structure)
# -------------------------------------------------------------------

class Exercise(BaseModel):
    # Avoid defaults in schema; Gemini rejects "default" fields. Optional values are nullable but required in shape.
    name: str = Field(description="Name of the exercise")
    sets: Optional[int]
    reps: Optional[int]
    duration_sec: Optional[int]
    rest_sec: int = Field(description="Rest time between sets")

class WorkoutDay(BaseModel):
    day: str
    focus: str = Field(description="Main muscle group or workout type (e.g., Push Day, Cardio)")
    calories: int = Field(description="Estimated calories burned")
    duration_min: int
    exercises: List[Exercise]

class DietDay(BaseModel):
    day: str
    meals: List[str] = Field(description="List of meals with calorie details included in the string")

class WorkoutPlanSchema(BaseModel):
    workout_plan: List[WorkoutDay]
    tips: List[str]

class DietPlanSchema(BaseModel):
    diet_plan: List[DietDay]
    tips: List[str]

# -------------------------------------------------------------------
# 2. Configuration & Model Setup
# -------------------------------------------------------------------

genai.configure(api_key=settings.GEMINI_API_KEY)

# Note: Gemini 1.5 Flash is currently the most stable for Constrained Output (JSON)
MODEL_NAME = "gemini-2.5-flash" 

def get_configured_model(schema):
    return genai.GenerativeModel(
        model_name=MODEL_NAME,
        generation_config={
            "response_mime_type": "application/json",
            "response_schema": schema,
            "temperature": 0.7,
        }
    )

# -------------------------------------------------------------------
# 3. Core Generation Functions
# -------------------------------------------------------------------

def generate_diet_plan(profile):
    """
    Generates an Indian diet plan based on full user profile.
    Returns: Dict containing 'diet_plan' and 'tips'
    """
    prompt = (
        f"Generate a 7-day Indian diet plan for a {profile.age}yo {profile.gender}. "
        f"Goal: {profile.goal}, Current Weight: {profile.weight_kg}kg, Target: {profile.target_weight_kg}kg. "
        f"Diet Type: {profile.diet_type}, Meals per Day: {profile.meals_per_day}. "
        f"Allergies: {', '.join(profile.food_allergies or ['None'])}, "
        f"Health Conditions: {', '.join(profile.health_conditions or ['None'])}. "
        f"Water Intake: {profile.water_intake}L/day, Avg Sleep: {profile.sleep_hours}hrs. "
        "Strictly ensure meals are Indian-style and include approximate calories for each meal."
    )

    try:
        model = get_configured_model(DietPlanSchema)
        response = model.generate_content(prompt)
        return DietPlanSchema.model_validate_json(response.text).model_dump()
    except Exception as e:
        logger.error(f"Diet Plan API Error: {str(e)}")
        return redirect('action_center')

def generate_workout_plan(profile):
    """
    Generates a workout plan based on full biometric and lifestyle data.
    Returns: Dict containing 'workout_plan' and 'tips'
    """
    prompt = (
        f"Generate a 7-day workout plan for a {profile.gender}, age {profile.age}. "
        f"Biometrics: BMI {profile.bmi}, Weight {profile.weight_kg}kg, Height {profile.height_cm}cm. "
        f"Experience: {profile.fitness_experience}, Activity Level: {profile.activity_level}. "
        f"Schedule: {profile.workout_days_per_week} days/week, {profile.workout_duration_minutes} min/session. "
        f"Preferences: {profile.workout_preferences}. "
        f"Health Constraints: {', '.join(profile.health_conditions or ['None'])}. "
        f"Stress Level: {profile.stress_level}. "
        "Rules: Provide exactly 6 exercises per day. If health conditions exist, provide low-impact alternatives."
    )

    try:
        model = get_configured_model(WorkoutPlanSchema)
        response = model.generate_content(prompt)
        return WorkoutPlanSchema.model_validate_json(response.text).model_dump()
    except Exception as e:
        logger.error(f"Workout Plan API Error: {str(e)}")
        return get_workout_fallback()

# -------------------------------------------------------------------
# 4. Fallback Data (Specific to Request Type)
# -------------------------------------------------------------------

def get_diet_fallback():
    return {
        "diet_plan": [
            {"day": "Monday", "meals": ["Poha (300 kcal)", "Dal Tadka & Rice (450 kcal)", "Paneer Tikka (400 kcal)"]},
            {"day": "Tuesday", "meals": ["Oats Upma (250 kcal)", "Vegetable Khichdi (400 kcal)", "Moong Dal Chilla (350 kcal)"]},
        ],
        "tips": ["Drink 3L water", "Avoid sugar", "Prioritize protein"]
    }

def get_workout_fallback():
    return {
        "workout_plan": [
            {
                "day": "Monday", 
                "focus": "Full Body", 
                "calories": 350, 
                "duration_min": 45, 
                "exercises": [
                    {"name": "Bodyweight Squats", "sets": 3, "reps": 15, "rest_sec": 60},
                    {"name": "Push-ups", "sets": 3, "reps": 12, "rest_sec": 60}
                ]
            }
        ],
        "tips": ["Warm up for 10 mins", "Focus on form", "Consistency is key"]
    }