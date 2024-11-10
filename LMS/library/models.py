from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return f'Name: {self.name}'
    
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    publication_date = models.DateField()
    category = models.ManyToManyField(Category)
    isbn = models.CharField(max_length=30)
    def __str__(self) -> str:
        return self.user.username

#trial comment
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15)

    def __str__(self) -> str:
        return f'user: {self.user}'
    
class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    biography = models.TextField(max_length=1200)


    def __str__(self) -> str:
        return f'{self.name}'
    
class Borrower(models.Model):
    username = models.CharField(max_length=100, default='dickson')
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=15)


    def __str__(self) -> str:
        return f'Name: {self.name}'
    
class BorrowerRecords(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    borrower = models.ForeignKey(Borrower, on_delete=models.PROTECT)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f'Borrow Date: {self.borrow_date}, Return Date: {self.return_date}'
    


    


   