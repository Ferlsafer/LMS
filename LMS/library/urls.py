from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.handle_registration, name='register'),
    path('login/', views.login_user, name='login'),
    path('about/', views.about_us, name='about'),
    path('contact/', views.contact, name='contact'),
]