
from datetime import date
from django.http import HttpResponse
from django.shortcuts import redirect, render

from app_core.models import Category, Doctor, Medicine_Category, Product, Therapy
from app_patient.models import Booking_Master, Booking_details, Cart, DoctorAppointment, Payment, TherapyAppointment
from app_dashboard.models import Patientregi
from django.contrib import messages  # Add this line

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

# def therapyappoint(request,id):
#     if request.method=="POST":
#         date=request.POST.get("date")
#         therapy=Therapy.objects.get(id=id)
#         count=therapy.count
#         total_count=TherapyAppointment.objects.filter(appointment_date =date,therapy=id).count()
#         if TherapyAppointment.objects.filter(appointment_date =date,therapy=id,patient=request.user).exists():
#             return HttpResponse("<script>alert('You have already booked an appointment on this date for this therapy.');window.location='/dashboard/patientdashboard/';</script>")
#         if int(total_count) > int(count):
#             return HttpResponse("<script>alert('No slots available on this date. Please choose another date.');window.location='/patient/therapyappoint/{{therapy.id}}/';</script>")
#         appoint=TherapyAppointment()
#         appoint.appointment_date=date
#         appoint.therapy=Therapy.objects.get(id=id)
#         appoint.patient=request.user
#         appoint.save()
#         return HttpResponse("<script>alert('Appointment booked successfully');window.location='/dashboard/patientdashboard/';</script>")

#     t=Therapy.objects.get(id=id)
#     return render(request, 'therapyappoint.html',{"therapy":t}) 

def therapyappoint(request, id):
    therapy = Therapy.objects.get(id=id)

    if request.method == "POST":
        date = request.POST.get("date")
        booking_for = request.POST.get("booking_for") # Will be 'self' or 'other'

        # 1. Availability Check
        # Convert total capacity to int to be safe
        capacity = int(therapy.count) 
        
        # Check how many appointments exist for this specific therapy on this date
        booked_count = TherapyAppointment.objects.filter(appointment_date=date, therapy=therapy).count()
        
        if booked_count >= capacity:
             return HttpResponse(f"<script>alert('No slots available on {date}.');window.history.back();</script>")

        # 2. Determine Patient Details (Snapshot)
        p_name = ""
        p_age = ""
        p_gender = ""

        if booking_for == "self":
            # CASE A: Booking for Self - Fetch from Patientregi
            # We use filter().first() to avoid crashes if profile doesn't exist
            profile = Patientregi.objects.filter(user=request.user).first()
            
            if profile:
                p_name = profile.name
                p_age = profile.age
                p_gender = profile.gender
            else:
                # Fallback if user hasn't completed profile
                p_name = request.user.first_name if request.user.first_name else request.user.username
                p_age = "N/A"
                p_gender = "N/A"
                
        else:
            # CASE B: Booking for Guest - Fetch from Form Inputs
            p_name = request.POST.get("other_name")
            p_age = request.POST.get("other_age")
            p_gender = request.POST.get("other_gender")

        # 3. Duplicate Check (Prevent double booking for same person on same day)
        if TherapyAppointment.objects.filter(appointment_date=date, therapy=therapy, patient=request.user, patient_name=p_name).exists():
             return HttpResponse(f"<script>alert('You have already booked for {p_name} on this date.');window.location='/dashboard/patientdashboard/';</script>")

        # 4. Save Appointment
        appoint = TherapyAppointment()
        appoint.appointment_date = date
        appoint.therapy = therapy
        appoint.patient = request.user
        
        # Save the snapshot details we determined above
        appoint.patient_name = p_name
        appoint.patient_age = p_age
        appoint.patient_gender = p_gender
        
        appoint.save()
        
        return HttpResponse("<script>alert('Appointment booked successfully');window.location='/dashboard/patientdashboard/';</script>")

    return render(request, 'therapyappoint.html', {"therapy": therapy})



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
    try:
        patient_profile = Patientregi.objects.get(user=request.user)
    except Patientregi.DoesNotExist:
        patient_profile = None

    if request.method == "POST":
        selected_date = request.POST.get("date")
        
        # --- NEW CODE: Fetch Guest Details from the form ---
        # If the user selected "Myself", these will be empty (None), which is fine.
        guest_name_input = request.POST.get("guest_name")
        guest_age_input = request.POST.get("guest_age")
        guest_gender_input = request.POST.get("guest_gender")

        # Create the appointment object including the guest fields
        appoint = DoctorAppointment(
            doctor=doc,
            patient=request.user,
            appointment_date=selected_date,
            status="Pending",
            
            # --- Save the Guest Data here ---
            guest_name=guest_name_input,
            guest_age=guest_age_input,
            guest_gender=guest_gender_input
        )
        
        appoint.save()
        return HttpResponse("<script>alert('Booked successfully!');window.location='/dashboard/patientdashboard/';</script>")

    return render(request, 'doctorappoint.html', {
        "doctor": doc, 
        "patient": patient_profile
    })
    
def viewmedcategory(request):
    mc=Medicine_Category.objects.all()
    return render(request, 'viewmedcategory.html',{"medcat":mc})

def vproduct(request,id):
    p=Medicine_Category.objects.get(id=id)
    prod= p.product_set.all()
    return render(request, 'vproduct.html',{"vprod":prod})

def vprodetails(request,id):
    pd=Product.objects.get(id=id)
    return render(request, 'vproductdetails.html',{"prodetails":pd})




from django.contrib import messages

def add_to_cart(request, id):
    if not request.user.is_authenticated:
        return redirect('loginf') 

    product = Product.objects.get(id=id)

    # Convert the product's quantity string to an integer
    # We use a try/except block just in case the field is empty or contains non-numbers
    try:
        available_stock = int(product.quantity)
    except (ValueError, TypeError):
        available_stock = 0

    # 1. Check if the product is out of stock
    if available_stock <= 0:
        messages.error(request, f"Sorry, {product.productname} is currently out of stock.")
        return redirect(request.META.get('HTTP_REFERER', 'app_patient:viewmedcategory'))
    
    # Get or create the cart item
    cart_item, created = Cart.objects.get_or_create(
        patient=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        # Convert cart_item.quantity to int as well to ensure safe comparison
        current_cart_qty = int(cart_item.quantity)
        
        # 2. Check if adding another exceeds available stock
        if current_cart_qty + 1 > available_stock:
            messages.warning(request, f"Only {available_stock} units available in stock.")
        else:
            cart_item.quantity = current_cart_qty + 1
            cart_item.save()

    return redirect(request.META.get('HTTP_REFERER', 'app_patient:viewmedcategory'))

def view_cart(request):
    if not request.user.is_authenticated:
        return redirect('loginf') 
    
    cart_items = Cart.objects.filter(patient=request.user)
    total = 0
    
    for item in cart_items:
        # Convert both to float/int to be absolutely safe
        try:
            price = float(item.product.price)
            qty = int(item.quantity)
            item.subtotal = price * qty
            total += item.subtotal
        except (ValueError, TypeError):
            item.subtotal = 0
        
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
    })





    
def update_cart(request, item_id, action):
    cart_item = Cart.objects.get(id=item_id)
    current_qty = int(cart_item.quantity)
    
    # Safely convert product stock to an integer
    try:
        available_stock = int(cart_item.product.quantity)
    except (ValueError, TypeError):
        available_stock = 0

    if action == 'increment':
        # Check if we have enough stock before incrementing
        if current_qty < available_stock:
            cart_item.quantity = current_qty + 1
            cart_item.save()
        else:
            # Trigger the alert message
            messages.warning(request, f"Cannot add more. Only {available_stock} units available.")
            
    elif action == 'decrement':
        if current_qty > 1:
            cart_item.quantity = current_qty - 1
            cart_item.save()
        else:
            cart_item.delete()
            
    return redirect('app_patient:viewcart')


def remove_from_cart(request, item_id):
    cart_item = Cart.objects.get(id=item_id)
    cart_item.delete()
    return redirect('app_patient:viewcart')






from django.shortcuts import render, redirect # Added redirect
from django.http import HttpResponse
from .models import Cart, Booking_Master, Booking_details, Payment, deliveryaddress
from app_core.models import Product 
from datetime import date
# def delivery_address(request):
#     if request.method=="POST":
#         address_line=request.POST.get("address")
#         city=request.POST.get("city")
#         state=request.POST.get("state")
#         postal_code = request.POST.get('postal_code')
#         country=request.POST.get("country")
#         name=request.POST.get("name")
#         contact=request.POST.get("contact")
#         addr=deliveryaddress()
#         addr.patient=request.user
#         addr.address_line1=address_line
#         addr.city=city
#         addr.state=state
#         addr.postal_code=postal_code
#         addr.country=country
#         addr.name=name
#         addr.contact=contact
#         addr.save()
#         return HttpResponse("<script>alert('Address added successfully');window.location='/patient/payment/cart';</script>")
#     return render(request, 'delivery_details.html')


def delivery_address(request):
    if request.method == "POST":
        # Create and save the address
        addr = deliveryaddress()
        addr.patient = request.user
        addr.name = request.POST.get("name")
        addr.contact = request.POST.get("contact")
        addr.address_line1 = request.POST.get("address")
        addr.country = request.POST.get("country")
        addr.state = request.POST.get("state")
        addr.city = request.POST.get("city")
        addr.postal_code = request.POST.get("postal_code")
        addr.save()
        
        # Redirect to the Review/Payment page
        return redirect('app_patient:payment_page')

    return render(request, 'delivery_details.html')


# def payment(request, source):
#     cart_items = []
#     total_amount = 0
    
#     if source == "cart":
#         cart_items = Cart.objects.filter(patient=request.user)
#         for item in cart_items:
#             item.subtotal = float(item.product.price) * int(item.quantity)
#         total_amount = sum(item.subtotal for item in cart_items)

#     if request.method == "POST":
#         payment_method = request.POST.get("payment_method")
        
#         if source == "cart":
#             # 1. Stock Check
#             for item in cart_items:
#                 if int(item.product.quantity) < int(item.quantity):
#                     return HttpResponse(f"<script>alert('Sorry, {item.product.productname} is out of stock!');history.back();</script>")

#             # 2. Create Master record
#             booking_master = Booking_Master.objects.create(
#                 patient=request.user,
#                 booking_date=date.today(),
#                 total_amount=total_amount
#             )
            
#             # 3. Process Details and Update Stock
#             booking_details_list = []
#             for item in cart_items:
#                 product = item.product
#                 product.quantity = int(product.quantity) - int(item.quantity)
#                 product.save()

#                 booking_details_list.append(Booking_details(
#                     booking_master=booking_master,
#                     product=product,
#                     quantity=item.quantity,
#                     price=float(product.price)
#                 ))
#             Booking_details.objects.bulk_create(booking_details_list)
            
#             # 4. Create Payment record
#             Payment.objects.create(
#                 booking_master=booking_master,
#                 amount=total_amount,
#                 payment_method=payment_method
#             )
            
#             # 5. Clear Cart
#             cart_items.delete()
            
#             # 6. REDIRECT to final page with the booking ID
#             return redirect('app_patient:final_page', booking_id=booking_master.id)

#     return render(request, 'payment.html', {
#         "source": source,
#         "cart_items": cart_items,
#         "total": total_amount
#     })

def payment_page(request):
    # Fetch Cart Items
    cart_items = Cart.objects.filter(patient=request.user)
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('app_patient:viewcart') # Or wherever your product list is

    # Calculate Totals
    total_amount = 0
    for item in cart_items:
        item.subtotal = int(item.product.price) * int(item.quantity)
        total_amount += item.subtotal

    # Fetch the Address to display
    address = deliveryaddress.objects.filter(patient=request.user).last()

    context = {
        'cart_items': cart_items,
        'total': total_amount,
        'address': address
    }
    return render(request, 'payment.html', context)


def process_payment(request):
    if request.method == "POST":
        cart_items = Cart.objects.filter(patient=request.user)
        
        if not cart_items.exists():
            return redirect('app_patient:payment_page')

        # Calculate Total
        total_amount = sum(int(item.product.price) * int(item.quantity) for item in cart_items)

        # A. Stock Check Validation
        for item in cart_items:
            if int(item.product.quantity) < int(item.quantity):
                messages.error(request, f"Sorry, {item.product.productname} is out of stock or requested quantity is too high.")
                return redirect('app_patient:payment_page')

        # B. Create Booking Master
        booking = Booking_Master.objects.create(
            patient=request.user,
            booking_date=date.today(),
            total_amount=total_amount
            # If you added the foreign key I suggested earlier:
            # delivery_address=deliveryaddress.objects.filter(patient=request.user).last() 
        )

        # C. Create Details & Reduce Stock
        booking_details_list = []
        for item in cart_items:
            # Reduce Stock
            product = item.product
            product.quantity = int(product.quantity) - int(item.quantity)
            product.save()

            # Prepare Booking Detail
            booking_details_list.append(Booking_details(
                booking_master=booking,
                product=product,
                quantity=item.quantity,
                price=product.price
            ))
        
        # Bulk create for performance
        Booking_details.objects.bulk_create(booking_details_list)

        # D. Create Payment Record
        Payment.objects.create(
            booking_master=booking,
            amount=total_amount,
            payment_method="Card/Online", # Or request.POST.get('payment_method')
        )

        # E. Clear Cart
        cart_items.delete()

        # F. Redirect to Success Page
        return redirect('app_patient:final_page', booking_id=booking.id)

    # If someone tries to access this URL via GET, send them back
    return redirect('app_patient:payment_page')


def final_page(request, booking_id):
    # 1. Fetch the booking
    try:
        booking = Booking_Master.objects.get(id=booking_id)
    except Booking_Master.DoesNotExist:
        return HttpResponse("Booking not found")

    items = Booking_details.objects.filter(booking_master=booking)

    # --- THE FIX ---
    # Instead of filtering by user, we just grab the MOST RECENT address added to the database.
    # This guarantees something will show if your database has data.
    address = deliveryaddress.objects.last() 
    # ---------------

    last_doc = DoctorAppointment.objects.filter(patient=request.user).last()
    last_therapy = TherapyAppointment.objects.filter(patient=request.user).last()

    context = {
        'items': items,       
        'payment': booking,   
        'address': address,   
        'last_doc': last_doc,
        'last_therapy': last_therapy,
    }

    return render(request, 'final_page.html', context)