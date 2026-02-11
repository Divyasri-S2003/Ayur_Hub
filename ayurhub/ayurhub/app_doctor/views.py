from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app_patient.models import DoctorAppointment
# Import your specific Patient profile model if needed
# from app_patient.models import PatientProfile 

@login_required
def manage_appointments(request):
    # 1. Get appointments for the logged-in doctor
    try:
        current_doctor = request.user.doctor 
        appointments = DoctorAppointment.objects.filter(doctor=current_doctor)
    except AttributeError:
        # Fallback if the user is not a doctor
        appointments = DoctorAppointment.objects.all()

    # 2. Date Filtering
    selected_date = request.GET.get('search_date')
    if selected_date:
        appointments = appointments.filter(appointment_date=selected_date)

    # 3. Ordering (Newest first)
    appointments = appointments.order_by('-appointment_date')

    context = {
        'appointments': appointments,
        'search_date': selected_date
    }
    return render(request, 'manageappoint.html', context)

@login_required
def complete_appointment(request, id):
    try:
        appointment = DoctorAppointment.objects.get(id=id)
        # Update status to "Completed" (String)
        appointment.status = "Completed"
        appointment.save()
    except DoctorAppointment.DoesNotExist:
        pass
    
    return redirect('app_doctor:manage_appointments')



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app_patient.models import TherapyAppointment

# ---------------------------------------------------------
# RENAME THIS FUNCTION TO MATCH YOUR URLS.PY
# ---------------------------------------------------------
@login_required
def manage_therapy_appointments(request):   # <--- This was likely named 'manage_appointments' before
    
    # 1. Get all therapy appointments (Newest first)
    appointments = TherapyAppointment.objects.all().order_by('-appointment_date')

    # 2. Date Filtering
    selected_date = request.GET.get('search_date')
    if selected_date:
        appointments = appointments.filter(appointment_date=selected_date)

    context = {
        'therapy_appointments': appointments,
        'search_date': selected_date
    }
    
    # 3. Render the template
    return render(request, 'therapy_appointment_manage.html', context)


@login_required
def complete_therapy_appointment(request, id):
    appointment = get_object_or_404(TherapyAppointment, id=id)
    appointment.status = "Completed"
    appointment.save()
    messages.success(request, "Therapy session marked as completed.")
    
    # Redirect back to the dashboard so they can see the change immediately
    return redirect('app_doctor:doctordashboard')


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from app_core.models import  Doctor, User # Adjust imports based on your app names
from .models import Prescription 

def appointment_details(request, app_id):
    # Fetch the specific appointment
    appointment = get_object_or_404(DoctorAppointment, id=app_id)
    
    # Get the logged-in doctor
    doctor = get_object_or_404(Doctor, user=request.user) 

    # Fetch previous prescriptions for this patient (excluding the current appointment if it already has one)
    previous_prescriptions = Prescription.objects.filter(
        patient=appointment.patient
    ).exclude(appointment=appointment).order_by('-created_at')

    # Handle form submission for new prescription
    if request.method == 'POST':
        prescription_text = request.POST.get('prescription_text')
        if prescription_text:
            Prescription.objects.create(
                appointment=appointment,
                doctor=doctor,
                patient=appointment.patient,
                prescription_text=prescription_text
            )
            messages.success(request, "Prescription saved successfully.")
            return redirect('app_doctor:appointment_details', app_id=app_id)

    context = {
        'appointment': appointment,
        'previous_prescriptions': previous_prescriptions,
    }
    return render(request, 'appointment_details.html', context)