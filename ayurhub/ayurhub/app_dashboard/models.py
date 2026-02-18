from django.db import models

from ayurhub.users.models import User

# Create your models here.
# class Patientregi(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name=models.CharField()
#     age=models.CharField()
#     gender=models.CharField()
#     contact=models.CharField()
#     email=models.CharField()
#     address=models.CharField()

class Patientregi(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.CharField(max_length=10)
    gender = models.CharField(max_length=20)
    contact = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
