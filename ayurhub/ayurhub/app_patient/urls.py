from django.urls import path
from app_patient import views
app_name="app_patient"
urlpatterns = [
    path("viewcategory/",views.viewcategory,name='viewcategory'),
    path("viewtherapy/<int:id>/",views.viewtherapy,name='viewtherapy'),
    path("therapydetail/<int:id>/",views.therapydetail,name='therapydetail'),
    path("therapyappoint/<int:id>/",views.therapyappoint,name='therapyappoint'),
    
    path("viewdoctor/",views.viewdoctor,name='viewdoctor'),
    path("viewdocdetails/<int:id>/",views.viewdocdetails,name='viewdocdetails'),
    path("doctorappoint/<int:id>/", views.doctorappoint, name='doctorappoint'),
    
    path("viewmedcategory/",views.viewmedcategory,name='viewmedcategory'),
    path("vproduct/<int:id>/",views.vproduct,name='vproduct'),
    
]

