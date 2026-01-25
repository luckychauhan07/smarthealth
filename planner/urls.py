from django.urls import path
from .views import (
    action_center,
    diet,
    gemini_api_test,
    generate_diet,
    generate_workout,
    workout,
)

urlpatterns = [
    path('action-center/', action_center, name='action_center'),
    path('generate-diet/', generate_diet, name='generate_diet'),
    path('generate-workout/', generate_workout, name='generate_workout'),
    path('diet/', diet, name='diet'),
    path('workout/', workout, name='workout'),
    path('api/gemini-test/', gemini_api_test),
]
