from django.urls import path

from . import views

from .views import register_view, login_view, logout_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # accounts/urls.py
path("action-center/", views.action_center, name="action_center"),
]
