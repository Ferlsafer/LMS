from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='login_user')
def home(request):
    return render(request, 'index.html')

def about_us(request):
    return render(request, 'about_us.html')

def contact(request):
    return render(request, 'contact_us.html')

def handle_registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']  # phone is for Profile, not User
        password = request.POST['password']
        
        # Create the User object without the phone number
        user = User.objects.create(
            username=username, 
            email=email
        )
        # Set and hash the password
        user.set_password(password)
        user.save()

        # Create a Profile object linked to the user with the phone number
        Profile.objects.create(
            user=user,
            phone=phone,
        )
        
        return redirect('login_user')
    
    return render(request, 'registration_form.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('book_catalog')
    return render(request, 'index.html')

def logout_user(request):
    logout(request)
    return redirect('home')

def admin_dashboard(request):
    '''if not request.user.is_authenticated or not request.user.borrower.is_admin:
        return HttpResponseForbidden("You are not authorized to access this page.")'''
   
    books = Book.objects.all()
    categories = Category.objects.all()
    return render(request, 'admin_dashboard.html', {'books': books, 'categories': categories})

def book_catalog(request):
    books = Book.objects.all()
    return render(request, 'book_catalog.html', {'books': books})
def add_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        isbn = request.POST['isbn']
        publication_date = request.POST['publication_date']
        category_id = request.POST['category']

        author_name = request.POST['author_name']
        author_birth_date = request.POST['author_birth_date']
        author_biography = request.POST['author_biography']

        author, created = Author.objects.get_or_create(
            name=author_name,
            defaults={'birth_date': author_birth_date, 'biography': author_biography}
        )

        category = Category.objects.get(id=category_id)
        Book.objects.create(
            title=title,
            isbn=isbn,
            publication_date=publication_date,
            author=author,
            category=category
        )

        return redirect('list_books') 

    categories = Category.objects.all()
    return render(request, 'add_book.html', {'categories': categories})


def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    authors = Author.objects.all()  

    if request.method == 'POST':
        book.title = request.POST['title']
        book.author_id = request.POST['author']
        book.isbn = request.POST['isbn']
        book.publication_date = request.POST['publication_date']
        book.save()
        return redirect('list_books') 

    return render(request, 'edit_book.html', {'book': book, 'authors': authors})


def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('list_books')

def add_category(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']
        Category.objects.create(name=category_name)
        return redirect('admin_dashboard')  

    return render(request, 'admin_dashboard.html')


def add_author(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        birth_date = request.POST.get('birth_date')
        biography = request.POST.get('biography')

        if not name:
            return HttpResponse("Name is required.", status=400)

        Author.objects.create(name=name, birth_date=birth_date, biography=biography)
        return redirect('add_author')

    return render(request, 'add_author.html')

def list_books(request):
    books = Book.objects.all()
    categories = Category.objects.all()


    category_id = request.GET.get('category')
    sort_by = request.GET.get('sort', 'title')  # Default sort by title

    # This Filter by category if one is selected
    if category_id:
        books = books.filter(category=category_id)  # Use 'category' to sort

    # Sort based on the selected option
    if sort_by == 'author':
        books = books.order_by('author__name')
    elif sort_by == 'publication_date':
        books = books.order_by('publication_date')
    else:
        books = books.order_by('title')  # Default sorting by title

    # displays all the data back to the template so that it can be seen in the UI
    render_data = {
    'books': books,
    'categories': categories,
    'selected_category': category_id,
    'selected_sort': sort_by,
    }
    return render(request, 'books.html', render_data)

        


    

