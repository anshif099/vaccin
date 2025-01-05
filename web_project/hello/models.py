from django.db import models

# Create your models here.
from django.db import models
from django.utils.timezone import now
import random

class user(models.Model): 
    email = models.CharField(max_length=25, unique=True)
    Password = models.CharField(max_length=10)
    Mobile = models.CharField(max_length=20)
    Dob = models.CharField(max_length=10)
    otp = models.CharField(max_length=6, blank=True, null=True)    
    otp_created_at = models.DateTimeField(blank=True, null=True)

    def generate_otp(self):
        """Generate a 6-digit OTP and save it to the user instance."""
        self.otp = f"{random.randint(100000, 999999)}"
        self.otp_created_at = now()
        self.save()

class admin(models.Model): 
    LgId = models.CharField(max_length=50)

class bok(models.Model):
    center = models.CharField(max_length=50)
    childname = models.CharField(max_length=50)
    cname = models.CharField(max_length=100)
    cdate = models.CharField(max_length=10)
    status = models.CharField(
        max_length=10, 
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], 
        default='Pending'
    )


class vccinUpdate(models.Model): 
    CenterID=models.CharField(max_length=50)
    CN=models.CharField(max_length=50)
    Date=models.CharField(max_length=10)
    DTP=models.CharField(max_length=50)
    HepatitisB=models.CharField(max_length=50)
    Polio=models.CharField(max_length=50)
    Hib=models.CharField(max_length=50)
    Rotavirus=models.CharField(max_length=50)
    PCV=models.CharField(max_length=50)
    Influenza=models.CharField(max_length=50)
    MMR=models.CharField(max_length=50)
    VitaminA=models.CharField(max_length=50)
    Varicella=models.CharField(max_length=50)
    HepatitisA=models.CharField(max_length=50)
    TT=models.CharField(max_length=50)
    HPV=models.CharField(max_length=50)

class approve(models.Model):
    REmail=models.CharField(max_length=50)
    CHName=models.CharField(max_length=50)
    VCD=models.CharField(max_length=50)
    DT=models.CharField(max_length=50)
    UVCN=models.CharField(max_length=50)
    UVD=models.CharField(max_length=50)

class Ufeedback(models.Model):
    FUN=models.CharField(max_length=50)
    Feed=models.CharField(max_length=100)

class Cfeedback(models.Model):
    FCN=models.CharField(max_length=50)
    CFeed=models.CharField(max_length=100)
    