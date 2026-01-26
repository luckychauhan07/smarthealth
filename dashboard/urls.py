from django.urls import path
from .views import dashboard_view
from .views import (
    
    dashboard_diet,
    dashboard_workout,
)

urlpatterns = [
    path("", dashboard_view, name="dashboard"),
    # path("home/", dashboard_home, name="dashboard_home"),
    path("diet/", dashboard_diet, name="dashboard_diet"),
    path("workout/", dashboard_workout, name="dashboard_workout"),
]
