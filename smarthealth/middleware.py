from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser


class OnboardingRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        # 🔹 Skip anonymous users

        # 🔹 Skip if user has no profile yet (safety)
        profile = getattr(user, "health_profile", None)
        if not profile:
            return self.get_response(request)

        onboarding_url = reverse("action_center")
        logout_url = reverse("logout")

        # 🔹 Allow these paths without redirect
        if request.path.startswith(onboarding_url) or request.path.startswith(logout_url):
            return self.get_response(request)


            # Allow all pages to be visited; views will decide redirects.
            # This keeps incomplete users able to reach action_center first.
        return self.get_response(request)
