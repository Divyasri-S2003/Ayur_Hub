from django.db import models

from ayurhub.users.models import User

# Create your models here.
class District(models.Model):
    name = models.CharField(max_length=100)


class Location(models.Model):
    name = models.CharField(max_length=100)
    dis = models.ForeignKey(District, on_delete=models.CASCADE)


class Category(models.Model):
    name=models.CharField()
    description=models.CharField(max_length=20,null=True,blank=True)
    img=models.ImageField(upload_to="media/",null=True,blank=True)

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=255, null=True, blank=True)
    contact=models.CharField()
    specialization=models.CharField()
    qualification=models.CharField(null=True)
    schedule=models.CharField()
    experience=models.CharField(null=True)
    fee=models.CharField(null=True,blank=True)
    img=models.ImageField(upload_to="media/",null=True,blank=True)
    mode=models.CharField(max_length=50,null=True,blank=True)
    about=models.TextField(null=True,blank=True)


class Therapy(models.Model):
    therapyname=models.ForeignKey(Category,on_delete=models.CASCADE)  # model kodknath oke field name ann and views kodknath variable name
   
    servicename=models.CharField(max_length=100)
    shortdescription=models.CharField(max_length=200,null=True,blank=True)
    description=models.TextField()
    img=models.ImageField(upload_to="media/",null=True,blank=True)
    duration=models.CharField(max_length=50)
    price=models.CharField(max_length=50)
    benefits=models.TextField(null=True)
    productused=models.CharField(null=True,blank=True,max_length=100)
    count=models.CharField(null=True,blank=True,max_length=50)



class Medicine_Category(models.Model):
    name=models.CharField(max_length=100)
    img=models.ImageField(upload_to="media/",null=True,blank=True)
    
    
class Product(models.Model):
    medicinecategory=models.ForeignKey(Medicine_Category,on_delete=models.CASCADE)
    productname=models.CharField(max_length=100)
    description=models.TextField()
    img=models.ImageField(upload_to="media/",null=True,blank=True)
    price=models.CharField(max_length=50)
    quantity=models.CharField(max_length=50)
    
    