from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.handle_registration, name='register'),
    path('login/', views.login_user, name='login'),
    path('about/', views.about_us, name='about'),
    path('contact/', views.contact, name='contact'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-book/', views.add_book, name='add_book'),
    path('edit-book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete-book/<int:book_id>/', views.delete_book, name='delete_book'),
    path('book_catalog/', views.book_catalog, name='book_catalog'),
    path('add_category/', views.add_category, name='add_category'),
    path('authors/add/', views.add_author, name='add_author'),
    path('list_books', views.list_books, name='list_books'),
]