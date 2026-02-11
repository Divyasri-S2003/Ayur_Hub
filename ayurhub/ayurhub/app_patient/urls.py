from django.urls import path
from app_patient import views
app_name="app_patient"
urlpatterns = [
    path("viewcategory/",views.viewcategory,name='viewcategory'),
    path("viewtherapy/<int:id>/",views.viewtherapy,name='viewtherapy'),
    path("therapydetail/<int:id>/",views.therapydetail,name='therapydetail'),
    
    path("therapyappoint/<int:id>/", views.therapyappoint, name='therapyappoint'),
    
    path("viewdoctor/",views.viewdoctor,name='viewdoctor'),
    path("viewdocdetails/<int:id>/",views.viewdocdetails,name='viewdocdetails'),
    path("doctorappoint/<int:id>/", views.doctorappoint, name='doctorappoint'),
    
    path("viewmedcategory/",views.viewmedcategory,name='viewmedcategory'),
    path("vproduct/<int:id>/",views.vproduct,name='vproduct'),
    path("vprodetails/<int:id>/",views.vprodetails,name='vprodetails'),
    
    path("add_to_cart/<int:id>/",views.add_to_cart,name='addtocart'),
    path("viewcart/",views.view_cart,name='viewcart'),
    path("updatecart/<int:item_id>/<str:action>/", views.update_cart, name='updatecart'),
    path("removefromcart/<int:item_id>/", views.remove_from_cart, name='removefromcart'),
    path("checkout/",views.delivery_address,name='checkout'),
    
    path('delivery-address/', views.delivery_address, name='delivery_address'),
    path('payment-review/', views.payment_page, name='payment_page'),
    path('process-payment/', views.process_payment, name='process_payment'),
    
    path('final-page/<int:booking_id>/', views.final_page, name='final_page'),
]

