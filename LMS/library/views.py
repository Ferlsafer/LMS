from django.shortcuts import render, redirect
from .models import *

def home(request):
    return render(request, 'index.html')

def about_us(request):
    return render(request, 'about_us.html')

def contact(request):
    return render(request, 'contact_us.html')

def handle_registration(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        user = Borrower(
            name = name,
            email = email,
            phone = phone,
            password = password
        )
        user.save()
        return redirect('home')
    return render(request, 'registration_form.html')

def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = Borrower.object.get(email==email)
        if user.password == password:
            return redirect('home')
    return render(request, 'index.html')
        


    

