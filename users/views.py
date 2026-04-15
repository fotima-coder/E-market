from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from cities_light.models import Country
from .models import User
import random
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from eskiz_sms import EskizSMS

email ="jaloldinovafotima90@gmail.com"
password = "your_password"
eskiz_sms = EskizSMS(email=email, password=password)



class RegisterView(View):
    def get(self,request):
        countries = Country.objects.all()
        context = {
            'countries': countries
        }
        return render(request,'register.html',context)

    def post(self,request):
        if User.objects.filter(phone=request.POST.get('phonel')).exists():
            messages.error(request,'Telefon raqam band qilingan!')
            return render(request,'register.html')
        elif request.POST.get('password') != request.POST.get('repeat_password'):
            messages.error(request,'Parol mos kelmadi!')
            return render(request,'register.html')
        else:
            user = User.objects.create_user(
                username=request.POST.get('phone'),
                password=request.POST.get('password'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                phone=request.POST.get('phonel'),
                gender=request.POST.get('gender'),
                country=get_object_or_404(Country, pk=request.POST.get('country_id')),
                city=request.POST.get('city'),
            )

            confirmation_code = random.randint(100000, 999999)
            user.confirmation_code = f"{confirmation_code}"
            print(confirmation_code)
            user.save()

            login(request,user)
            eskiz_sms.send_sms(user.phone, f"Bu Eskiz dan test")
            return redirect('register-confirm')



class RegisterConfirmView(LoginRequiredMixin, View):
    def get(self,request):
        return render(request,'register-confirm.html')
    def post(self,request):
        if request.POST.get('confirmation_code') == request.user.confirmation_code:
            user = request.user
            user.confirmed = True
            user.save()
            return redirect('home')
        messages.error(request, 'Notogri kod kiritildi !')
        return self.get(request)


class LoginView(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        pass

def logout_view(request):
    logout(request)
    return redirect('register')