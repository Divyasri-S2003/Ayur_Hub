from django.urls import path

from app_dashboard import views

app_name = "app_dashboard"

urlpatterns = [
    path("admindashboard/", views.admindashboard),
    path("", views.guestdashboard, name="guestdashboard"),
    path("loginf/", views.loginf, name="loginf"),

    path("patientdashboard/", views.patientdashboard, name="patientdashboard"),
    path("patientregist/", views.patientregist, name="patientregist"),

    path("doctordashboard/", views.doctordashboard, name="doctordashboard"),
    
    path("logout/",views.logout_view,name='logout'),
]
