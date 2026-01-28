from django.db import models

from ayurhub.users.models import User

# Create your models here.
class Patientregi(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    name=models.CharField()
    age=models.CharField()
    gender=models.CharField()
    contact=models.CharField()
    email=models.CharField()
    address=models.CharField()
