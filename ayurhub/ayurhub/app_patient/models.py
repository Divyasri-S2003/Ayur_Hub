from django.db import models

from app_core.models import Doctor, Therapy
from ayurhub.users.models import User

# Create your models here.
class TherapyAppointment(models.Model):
    therapy=models.ForeignKey(Therapy, on_delete=models.CASCADE,related_name='appointments_therapy')
    patient=models.ForeignKey(User, on_delete=models.CASCADE,related_name='appointments_patient')
    appointment_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)

class DoctorAppointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    status = models.CharField(max_length=20, default="Pending")
    # Add other fields like created_at, symptoms, etc.