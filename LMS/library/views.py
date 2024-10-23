from django.shortcuts import render, redirect
from .models import *

def home(request):
    return render(request, 'index.html')

def handle_registration(request):
    if request.method == 'POST':
        name = request.POST['full_name']
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
        return redirect('index.html')
    return render(request, 'index.html')

    

