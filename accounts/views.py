import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

from planner.models import UserPlanStatus, GeneratedPlan
from health.models import HealthProfile
from accounts.models import OTPVerification
from accounts.email_templates import otp_email_body, otp_email_subject

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
    """Step 1: User enters email and basic details, OTP is sent"""
    if request.method == "POST":
        user_name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validation
        if not user_name:
            messages.error(request, "Username is required")
            return redirect('register')
        
        if not email or not password or not confirm_password:
            messages.error(request, "All fields are required")
            return redirect('register')

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.error(request, "Enter a valid email address")
            return redirect('register')

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters")
            return redirect('register')

        if User.objects.filter(username=user_name).exists():
            messages.error(request, "Username already registered")
            return redirect('register')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')
        
        # ✅ Generate & Send OTP
        otp_record, created = OTPVerification.objects.get_or_create(email=email)
        otp_record.otp = OTPVerification.generate_otp()
        otp_record.username = user_name
        otp_record.password = password
        otp_record.is_verified = False
        otp_record.save()
        
        # Send email
        try:
            send_mail(
                subject=otp_email_subject(),
                message=otp_email_body(otp_record.otp, user_name),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, f"OTP sent to {email}. Please check your inbox.")
            return redirect(f'/accounts/verify-otp/?emailId={email}')     
        except Exception as e:
            messages.error(request, f"Failed to send OTP: {str(e)}")
            return redirect('register')

    return render(request, 'register.html')


def verify_otp_view(request):
    """Step 2: User enters OTP and completes registration"""
    email = request.GET.get('emailId')
    
    if not email:
        messages.error(request, "Invalid request")
        return redirect('register')
    
    # Check if OTP record exists
    try:
        otp_record = OTPVerification.objects.get(email=email)
    except OTPVerification.DoesNotExist:
        messages.error(request, "OTP session expired. Please register again.")
        return redirect('register')
    
    if request.method == "POST":
        otp_input = request.POST.get('otp')
        
        if not otp_input:
            messages.error(request, "Please enter OTP")
            return render(request, 'verify_otp.html', {'email': email})
        
        # Check OTP
        if otp_record.is_expired():
            otp_record.delete()
            messages.error(request, "OTP expired. Please register again.")
            return redirect('register')
        
        if otp_input != otp_record.otp:
            messages.error(request, "Invalid OTP")
            return render(request, 'verify_otp.html', {'email': email})
        
        # ✅ OTP verified - Create user
        try:
            user = User.objects.create_user(
                username=otp_record.username,
                email=email,
                password=otp_record.password
            )
            otp_record.is_verified = True
            otp_record.save()
            
            messages.success(request, "Email verified! Please login with your credentials.")
            otp_record.delete()  # Clean up OTP record
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Registration failed: {str(e)}")
            return render(request, 'verify_otp.html', {'email': email})
    
    return render(request, 'verify_otp.html', {'email': email})


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
            else:
                return redirect('action_center')
        else:
            return redirect('action_center')

    return render(request, 'login.html')


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    # After logout, redirect to homepage or login page                 
    return redirect('login')


@login_required
def action_center(request):
    return render(request, "action_center.html")
