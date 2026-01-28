from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login


from app_dashboard.models import Patientregi
from ayurhub.users.models import User

# Create your views here.
def admindashboard(request):
    return render(request, "Admintemplate.html")

def guestdashboard(request):
    return render(request, "Guesttemplate.html")


def loginf (request):
    if request.method=='POST':
        Username= request.POST.get('username')
        Password= request.POST.get('password') 

        user=authenticate(request, username=Username, password=Password)
        if user is not None:
            login(request, user)
            if user.role=='Patient':
                return HttpResponse("<script>alert('Login Successful');window.location='/dashboard/patientdashboard/';</script>")
            elif user.role=='Doctor':
                return HttpResponse("<script>alert('Login Successful');window.location='/dashboard/doctordashboard/';</script>")
            elif user.role == 'Admin':
                return HttpResponse("<script>alert('Login Successful');window.location='/dashboard/admindashboard/';</script>")
        else:
            return HttpResponse("<script>alert('Login Failed');window.location='/dashboard/loginf/';</script>")        

    else:
        return render(request,"login.html")





def patientdashboard(request):
    return render(request, "Patienttemplate.html")
    
def patientregist(request):
    if request.method=='POST':
        name=request.POST.get('name')
        age=request.POST.get('age')
        gender=request.POST.get('gender')
        contact=request.POST.get('contact')
        email=request.POST.get('email')
        address=request.POST.get('address') 
        username=request.POST.get('username')
        password=request.POST.get('password')

        if not username or not password:
            return HttpResponse("<script>alert('Welcome to AyurHub');window.location='/dashboard/patientdashboard/';</script>")
        if User.objects.filter(username = username,email=email ).exists():
            return HttpResponse("<script>alert('User Already Exist');window.location='/dashboard/patientregist/';</script>")
        user=User()
        user.name=name
        user.email=email
        user.username=username
        user.set_password(password)
        user.role='Patient'
        user.save()

        Patientregi.objects.create(user=user,age=age,gender=gender,contact=contact,address=address)
        return HttpResponse("<script>alert('Patient Registered Successfully');window.location='/dashboard/loginf/';</script>")
    else:   
        return render(request,"PatientRegistration.html")


    

def doctordashboard(request):
    return render(request, "Doctortemplate.html")


