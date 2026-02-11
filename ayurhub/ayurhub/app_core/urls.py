from django.urls import path
from app_core import views

app_name="core"
urlpatterns = [
    path("dist/",views.dist,name='dist'),  
    path("viewdis/",views.viewdis,name='viewdis'),
    path("deletedist/<int:id>/",views.deletedist,name='deletedist'),
    path("editdis/<int:id>/",views.editdis,name='editdis'),


    path("location/",views.location,name='location'),
    path("viewloc/",views.viewloc,name='viewloc'),
    path("deleteloc/<int:id>/",views.deleteloc,name='deleteloc'),
    path("locationup/<int:id>/", views.locationup, name="locationup"),


    path("category/",views.category,name='category'),
    path("viewcat/",views.viewcat,name='viewcat'),
    path("deletecat/<int:name>", views.deletecat, name="deletecat"),
    path("editcat/<int:name>/", views.cateup, name="editcat"),

    path("doctor/",views.doctor,name='doctor'),
    path("viewdoc/",views.viewdoc,name='viewdoc'),

    path("viewpatient/",views.viewpatient,name='viewpatient'),

    path("therapies/",views.therapies,name='therapies'),
    path("viewtherapies/",views.viewtherapies,name='viewtherapies'),
    path("deletetherapy/<int:id>/",views.deletetherapy,name='deletetherapy'),
    path("edittherapy/<int:id>/", views.edittherapy, name="edittherapy"),
    
    path("medicinecategory/",views.medicinecategory,name='medicinecategory'),
    path("viewmedicat/",views.viewmedicinecat,name='viewmedicat'),
    path("deletemedicat/<int:id>/",views.delmedicinecat,name='deletemedicat'),
    path("editmedicat/<int:id>/", views.editmedicinecat, name="editmedicat"),
    
    path("product/",views.product,name='product'),
    path("viewproduct/",views.viewproduct,name='viewproduct'),
    path("deletproduct/<int:id>/",views.deletproduct,name='deletproduct'),
    path("editproduct/<int:id>/", views.editproduct, name="editproduct"),
    
    path('viewappointments/', views.view_appointments, name='view_appointments'),
    path('doctorschedule/', views.view_doctor_schedule, name='view_doctor_schedule'),


   


    

  
    ]