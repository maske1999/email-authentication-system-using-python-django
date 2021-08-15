from mail_authentication.settings import EMAIL_HOST
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import profile
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
import uuid
# Create your views here.
@login_required
def index(request):
    if request.POST:
        username=request.POST.get('username')
    return render(request, "index.html", {'username': request.user.username})

def login(request):
    if request.POST:
        username=request.POST.get('username')
        password=request.POST.get('password')
        user_obj=User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, 'user is not found')
            return redirect('/login')
        profile_obj=profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_varified:
              messages.success(request, 'profile is not varified')
              return redirect('/login')  
        user=authenticate(username=username,password=password)
        if user is None:
             messages.success(request, 'wrong password')
             return redirect('/login')  
        else:
            auth_login(request,user)
            return redirect('/index')
    return render(request,"login.html")

def register(request):
    if request.POST:
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password') 
        if User.objects.filter(username=username).first():
            messages.success(request, 'username is already taken.')
            return redirect('/register')
        if User.objects.filter(email=email).first():
            messages.success(request, 'email is already taken.')
            return redirect('/register')
        user_obj=User(username=username,email=email)
        user_obj.set_password(password)
        user_obj.save()
        token=str(uuid.uuid4())
        profile_obj=profile(user=user_obj,auth_token=token)
        profile_obj.save()
        send_register_mail(email=email,token=token)
        messages.success(request, 'user is created check email and verify user')
    return render(request,"register.html")

def verify(request, token):
    profile_obj=profile.objects.filter(auth_token=token).first()
    if profile_obj:
        if profile_obj.is_varified:
             messages.success(request, 'profile is already verified.')
             return redirect('/login')
        profile_obj.is_varified=True
        profile_obj.save()
        messages.success(request, 'profile is verified.')
        return redirect('/login')
        
    else:
         messages.success(request, 'error occured')         
         return redirect('/register')



def send_register_mail(email,token):
    subject='your activation link'
    message=f'click to verify email http://127.0.0.1:8000/verify/{token}'
    email_from=settings.EMAIL_HOST_USER
    recipant_list=[email]
    send_mail(subject,message,email_from,recipant_list)

