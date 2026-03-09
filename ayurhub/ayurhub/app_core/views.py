from django.http import HttpResponse # pyright: ignore[reportMissingModuleSource]
from django.shortcuts import render # type: ignore
from app_core.models import Category, District, Doctor, Location, Medicine_Category, Product, Therapy
from app_dashboard.models import Patientregi
from app_patient.models import DoctorAppointment, TherapyAppointment
from ayurhub.users.models import User



# Create your views here.
def dist(request):
    if request.method=='POST':
        name=request.POST.get('name')
        print("success ")
        if District.objects.filter(name = name ).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/core/dist/';</script>")
        dist=District()
        dist.name=name
        dist.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='/core/dist/';</script>")
    else:
        return render(request,"district.html")
    

def viewdis(request):
    v=District.objects.all()
    return render(request,"viewdis.html",{"list":v})


def deletedist(request,id):
    d=District.objects.get(id=id)
    d.delete()
    return HttpResponse("<script>alert('Deleted Successfully');window.location='/core/viewdis/';</script>")


def editdis(request,id):
   s=District.objects.get(id=id)
   if request.method=='POST' :
        print ("submission successfull")
        name= request.POST.get('name')
        print (name)
        if District.objects.filter(name=name).exists():
            return HttpResponse("<script>alert('Already Exists');window.location='/core/viewdis/';</script>")
        
        s.name=name
        s.save()
        return HttpResponse("<script>alert('Edited Successfully');window.location='/core/viewdis/';</script>" )
   else:
        
#  return HttpResponse("<script>alert('Deleted Successfully');window.location='/home/vcat';</script>" )
    return render(request,'editdis.html',{'editdis':s})
   



def location(request):
    if request.method=='POST':
        name=request.POST.get('name')
        dis=request.POST.get('name1')
        print("success ")
        if Location.objects.filter(name = name,dis=dis ).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/core/location/';</script>")
        loc=Location()
        loc.name=name
        loc.dis=District.objects.get(id = dis)
        loc.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='/core/location/';</script>")
    else:
        v=District.objects.all()
        return render(request,"location.html",{"list":v})
    

def viewloc(request):
    v=Location.objects.all()
    return render(request,"viewloc.html",{"list":v})

def deleteloc(request,id):
    d=Location.objects.get(id=id)
    d.delete()
    return HttpResponse("<script>alert('Deleted Successfully');window.location='/core/viewloc/';</script>")


def locationup(request,id):
    up = Location.objects.get(id=id)
    if request.method=="POST":
        name = request.POST.get('name')
        dis = request.POST.get('dis')
        # return HttpResponse(dis)
        if Location.objects.filter( name=name, dis=dis ).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='';</script>")
        up.name = name
        up.dis = District.objects.get(id = dis)
        up.save()
        return HttpResponse("<script>alert('Updated Successfully');window.location='/core/viewloc/';</script>")
    list=District.objects.all()
    return render(request,"editloc.html",{"locationv":up,"list":list})





def category(request): 
    if request.method=='POST':
        name=request.POST.get('name')
        # description=request.POST.get('description')
        print("success ")
        if Category.objects.filter(name = name ).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/core/category/';</script>")
        cat=Category()
        cat.name=name
        # cat.description=description
        if len(request.FILES) !=0:
            img = request.FILES['img']
        else:
            img = 'Images/default.jpg'
        cat.img=img
        cat.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='/core/category/';</script>")
    else:
        return render(request,"category.html")
    
def viewcat(request):
    cv=Category.objects.all()
    return render(request,"viewcat.html",{"list":cv})


def deletecat(request,name):
    d=Category.objects.get(id=name)
    d.delete()
    return HttpResponse("<script>alert('Deleted Successfully');window.location='/core/viewcat/';</script>")


def cateup(request,name):
    up = Category.objects.get(id=name)
    if request.method=="POST":
        cname = request.POST.get('name')
        desc = request.POST.get('description')
        img = request.FILES.get('img')

        if Category.objects.filter(name=cname).exclude(id=name).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/core/category/';</script>")
        up.name=cname
        up.description=desc
        if img:
            up.img=img
        up.save()
        return HttpResponse("<script>alert('Updated Successfully');window.location='/core/viewcat/';</script>")
    return render(request,"editcat.html",{"catv":up})


def doctor(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')
        contact=request.POST.get('contact')
        specialization=request.POST.get('specialization')
        schedule=request.POST.get('schedule')
        experience=request.POST.get('experience')
        if request.FILES.get('img'):
            img = request.FILES['img']
        else:
            img = 'Images/default.jpg'
        fee=request.POST.get('fee')
        mode=request.POST.get('mode')
        qualification=request.POST.get('qualification')
        about=request.POST.get('about')

        if not username or not password:
            return HttpResponse("<script>alert('Username and Password are required');window.location='/core/doctor/';</script>")
        if User.objects.filter(username = username,email=email ).exists():
            return HttpResponse("<script>alert('User Already Exist');window.location='/core/doctor/';</script>")
        user=User()
        user.name=name
        user.email=email
        user.username=username
        user.set_password(password)
        user.role='Doctor'
        user.save()

        Doctor.objects.create(
            user=user,contact=contact,specialization=specialization,schedule=schedule,experience=experience,fee=fee,img=img,mode=mode,qualification=qualification,about=about)
        return HttpResponse("<script>alert('Doctor Added Successfully');window.location='/core/doctor/';</script>")
    else:   
        return render(request,"doctor.html")
        

def viewdoc(request):
    dv=Doctor.objects.all()
    return render(request,"viewdoc.html",{"list":dv})


def viewpatient(request):
    pv=Patientregi.objects.all()
    return render(request,"viewpatient.html",{"pt":pv})


def therapies(request):
    if request.method=='POST':
        therapyname=request.POST.get('therapyname')#bracket kodtha corresponding htmlpg ll name= kodthath
        servicename=request.POST.get('servicename')
        shortdescription=request.POST.get('shortdescription')
        description=request.POST.get('description')
        duration=request.POST.get('duration')
        price=request.POST.get('price')
        benefits=request.POST.get('benefits')
        productused=request.POST.get('productused')
        count=request.POST.get('count')
        print("success ")
        if Therapy.objects.filter(therapyname_id = therapyname, servicename=servicename ).exists():#first therapyname is variable name second is model perrr
            return HttpResponse("<script>alert('Already Exist');window.location='/core/therapies/';</script>")
        
        ther=Therapy()# Therapy model inda object aan ther
        # ther.therapyname=therapyname #ivide therapyname ennath model ll nn vilikkunnath
        ther.servicename=servicename#obj.modelname=variablename
        ther.shortdescription=shortdescription
        ther.description=description
        if len(request.FILES) !=0:
            img = request.FILES['img']
        else:
           img = 'Images/default.jpg'
        ther.img=img
        ther.duration=duration
        ther.price=price
        ther.benefits=benefits
        ther.productused=productused
        ther.count=count
        ther.therapyname=Category.objects.get(id=therapyname)# obj.fk field name from model=eviden aano vilikne aa model name.object.get(id=field name from model)
        ther.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='/core/therapies/';</script>")
    else:
        cat=Category.objects.all()
        return render(request,"therapies.html",{"list":cat})#list = context (ndh name venel kodkaa)

       
def viewtherapies(request):
    tv=Therapy.objects.all()
    return render(request,"viewtherapies.html",{"viewthera":tv})

def deletetherapy(request,id):
    d=Therapy.objects.get(id=id)
    d.delete()
    return HttpResponse("<script>alert('Deleted Successfully');window.location='/core/viewtherapies/';</script>")

def edittherapy(request,id):# ivide id vanath urls id il ninnum
    s=Therapy.objects.get(id=id)
    if request.method=='POST' :
          print ("submission successfull")
          therapyname= request.POST.get('therapyname')
          servicename= request.POST.get('servicename')
          shortdescription= request.POST.get('shortdescription')

          description= request.POST.get('description')
          duration= request.POST.get('duration')
          price= request.POST.get('price')
          benefits= request.POST.get('benefits')
          productused= request.POST.get('productused')
          count= request.POST.get('count')
    
          if Therapy.objects.filter(therapyname=therapyname, servicename=servicename).exclude(id=id).exists():
                return HttpResponse("<script>alert('Already Exists');window.location='/core/viewtherapies/';</script>")
          
          s.therapyname=Category.objects.get(id=therapyname)
          s.servicename=servicename
          s.shortdescription=shortdescription
          s.description=description
          if len(request.FILES) !=0:
                img = request.FILES['img']
                s.img=img
          s.duration=duration
          s.price=price
          s.benefits=benefits
          s.productused=productused
          s.count=count
          s.save()
          return HttpResponse("<script>alert('Edited Successfully');window.location='/core/viewtherapies/';</script>" )
    else:
         s=Therapy.objects.get(id=id)
         c=Category.objects.all()
         return render(request,'edittherapies.html',{'editt':s,'list':c})




def medicinecategory(request):
    if request.method=='POST':
        name=request.POST.get('name')
        print("success ")
        if Medicine_Category.objects.filter(name = name ).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/core/medicinecategory/';</script>")
        medcat=Medicine_Category()
        medcat.name=name
        if len(request.FILES) !=0:
            img = request.FILES['img']
        else:
            img = 'Images/default.jpg'
        medcat.img=img
        medcat.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='/core/medicinecategory/';</script>")
    else:
        return render(request,"medicinecategory.html")


def viewmedicinecat(request):
    mv=Medicine_Category.objects.all()
    return render(request,"viewmedicat.html",{"medcat":mv})


def delmedicinecat(request,id):
    d=Medicine_Category.objects.get(id=id)
    d.delete()
    return HttpResponse("<script>alert('Deleted Successfully');window.location='/core/viewmedicat/';</script>")


def editmedicinecat(request,id):
    up = Medicine_Category.objects.get(id=id)
    if request.method=="POST":
        cname = request.POST.get('name')
        img = request.FILES.get('img')

        if Medicine_Category.objects.filter(name=cname).exclude(id=id).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/core/medicinecategory/';</script>")
        up.name=cname
        if img:
            up.img=img
        up.save()
        return HttpResponse("<script>alert('Updated Successfully');window.location='/core/viewmedicat/';</script>")
    return render(request,"editmedicinecat.html",{"medcatv":up})


def product(request):
    if request.method=='POST':
        medicinecategory=request.POST.get('medicinecategory')
        productname=request.POST.get('productname')
        description=request.POST.get('description')
        price=request.POST.get('price')
        print("success ")
        if Product.objects.filter(medicinecategory = medicinecategory, productname=productname ).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/core/product/';</script>")
        
        pr=Product()
        pr.productname=productname
        pr.description=description
        if len(request.FILES) !=0:
            img = request.FILES['img']
        else:
           img = 'Images/default.jpg'
        pr.img=img
        pr.price=price
        pr.medicinecategory=Medicine_Category.objects.get(id=medicinecategory)
        pr.quantity=request.POST.get('quantity')    
        pr.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='/core/product/';</script>")
    else:
        cat=Medicine_Category.objects.all()
        return render(request,"product.html",{"list":cat})  
    

def viewproduct(request):
    pv=Product.objects.all()
    return render(request,"viewproduct.html",{"viewprod":pv})

def deletproduct(request,id):
    d=Product.objects.get(id=id)
    d.delete()
    return HttpResponse("<script>alert('Deleted Successfully');window.location='/core/viewproduct/';</script>")

def editproduct(request,id):
    s=Product.objects.get(id=id)
    if request.method=='POST' :
          print ("submission successfull")
          medicinecategory= request.POST.get('medicinecategory')
          productname= request.POST.get('productname')
          description= request.POST.get('description')
          price= request.POST.get('price')
          quantity=request.POST.get('quantity')
    
          if Product.objects.filter(medicinecategory=medicinecategory, productname=productname).exclude(id=id).exists():
                return HttpResponse("<script>alert('Already Exists');window.location='/core/viewproduct/';</script>")
          
          s.medicinecategory=Medicine_Category.objects.get(id=medicinecategory)
          s.productname=productname
          s.description=description
          if len(request.FILES) !=0:
                img = request.FILES['img']
                s.img=img
          s.price=price
          s.quantity=quantity
          s.save()
          return HttpResponse("<script>alert('Edited Successfully');window.location='/core/viewproduct/';</script>" )
    else:
         s=Product.objects.get(id=id)
         c=Medicine_Category.objects.all()
         return render(request,'editproduct.html',{'editp':s,'list':c})
     
     
   


def view_appointments(request):
    # Fetch all Doctor appointments (newest first)
    doc_appointments = DoctorAppointment.objects.select_related('doctor', 'patient').all().order_by('-appointment_date')
    
    # Fetch all Therapy appointments (newest first)
    therapy_appointments = TherapyAppointment.objects.select_related('therapy', 'patient').all().order_by('-appointment_date')

    context = {
        'doc_appointments': doc_appointments,
        'therapy_appointments': therapy_appointments,
    }
    return render(request, 'view_appointments.html', context)




def view_doctor_schedule(request):
    # Fetch all doctors and their user details
    doctors = Doctor.objects.select_related('user').all()
    
    context = {
        'doctors': doctors
    }
    return render(request, 'view_doctor_schedule.html', context)


from django.shortcuts import render
from django.db.models import Sum
from app_patient.models import Booking_details   # ✅ correct model name


def admin_product_pie_chart(request):

    # Aggregate total quantity purchased per product
    product_data = (
        Booking_details.objects
        .values('product__productname')   # ✅ correct field name
        .annotate(total_purchased=Sum('quantity'))
        .order_by('-total_purchased')
    )

    # Prepare labels
    labels = [
        item['product__productname']
        for item in product_data
        if item['product__productname']
    ]

    # Prepare data
    data = [
        item['total_purchased']
        for item in product_data
    ]

    context = {
        'labels': labels,
        'data': data,
    }

    return render(request, 'booking_report.html', context)


from django.shortcuts import render
from app_patient.models import DoctorAppointment, TherapyAppointment

def appointment_report(request):

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    doctor_appointments = DoctorAppointment.objects.all().order_by('-appointment_date')
    therapy_appointments = TherapyAppointment.objects.all().order_by('-appointment_date')

    # Apply filter
    if start_date and end_date:
        doctor_appointments = doctor_appointments.filter(
            appointment_date__range=[start_date, end_date]
        )

        therapy_appointments = therapy_appointments.filter(
            appointment_date__range=[start_date, end_date]
        )

    context = {
        'doctor_data': doctor_appointments,
        'therapy_data': therapy_appointments,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'appointment_report.html', context)