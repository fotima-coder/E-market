import random
from urllib import request

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from cities_light.models import Country
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model

User = get_user_model()
class RegisterView(View):
    def get(self, request):
        countries = Country.objects.all()
        context = {'countries': countries}
        return render(request, 'register.html', context)

    def post(self, request):
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat-password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        city = request.POST.get('city')
        country_id = request.POST.get('country_id')   # .get() ishlatish juda muhim!

        # 1. Telefon bandligini tekshirish
        if User.objects.filter(phone=phone).exists():
            messages.error(request, 'Bu telefon nomer band!')
            return self.render_with_context(request)

        # 2. Parollar mosligini tekshirish
        if password != repeat_password:
            messages.error(request, 'Parollar mos emas!')
            return self.render_with_context(request)

        # 3. Country_id majburiy
        if not country_id:
            messages.error(request, 'Davlatni tanlash majburiy!')
            return self.render_with_context(request)

        try:
            country = get_object_or_404(Country, id=country_id)
        except:
            messages.error(request, 'Noto‘g‘ri davlat tanlandi!')
            return self.render_with_context(request)

        # User yaratish
        user = User.objects.create_user(
            username=phone,
            phone=phone,
            password=password,
            first_name=first_name,
            last_name=last_name,
            country=country,
            gender=gender,
            city=city,
        )

        confirmation_code = random.randint(100000, 999999)
        user.confirmation_code = f"{confirmation_code}"
        print(confirmation_code)
        user.save()




        login(request, user)
        return redirect('register-confirm')

    # Qayta render qilish uchun yordamchi metod (countries ni qayta yuklash uchun)
    def render_with_context(self, request):
        countries = Country.objects.all()
        context = {'countries': countries}
        return render(request, 'register.html', context)

class RegisterConfirmView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'register-confirm.html')

    def post(self, request):

        if request.POST.get('confirmation_code') == request.user.confirmation_code:
            user = request.user
            user.confirmed = True
            user.save()
            return redirect('home')
        messages.error(request, "Noto'g'ri kod kiritingiz!")
        return self(request)





class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = authenticate(
            username =request.POST.get('username'),
            password =request.POST.get('password')

        )
        if user is not None:
            login(request, user)
            return redirect('home')

        messages.error(request, "Noto'g'ri kod kiritingiz!")
        return render(request, 'login.html')





def logout_view(request):
    logout(request)
    return redirect('login')