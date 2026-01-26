import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from planner.models import UserPlanStatus, GeneratedPlan
from health.models import HealthProfile

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        profile = HealthProfile.objects.filter(user=request.user).first()
        if profile and profile.onboarding_completed:
            return redirect('dashboard')
        else:
            return redirect('action_center')
    return render(request, 'index.html')



def register_view(request):
    if request.method == "POST":
        user_name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if not user_name:
            messages.error(request, "Username is required")
            return redirect('register')
        # 1️⃣ Empty fields
        if not email or not password or not confirm_password:
            messages.error(request, "All fields are required")
            return redirect('register')

        # 2️⃣ Email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.error(request, "Enter a valid email address")
            return redirect('register')

        # 3️⃣ Password length
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters")
            return redirect('register')

        # 4️⃣ User already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')
        # 5️⃣ Create user
        user = User.objects.create_user(
        username=user_name,
        email=email,
        password=password
        )

        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')

    return render(request, 'register.html')




def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        # 1️⃣ Empty fields
        if not email or not password:
            messages.error(request, "Email and password are required")
            return redirect('login')

        # 2️⃣ Look up by email then authenticate with username
        user_by_email = User.objects.filter(email=email).first()
        if not user_by_email:
            messages.error(request, "Invalid email or password")
            return redirect('login')

        user = authenticate(username=user_by_email.username, password=password)
        if user is None:
            messages.error(request, "Invalid email or password")
            return redirect('login')

        login(request, user)

        profile = HealthProfile.objects.filter(user=user).first()
        plan = GeneratedPlan.objects.filter(user=user).first()

        # Desired flow:
        # - If profile completed and plan exists -> dashboard
        # - If profile completed and no plan -> action_center
        # - If profile not completed -> action_center (buttons will redirect to onboarding before API)
        if profile and profile.onboarding_completed:
            if plan:
                return redirect('dashboard')
            return redirect('action_center')
        else:
            return redirect('action_center')
        

    return render(request, 'login.html')



@login_required
def action_center(request):
    return render(request, "action_center.html")
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
