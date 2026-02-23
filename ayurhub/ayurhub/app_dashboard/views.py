from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout


from app_dashboard.models import Patientregi
from ayurhub.users.models import User

# Create your views here.
@never_cache
@login_required(login_url='/loginf/')
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
                return HttpResponse("<script>alert('Login Successful');window.location='/patientdashboard/';</script>")
            elif user.role=='Doctor':
                return HttpResponse("<script>alert('Login Successful');window.location='/doctordashboard/';</script>")
            elif user.role == 'Admin':
                return HttpResponse("<script>alert('Login Successful');window.location='/admindashboard/';</script>")
        else:
            return HttpResponse("<script>alert('Login Failed');window.location='/loginf/';</script>")        

    else:
        return render(request,"login.html")




@never_cache
@login_required(login_url='/loginf/')
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
            return HttpResponse("<script>alert('Welcome to AyurHub');window.location='/patientdashboard/';</script>")
        if User.objects.filter(username = username,email=email ).exists():
            return HttpResponse("<script>alert('User Already Exist');window.location='/patientregist/';</script>")
        user=User()
        user.name=name
        user.email=email
        user.username=username
        user.set_password(password)
        user.role='Patient'
        user.save()

        Patientregi.objects.create(user=user,age=age,gender=gender,contact=contact,address=address)
        send_mail(
        subject="Welcome to Our Platform",
        message=f"Hi {name},\n\nYour account has been successfully created.",
        from_email=None,  
        recipient_list=[email],
    )
        return HttpResponse("<script>alert('Patient Registered Successfully');window.location='/loginf/';</script>")
    else:   
        return render(request,"PatientRegistration.html")


    
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app_patient.models import DoctorAppointment, TherapyAppointment
from app_core.models import Doctor

@login_required(login_url='login')
@never_cache
@login_required(login_url='/loginf/')
def doctordashboard(request):
    try:
        doctor_profile = request.user.doctor
    except AttributeError:
        return redirect('index') 

    # 1. Fetch Doctor Appointments
    appointments = DoctorAppointment.objects.filter(doctor=doctor_profile).order_by('-appointment_date')
    
    # 2. Apply Date Filter if present
    search_date = request.GET.get('search_date')
    if search_date:
        appointments = appointments.filter(appointment_date=search_date)

    # 3. Therapy Logic (BPT Qualification Check)
    therapy_appointments = TherapyAppointment.objects.none() 
    is_therapy_admin = False 

    if doctor_profile.qualification == 'BPT':
        is_therapy_admin = True
        therapy_appointments = TherapyAppointment.objects.all().order_by('-appointment_date')
        if search_date:
            therapy_appointments = therapy_appointments.filter(appointment_date=search_date)

    # ---------------------------------------------------------
    # 4. STATS LOGIC (THE FIX)
    # ---------------------------------------------------------
    
    # We use __icontains to be extra safe against hidden spaces or case issues
    pending_doc = appointments.filter(status__icontains="Pending").count()
    
    pending_therapy = 0
    if is_therapy_admin:
        pending_therapy = therapy_appointments.filter(status__icontains="Pending").count()

    # Red Card: Total Pending Actions (Doctor + Therapy)
    pending_count = pending_doc + pending_therapy

    # Middle Card: Total Visits (Completed Appointments)
    completed_doc = appointments.filter(status__icontains="Completed").count()
    completed_therapy = 0
    if is_therapy_admin:
        completed_therapy = therapy_appointments.filter(status__icontains="Completed").count()
    
    completed_count = completed_doc + completed_therapy

    # First Card: Appointments List (Total count shown in the table)
    list_count = appointments.count()

    context = {
        'doctor': doctor_profile,
        'appointments': appointments,
        'therapy_appointments': therapy_appointments, 
        'is_therapy_admin': is_therapy_admin,         
        'search_date': search_date,
        'total_count': completed_count, # Matches "Total Visits" label
        'pending_count': pending_count, # Matches "Pending Actions" label
        'list_count': list_count,       # Matches "Appointments List" label
    }

    return render(request, "Doctortemplate.html", context)


def logout_view(request):
    logout(request)
    return HttpResponse(
        "<script>alert('Logged out successfully');window.location='/loginf/';</script>"
    )
    
    