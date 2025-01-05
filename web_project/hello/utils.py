from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(user_email, otp):
    """
    Function to send OTP to the user's email address.
    """
    subject = "Your OTP for Password Reset"
    message = f"Your OTP is {otp}. It is valid for 5 minutes."
    from_email = settings.DEFAULT_FROM_EMAIL  # This can be set in your settings.py
    recipient_list = [user_email]
    
    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        print(f"Error sending email: {e}")
