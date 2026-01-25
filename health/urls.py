from django.urls import path


from .views import onboarding_view

urlpatterns = [
    path("onboarding/", onboarding_view, name="onboarding"),
]

