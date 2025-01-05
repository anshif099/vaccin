from django.template import loader
from django.http import HttpResponse
from django.shortcuts import  redirect, render
from .models import*
from hello.models import admin
from datetime import datetime, timezone
from django.shortcuts import render, get_object_or_404
from .models import bok
from urllib.parse import unquote
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from .models import Ufeedback, Cfeedback
from itertools import zip_longest
# Create your views here.
def index(request):
    return render(request,"hello/index.html")
def booking(request):
    template = loader.get_template("hello/selectcenterfirst.html") 
    context = {}
    if request.method == "POST": 
        try: 
            centerid = request.POST.get('txtCenterid')  
            login_obj = vccinUpdate.objects.filter(CenterID=centerid).exists()
            if login_obj: 
                user_obj=vccinUpdate.objects.get(CenterID=centerid) 
                request.session['USERNAME'] = user_obj.CenterID
                username = request.session.get('USERNAME')
                items =vccinUpdate.objects.filter(CenterID=username)
                context={
                    'items': items
                    }
                template = loader.get_template("hello/booknow1.html") 
            else: 
                context = {"error": "No Slote Available Yes"}
                HttpResponse(template.render(context, request)) 
        except Exception as e: 
            context = {"error": "No Slote Available Yet"} 
            HttpResponse(template.render(context, request)) 
    return HttpResponse(template.render(context, request)) 

def register(request):
    return render(request,"hello/register.html")
def createReg(request):
    if request.method == "POST":
        email = request.POST["txtEmail"]
        password = request.POST["txtPassword"]
        mobile = request.POST["txtMobile"]
        dob = request.POST["txtDob"]

        
        if user.objects.filter(email=email).exists():
            context = {"error": "User with this email already exists."}
            return render(request, "hello/register.html", context)
        
     
        std = user(email=email, Password=password, Mobile=mobile, Dob=dob)
        std.save()
        return render(request, "hello/login.html", {"success": "Registration successful. Please log in."})
    
    return render(request, "hello/register.html")


def DBLogin(request): 
    template = loader.get_template("hello/login.html") 
    context = {}
    if request.method == "POST": 
        try: 
            email = request.POST.get('txtEmail') 
            password = request.POST.get('txtPassword') 
            login_obj = user.objects.filter(email=email).exists()
            if login_obj: 
                user_obj=user.objects.get(email=email,Password=password) 
                request.session['USERNAME'] = user_obj.email 
                template = loader.get_template("hello/homeindex.html") 
            else: 
                context = {"error": "invalid user"}
                HttpResponse(template.render(context, request)) 
        except Exception as e: 
            context = {"error": "invalid password"} 
            HttpResponse(template.render(context, request)) 
    return HttpResponse(template.render(context, request)) 
def Admin(request):
    return render(request,"hello/admin_login.html")
def ADLogin(request): 
    template = loader.get_template("hello/admin_login.html") 
    context = {}
    if request.method == "POST": 
        try: 
            email = request.POST.get('txtLoginid') 
            login_obj = admin.objects.filter(LgId=email).exists()
            if login_obj: 
                user_obj=admin.objects.get(LgId=email) 
                request.session['USERNAME'] = user_obj.LgId
                template = loader.get_template("hello/admin.html") 
            else: 
                context = {"error": "invalid admin"}
                HttpResponse(template.render(context, request)) 
        except Exception as e: 
            context = {"error": "invalid admin"} 
            HttpResponse(template.render(context, request)) 
    return HttpResponse(template.render(context, request))  
def adminIndex(request):
    return render(request,"hello/admin_index.html")
def addCenter(request):
    return render(request,"hello/add_center.html")
def CDLogin(request): 
    template = loader.get_template("hello/center_login.html") 
    context = {}
    if request.method == "POST": 
        try: 
            email = request.POST.get('txtCenterLgid') 
            login_obj = vccinUpdate.objects.filter(CenterID=email).exists()
            if login_obj: 
                user_obj=vccinUpdate.objects.get(CenterID=email) 
                request.session['USERNAME'] = user_obj.CenterID
                template = loader.get_template("hello/center_home.html") 
            else: 
                context = {"error": "invalid Center"}
                HttpResponse(template.render(context, request)) 
        except Exception as e: 
            context = {"error": "invalid Center"} 
            HttpResponse(template.render(context, request)) 
    return HttpResponse(template.render(context, request))
def mainIndex(request):
    return render(request,"hello/index.html")
def centerhome(request):
    return render(request,"hello/center_home.html")
def booked(request):
    return render(request,"hello/booking_table.html")
def vcb(request):
    if request.method == "POST":
        Center= request.POST["txtCenter"]
        childname = request.POST["txtchildname"]
        cname= request.POST["txtcname"]
        cdate = request.POST["txtcdate"]
    
        
        std =bok(childname=childname,cname=cname,cdate=cdate,center=Center)
        std.save()
        return render(request, "hello/index.html", {"success": "Booking successful."})
    return render(request, "hello/booknow1.html",)
def view_reports(request):
    username = request.session.get('USERNAME')
    if not username:
        return redirect('CDLogin')  

    reports =bok.objects.filter(center=username)
    return render(request, "hello/booking_table.html", {'reports':reports})


def filterDate(request):
    selected_date = request.GET.get('date')
    reports = bok.objects.all()

    if selected_date:
        try:
            
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
            reports = reports.filter(cdate=date_obj)
        except ValueError:
            
            selected_date = None

    context = {
        'reports': reports,
        'selected_date': selected_date,
    }
    return render(request, "hello/booking_table.html", context)

def centerProfile(request):
    username = request.session.get('USERNAME')
    if not username:
        return redirect('CDLogin')  

    profile =vccinUpdate.objects.filter(CenterID=username)
    return render(request,"hello/profile.html",{'profile':profile})

def stock(request):
    if request.method == "POST":
        centerid = request.POST.get("txtCenterid", "")
        cn = request.POST.get("txtCn", "")
        date = request.POST.get("txtDate", "")
        dtp = request.POST.get("txtDtp", "false")
        hepatitisb = request.POST.get("txtHepatitisb", "false")
        polio = request.POST.get("txtPolio", "false")
        hib = request.POST.get("txtHib", "false")
        rotavirus = request.POST.get("txtRotavirus", "false")
        pcv = request.POST.get("txtPcv", "false")
        influenza = request.POST.get("txtInfluenza", "false")
        mmr = request.POST.get("txtMmr", "false")
        vitamina = request.POST.get("txtVitamina", "false")
        varicella = request.POST.get("txtVaricella", "false")
        hepatitisa = request.POST.get("txtHepatitisa", "false")
        tt = request.POST.get("txtTt", "false")
        hpv = request.POST.get("txtHpv", "false")

        
        std = vccinUpdate(
            CenterID=centerid,
            CN=cn,
            Date=date,
            DTP=dtp,
            HepatitisB=hepatitisb,
            Polio=polio,
            Hib=hib,
            Rotavirus=rotavirus,
            PCV=pcv,
            Influenza=influenza,
            MMR=mmr,
            VitaminA=vitamina,
            Varicella=varicella,
            HepatitisA=hepatitisa,
            TT=tt,
            HPV=hpv
        )
        std.save()
        return render(request, "hello/admin_index.html", {"success": "Slot Updated Successfully."})

    return render(request, "hello/ASU1.html")

def centerselect(request):
    return render(request,"hello/selectcenterfirst.html")


def filterCenter(request):
    items = vccinUpdate.objects.all()
    context = {'items': items}
    
    return render(request, "hello/selectcenterfirst.html", context)


def editvc(request):
    username = request.session.get('USERNAME')
    
    if not username:
        return redirect('CDLogin')  # Redirect to the login page if no username is found
    
    # Fetch the records for the center
    reports = vccinUpdate.objects.filter(CenterID=username)
    
    # Assuming only one record per CenterID (you may need to adjust this if multiple records are possible)
    report = reports.first()  # Use the first record if there are multiple (or handle differently if necessary)
    
    return render(request, 'hello/update_vaccines.html', {'report': report})

from django.shortcuts import render, get_object_or_404, redirect
from .models import vccinUpdate

def updatevc(request):
    username = request.session.get('USERNAME')
    
    if not username:
        return render(request, "hello/center_home.html", {"Error": "Username not found in session."})
    
    students = get_object_or_404(vccinUpdate, CenterID=username)
    
    post_data = {
        'CenterID': request.POST.get('txtCenterid', ''),
        'CN': request.POST.get('txtCn', ''),
        'Date': request.POST.get('txtDate', ''),
        'DTP': request.POST.get('txtDtp', 'false'),
        'HepatitisB': request.POST.get('txtHepatitisb', 'false'),
        'Polio': request.POST.get('txtPolio', 'false'),
        'Hib': request.POST.get('txtHib', 'false'),
        'Rotavirus': request.POST.get('txtRotavirus', 'false'),
        'PCV': request.POST.get('txtPcv', 'false'),
        'Influenza': request.POST.get('txtInfluenza', 'false'),
        'MMR': request.POST.get('txtmmr', 'false'),
        'VitaminA': request.POST.get('txtVitamina', 'false'),
        'Varicella': request.POST.get('txtVaricella', 'false'),
        'HepatitisA': request.POST.get('txtHepatitisa', 'false'),
        'TT': request.POST.get('txtTt', 'false'),
        'HPV': request.POST.get('txtHpv', 'false'),
    }
    
    for field, value in post_data.items():
        if value:
            setattr(students, field, value)
    
    students.save()
    
    return render(request, "hello/center_home.html", {"Success": "Slot Updated Successfully."})


def vchistory(request):
    return render(request,"hello/history.html")

def updatingvc(request):
    return render(request,"hello/approve.html")


def approved(request):
    if request.method == "POST":
        remail = request.POST["txtRemail"]
        chname = request.POST["txtName"]
        vcd = request.POST["txtVcd"]
        dt = request.POST["txtDt"]
        uvcn = request.POST["txtUvcn"]
        uvd = request.POST["txtUvd"]
        std = approve(REmail=remail, CHName=chname, VCD=vcd, DT=dt, UVCN=uvcn, UVD=uvd)
        std.save()
        return render(request, "hello/center_home.html", {"Success": "Updated Successfull."})
    return render(request, "hello/approve.html")

def view_certificate(request):
    username = request.session.get('USERNAME')
    if not username:
        return redirect('DBLogin')  

    reports =approve.objects.filter(REmail=username)
    
    return render(request, 'hello/history.html', {'reports':reports}) 

def details(request):
    return render(request,"hello/details.html")

def workBench(request):
    items = approve.objects.all()
    return render(request,"hello/workbench.html",{'items':items})
    




def update_status(request):
    if request.method == "POST":
        report_id = request.POST.get('report_id')
        action = request.POST.get('action')
        
        
        report = bok.objects.get(id=report_id)
        
        
        if action == "approve":
            report.status = "Approved"
        elif action == "reject":
            report.status = "Rejected"
        
        report.save()  
        if report.status=='Approved':
            return redirect('updatingvc')  

    return render(request,"hello/booking_table.html",{'rejected':'Rejected'}, status=400)


def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user_instance = user.objects.filter(email=email).first()  

        if user_instance:
            user_instance.generate_otp()  
            send_mail(
                'Your OTP for Password Reset',
                f'Your OTP is {user_instance.otp}',
                'admin@svacci04.com',
                [user_instance.email],
            )
            messages.success(request, 'OTP has been sent to your email.')
            
            return redirect('password_reset_verify', email=email)
        else:
            messages.error(request, 'User with this email does not exist.')

    return render(request, 'hello/password_reset.html')


def password_reset_verify(request, email):
    
    decoded_email = unquote(email)

   
    user_instance = user.objects.filter(email=decoded_email).first()

    if not user_instance:
        messages.error(request, 'User not found.')
        return redirect('password_reset_request')

    if request.method == 'POST':
        otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

       
        if user_instance.otp == otp and (timezone.now() - user_instance.otp_created_at).total_seconds() < 300:
            if new_password == confirm_password:
                user_instance.Password=new_password
                user_instance.otp=None
                user_instance.otp_created_at=None
                user_instance.save()
                messages.success(request, 'Password reset successfully.')
                return redirect('DBLogin')  
            else:
                messages.error(request, 'Passwords do not match.')
        else:
            messages.error(request, 'Invalid OTP or OTP has expired.')

    return render(request, 'hello/password_reset_verify.html', {'email': decoded_email})

def userprofile(request):
    username = request.session.get('USERNAME')
    if not username:
        return redirect('CDLogin')  

    profile =user.objects.filter(email=username)
    return render(request,"hello/userprofile.html",{'profile':profile})

def userfeedback(request):
    return render(request,"hello/feedback.html")

def userfeedback(request):
    if request.method == "POST":
        fun = request.POST["txtFun"]
        feed = request.POST["txtFeed"]
        
        std = Ufeedback(FUN=fun, Feed=feed,)
        std.save()
        return render(request, "hello/index.html", {"success": "Feedback Submited Successfully."})
    
    return render(request, "hello/feedback.html")

def centerfeedback(request):
    if request.method == "POST":
        fun = request.POST["txtFun"]
        feed = request.POST["txtFeed"]
        
    
        std = Cfeedback(FCN=fun, CFeed=feed,)
        std.save()
        return render(request, "hello/center_home.html", {"success": "Feedback Submited Successfully."})
    
    return render(request, "hello/centerfeedback.html")

def admindash(request):
    return render(request,"hello/admin.html")


from django.http import JsonResponse

def dashboard_data(request):
    try:
       
        total_users = user.objects.count()
        vaccinated_users = bok.objects.count()
        non_vaccinated_users = total_users - vaccinated_users
        total_centers = vccinUpdate.objects.count()

     
        return JsonResponse({
            'total_users': total_users,
            'vaccinated_users': vaccinated_users,
            'non_vaccinated_users': non_vaccinated_users,
            'total_centers': total_centers,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

def manageuser(request):
    if request.method == "POST" and "delete_user" in request.POST:
        user_id = request.POST.get("delete_user")
        user.objects.filter(id=user_id).delete()
        return redirect("manageuser")  

    users = user.objects.all()
    return render(request, "hello/manageuser.html", {"users": users})


def manage_centers(request):
    centers = vccinUpdate.objects.all()  
    if request.method == 'POST':
        center_id = request.POST.get('delete_center')
        if center_id:
            center = vccinUpdate.objects.get(CenterID=center_id)
            center.delete()  
            return redirect('manage_centers')  
    return render(request, 'hello/managecenter.html', {'centers': centers})




def vaccinated_users(request):

    records = bok.objects.all()


    if request.method == 'POST':
        record_id = request.POST.get('delete_record')
        if record_id:
            record = bok.objects.get(id=record_id)
            record.delete()  
            return redirect('vaccinated_users')  

    return render(request, 'hello/vaccinateduser.html', {'records': records})




from django.http import JsonResponse
import json

def manage_center(request):
    records = vccinUpdate.objects.all()
    return render(request, 'hello/addcenter.html', {'records': records})

def add_center(request):
    if request.method == "POST":
        data = json.loads(request.body)
        centerID = data.get('CenterID')
        centerName = data.get('CN')


        new_center = vccinUpdate(
            CenterID=centerID,
            CN=centerName,
        )
        new_center.save()

        return JsonResponse({
            'success': True,
            'centerID': centerID,
            'centerName': centerName,

            
        })
    return JsonResponse({'success': False})

def manage_feedback(request):
    
    user_feedbacks = Ufeedback.objects.all()
    center_feedbacks = Cfeedback.objects.all()

    feedbacks = zip_longest(center_feedbacks, user_feedbacks, fillvalue=None)

    return render(request, "hello/viewfeedback.html", {'feedbacks': feedbacks})
