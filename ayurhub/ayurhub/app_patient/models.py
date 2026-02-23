from django.db import models

from app_core.models import Doctor, Therapy
from ayurhub.users.models import User

# Create your models here.
# class TherapyAppointment(models.Model):
#     therapy=models.ForeignKey(Therapy, on_delete=models.CASCADE,related_name='appointments_therapy')
#     patient=models.ForeignKey(User, on_delete=models.CASCADE,related_name='appointments_patient')
#     appointment_date=models.DateField()
#     created_at=models.DateTimeField(auto_now_add=True)
#     patient_name = models.CharField(max_length=100, null=True, blank=True)
#     patient_age = models.IntegerField(null=True, blank=True)
#     patient_gender = models.CharField(max_length=20, null=True, blank=True)
#     guest_name = models.CharField(max_length=100, blank=True, null=True)
#     guest_age = models.IntegerField(blank=True, null=True)
#     guest_gender = models.CharField(max_length=20, blank=True, null=True)
#     status = models.CharField(max_length=20, default='Pending')
#     capacity = models.PositiveIntegerField(default=5, help_text="Max appointments per day")

class TherapyAppointment(models.Model):
    therapy = models.ForeignKey(Therapy, on_delete=models.CASCADE, related_name='appointments_therapy')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments_patient')
    appointment_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Use CharField for age to match your Patientregi model type
    patient_name = models.CharField(max_length=100, null=True, blank=True)
    patient_age = models.CharField(max_length=10, null=True, blank=True) 
    patient_gender = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=20, default='Pending')
    appointment_time = models.TimeField(null=True, blank=True)  # Optional time field

class DoctorAppointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    status = models.CharField(max_length=20, default="Pending")
    patient_name = models.CharField(max_length=100, null=True, blank=True)
    patient_age = models.IntegerField(null=True, blank=True)
    patient_gender = models.CharField(max_length=20, null=True, blank=True)
    guest_name = models.CharField(max_length=100, blank=True, null=True)
    guest_age = models.IntegerField(blank=True, null=True)
    guest_gender = models.CharField(max_length=20, blank=True, null=True)
    capacity = models.PositiveIntegerField(default=5, help_text="Max appointments per day")
    patient_problems = models.TextField(blank=True, null=True)
    appointment_time = models.TimeField(null=True, blank=True)
    meeting_link = models.URLField(max_length=500, null=True, blank=True)
    
    
class Cart(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('app_core.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
class Booking_Master(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    
class Booking_details(models.Model):
    booking_master = models.ForeignKey(Booking_Master, on_delete=models.CASCADE)
    product = models.ForeignKey('app_core.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
class Payment(models.Model):
    booking_master = models.ForeignKey(Booking_Master, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    therapy=models.ForeignKey(Therapy, on_delete=models.CASCADE, null=True, blank=True)
    payment_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
class deliveryaddress(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100)
    contact=models.CharField(max_length=15,null=True,blank=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    