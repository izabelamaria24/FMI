from django.db import models
from django.contrib.auth.models import User
from django import forms

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Publisher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20)
    publication_date = models.DateField()  
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    authors = models.ManyToManyField(Author, related_name='books')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='inventory')
    stock_qty = models.PositiveIntegerField()
    restock_date = models.DateField() 

    def __str__(self):
        return f"Inventory for {self.book.title}"


class Mesaj(models.Model):
    nume = models.CharField(max_length=10)
    prenume = models.CharField(max_length=50, blank=True)
    varsta = models.CharField(max_length=20)  
    email = models.EmailField()
    tip_mesaj = models.CharField(max_length=20, choices=[
        ('reclamatie', 'Reclamatie'),
        ('intrebare', 'Intrebare'),
        ('review', 'Review'),
        ('cerere', 'Cerere'),
        ('programare', 'Programare'),
    ])
    subiect = models.CharField(max_length=100)
    zile_asteptare = models.PositiveIntegerField()
    mesaj = models.TextField()
    data_trimitere = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mesaj de la {self.nume} ({self.tip_mesaj})"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    loyalty = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
    
