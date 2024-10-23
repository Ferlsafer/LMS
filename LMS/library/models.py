from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=30)


    def __str__(self) -> str:
        return f'name: {self.title}'
    
class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    biography = models.TextField(max_length=1200)


    def __str__(self) -> str:
        return f'{self.name}'
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField('Book')

    def __str__(self) -> str:
        return f'Name: {self.name}'
    
class Borrower(models.Model):
    books = models.ManyToManyField('Book')
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=15)

    def __str__(self) -> str:
        return f'Name: {self.name}'
    
class BorrowerRecords(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f'Borrow Date: {self.borrow_date}, Return Date: {self.return_date}'
    

    


   