from django.urls import path
from app_doctor import views
app_name = "app_doctor"
urlpatterns = [
    
    path('manageappointments/', views.manage_appointments, name='manage_appointments'),
    
    path('complete/<int:id>/', views.complete_appointment, name='complete_appointment'),
    
    path('manage-therapy/', views.manage_therapy_appointments, name='manage_therapy_appointments'),
    path('complete-therapy/<int:id>/', views.complete_therapy_appointment, name='complete_therapy_appointment'),

    path('appointment/<int:app_id>/details/', views.appointment_details, name='appointment_details'),
]
   