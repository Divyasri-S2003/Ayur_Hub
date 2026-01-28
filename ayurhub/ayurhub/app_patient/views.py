
from django.http import HttpResponse
from django.shortcuts import redirect, render

from app_core.models import Category, Doctor, Medicine_Category, Therapy
from app_patient.models import DoctorAppointment, TherapyAppointment
from app_dashboard.models import Patientregi

# Create your views here.
def viewcategory(request):
    c=Category.objects.all()
    return render(request, 'viewcategory.html',{"viewcat":c})

def viewtherapy(request,id):
    t=Therapy.objects.filter(therapyname=id)
    return render(request, 'viewtherapy.html',{"viewthera":t})

def therapydetail(request,id):
    t=Therapy.objects.get(id=id)
    return render(request, 'therapydetail.html',{"therapy":t})

def therapyappoint(request,id):
    if request.method=="POST":
        date=request.POST.get("date")
        therapy=Therapy.objects.get(id=id)
        count=therapy.count
        total_count=TherapyAppointment.objects.filter(appointment_date =date,therapy=id).count()
        if TherapyAppointment.objects.filter(appointment_date =date,therapy=id,patient=request.user).exists():
            return HttpResponse("<script>alert('You have already booked an appointment on this date for this therapy.');window.location='/dashboard/patientdashboard/';</script>")
        if int(total_count) > int(count):
            return HttpResponse("<script>alert('No slots available on this date. Please choose another date.');window.location='/patient/therapyappoint/{{therapy.id}}/';</script>")
        appoint=TherapyAppointment()
        appoint.appointment_date=date
        appoint.therapy=Therapy.objects.get(id=id)
        appoint.patient=request.user
        appoint.save()
        return HttpResponse("<script>alert('Appointment booked successfully');window.location='/dashboard/patientdashboard/';</script>")

    t=Therapy.objects.get(id=id)
    return render(request, 'therapyappoint.html',{"therapy":t}) 


def viewdoctor(request):
    d=Doctor.objects.all()
    return render(request, 'viewdoctor.html',{"vdoc":d})

def viewdocdetails(request,id):
    vd=Doctor.objects.get(id=id)
    return render(request, 'viewdocdetails.html',{"docdetails":vd})


def doctorappoint(request, id):
    # 1. Fetch the specific doctor
    doc = Doctor.objects.get(id=id)
    
    # 2. Fetch the patient profile linked to the logged-in user
    # This is necessary to get the 'age' field
    try:
        patient_profile = Patientregi.objects.get(user=request.user)
    except Patientregi.DoesNotExist:
        patient_profile = None

    if request.method == "POST":
        selected_date = request.POST.get("date")
        # ... validation logic ...
        appoint = DoctorAppointment(
            doctor=doc,
            patient=request.user,
            appointment_date=selected_date,
            status="Pending"
        )
        appoint.save()
        return HttpResponse("<script>alert('Booked');window.location='/dashboard/patientdashboard/';</script>")

    # 3. PASS BOTH OBJECTS TO THE TEMPLATE
    return render(request, 'doctorappoint.html', {
        "doctor": doc,           # Used for {{ doctor.user.name }}
        "patient": patient_profile # Used for {{ patient.age }}
    })
    
def viewmedcategory(request):
    mc=Medicine_Category.objects.all()
    return render(request, 'viewmedcategory.html',{"medcat":mc})

def vproduct(request,id):
    p=Medicine_Category.objects.get(id=id)
    prod= p.product_set.all()
    return render(request, 'vproduct.html',{"vprod":prod})