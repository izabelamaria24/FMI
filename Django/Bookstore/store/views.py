from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Book
from .forms import BookFilterForm, ContactForm, CustomAuthenticationForm, BookForm
import time
import json
import datetime
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def book_list(request):
    if request.method == 'POST':
        form = BookFilterForm(request.POST)  
        books = Book.objects.all()

        if form.is_valid():
            attributes = ['id', 'isbn', 'description', 'title', 'author', 'category', 'publisher', 'publication_date', 'price']

            for attr in attributes:
                value = form.cleaned_data.get(attr)
                if value:  
                    if attr == 'id':  
                        books = books.filter(**{f'{attr}': value})
                    elif attr == 'price':  
                        books = books.filter(**{f'{attr}': value})
                    elif attr == 'author':  
                        books = books.filter(authors=value)
                    elif attr in ['category', 'publisher']:  
                        books = books.filter(**{f'{attr}': value})
                    else:  
                        books = books.filter(**{f'{attr}__icontains': value})
    else:
        form = BookFilterForm()
        books = Book.objects.all()

    return render(request, 'book_list.html', {'form': form, 'books': books})


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            data_nasterii = form.cleaned_data['data_nasterii']
            mesaj = form.cleaned_data['mesaj']
            mesaj = " ".join(mesaj.replace("\n", " ").split()) 

            varsta = calcul_varsta(data_nasterii)

            timestamp = int(time.time())
            data = {
                "nume": form.cleaned_data['nume'],
                "prenume": form.cleaned_data['prenume'],
                "varsta": varsta,
                "email": form.cleaned_data['email'],
                "tip_mesaj": form.cleaned_data['tip_mesaj'],
                "subiect": form.cleaned_data['subiect'],
                "zile_asteptare": form.cleaned_data['zile_asteptare'],
                "mesaj": mesaj,
            }
            with open(f"mesaje/mesaj_{timestamp}.json", "w") as f:
                json.dump(data, f, indent=4)

            return JsonResponse({"success": True, "message": "Mesajul a fost trimis cu succes."})
        else:
            return JsonResponse({"success": False, "errors": form.errors})

    form = ContactForm()
    return render(request, "contact.html", {"form": form})


def calcul_varsta(data_nasterii):
    azi = datetime.now()
    delta = azi - data_nasterii
    luni = (delta.days // 30) % 12
    ani = delta.days // 365
    return f"{ani} ani și {luni} luni"


def logout_view(request):
    logout(request)
    return redirect('login')


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST, request=request)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if not form.cleaned_data.get('ramane_logat'):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(2*7*24*60*60)           
            return redirect('/store/profile')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'profile.html')


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('/store/books')
    else:
        form = BookForm()

    return render(request, 'add_book.html', {'form': form})