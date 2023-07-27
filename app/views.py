from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail,send_mass_mail
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required 

# Create your views here.
from app.forms import *

def registration(request):
    d={'ufo':UserForm(),'pfo':ProfileForm()}
    if request.method=='POST' and request.FILES:
        ufo=UserForm(request.POST)
        pfo=ProfileForm(request.POST,request.FILES)
        if ufo.is_valid() and pfo.is_valid():
            NUFD=ufo.save(commit=False)
            spw=ufo.cleaned_data['password']
            NUFD.set_password(spw)
            NUFD.save()
            NSPD=pfo.save(commit=False)
            NSPD.username=NUFD
            NSPD.save()

        
            send_mail('Registration',
                      'ur registration is successfull',
                      'bhavyashreetp22@gmail.com',
                      [NUFD.email],
                      
                      fail_silently=False)
            

        return HttpResponse('registration is successfull')

    return render(request,'registration.html',d)


def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)

    return render(request,'home.html')


def userlogin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)
        if AUO:
            if AUO.is_active:
                login(request,AUO)
                request.session['username']=username
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse('Not a Active User')
        else:
            return HttpResponse('Invalid Details')
    return render(request,'userlogin.html')



@login_required
def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def display_details(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)

    d={'UO':UO,'PO':PO}

    return render(request,'display_details.html',d)


@login_required
def change_password(request):
    
    if request.method=='POST':
        pw=request.POST['pw']
        username=request.session['username']

        UO=User.objects.get(username=username)
        UO.set_password(pw)
        UO.save()
        return HttpResponse('password changed successfully')
    return render(request,'change_password.html')


def reset_password(request):
    if request.method=="POST":
        username=request.POST['username']
        pw=request.POST['pw']

        UO=User.objects.get(username=username)
        UO.set_password(pw)
        UO.save()
        return HttpResponse('reset password')

    return render(request,'reset_password.html')









