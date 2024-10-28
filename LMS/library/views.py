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
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        is_admin = request.POST.get('is_admin') == 'on'  # I added this for the purpose handlelign normal user and admin temporary
        
        borrower = Borrower.objects.create(
            name=name, email=email, phone=phone, password=password, is_admin=is_admin
        )
        if is_admin:
            return redirect('admin_dashboard')  # after registration admin will be sent to admin dashboard direct
        else:
            return redirect('books.html') #this will send a normal user to book list page
    return render(request, 'registration_form.html')

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('list_books')
        return redirect('handle_registration')
    
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
    # Logic to display the book catalog for normal users
    books = Book.objects.all()
    return render(request, 'books.html', {'books': books})
def add_book(request):
    if request.method == 'POST':
        # Get book information from the form
        title = request.POST['title']
        isbn = request.POST['isbn']
        publication_date = request.POST['publication_date']
        category_id = request.POST['category']

        # Get author information from the form
        author_name = request.POST['author_name']
        author_birth_date = request.POST['author_birth_date']
        author_biography = request.POST['author_biography']

        # Create or get the author
        author, created = Author.objects.get_or_create(
            name=author_name,
            defaults={'birth_date': author_birth_date, 'biography': author_biography}
        )

        # Create the book with the selected category and the new author
        category = Category.objects.get(id=category_id)
        Book.objects.create(
            title=title,
            isbn=isbn,
            publication_date=publication_date,
            author=author,
            category=category
        )

        return redirect('list_books')  # Redirect to book list after adding all the information from the form

    categories = Category.objects.all()
    return render(request, 'add_book.html', {'categories': categories})


def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    authors = Author.objects.all()  

    if request.method == 'POST':
        # Get updated book information after editing it from the editing form 
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

        # I added this to make sure the field is filled
        if not name:
            return HttpResponse("Name is required.", status=400)

        Author.objects.create(name=name, birth_date=birth_date, biography=biography)
        return redirect('add_author')

    return render(request, 'add_author.html')

def list_books(request):
    books = Book.objects.all()
    categories = Category.objects.all()

    # Get filter and sort parameters from the request sent by the user from the form
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

        


    

