"""Email templates for OTP verification"""


def otp_email_body(otp_code, username="User"):
    """Generate OTP email body"""
    return f"""
Hi {username},

Welcome to SmartHealth! 💪

Your OTP for email verification is:

{otp_code}

This OTP is valid for 5 minutes only.

If you didn't request this, please ignore this email.

Best regards,
SmartHealth Team
"""


def otp_email_subject():
    """Generate OTP email subject"""
    return "SmartHealth - Email Verification OTP"
