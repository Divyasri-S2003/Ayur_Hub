from django.db import models

from app_core.models import Doctor
from app_patient.models import DoctorAppointment
from ayurhub.users.models import User

# Create your models here.
class Prescription(models.Model):
    appointment = models.OneToOneField(DoctorAppointment, on_delete=models.CASCADE, related_name='prescription')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    prescription_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)