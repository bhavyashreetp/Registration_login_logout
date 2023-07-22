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













