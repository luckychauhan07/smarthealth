from django.db import models
from django.utils import timezone
from datetime import timedelta
import random
import string


class OTPVerification(models.Model):
    """Temporary OTP storage for email verification during registration"""
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=4)
    username = models.CharField(max_length=150, blank=True)
    password = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'accounts_otpverification'
    
    @staticmethod
    def generate_otp():
        """Generate 4-digit OTP"""
        return ''.join(random.choices(string.digits, k=4))
    
    def is_expired(self):
        """Check if OTP expired (5 minutes)"""
        return timezone.now() > self.created_at + timedelta(minutes=5)
    
    def __str__(self):
        return f"OTP for {self.email}"
