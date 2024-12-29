from django import forms
from django.contrib.auth.models import User
from .models import Category, Publisher, Author, Book, Promotie
import re
import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
import os
import json
from django.conf import settings
from django.db import connection
from django.core.mail import mail_admins

class CustomAuthenticationForm(AuthenticationForm):
    ramane_logat = forms.BooleanField(
        required=False,
        initial=False,
        label='Ramaneti logat'
    )

    def clean(self):        
        cleaned_data = super().clean()
        ramane_logat = self.cleaned_data.get('ramane_logat')
        return cleaned_data

class BookFilterForm(forms.Form):
    id = forms.IntegerField(required=False, label='ID')
    isbn = forms.CharField(required=False, label='ISBN')
    description = forms.CharField(required=False, label='Description', widget=forms.Textarea(attrs={'rows': 1}))
    title = forms.CharField(required=False, label='Title')
    authors = forms.ModelChoiceField(queryset=Author.objects.all(), required=False, label='Author')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Category')
    publisher = forms.ModelChoiceField(queryset=Publisher.objects.all(), required=False, label='Publisher')
    publication_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Publication Date')
    price = forms.DecimalField(required=False, min_value=0, label='Price')


class ContactForm(forms.Form):
    nume = forms.CharField(
        max_length=10,
        required=True,
        label="Nume",
        validators=[
            lambda value: re.match(r'^[A-Z][a-zA-Z ]*$', value) or forms.ValidationError("Numele trebuie să înceapă cu literă mare și să conțină doar litere și spații.")
        ],
    )
    prenume = forms.CharField(
        max_length=50,
        required=False,
        label="Prenume",
        validators=[
            lambda value: value == "" or re.match(r'^[A-Z][a-zA-Z ]*$', value) or forms.ValidationError("Prenumele trebuie să înceapă cu literă mare și să conțină doar litere și spații.")
        ],
    )
    data_nasterii = forms.DateField(
        required=True,
        label="Data nașterii",
        input_formats=['%Y-%m-%d', '%d-%m-%Y'] 
    )
    email = forms.EmailField(required=True, label="E-mail")
    confirm_email = forms.EmailField(required=True, label="Confirmare e-mail")
    tip_mesaj = forms.ChoiceField(
        choices=[
            ('reclamatie', 'Reclamatie'),
            ('intrebare', 'Intrebare'),
            ('review', 'Review'),
            ('cerere', 'Cerere'),
            ('programare', 'Programare'),
        ],
        label="Tip mesaj"
    )
    subiect = forms.CharField(
        max_length=100,
        required=True,
        label="Subiect",
        validators=[
            lambda value: re.match(r'^[A-Z][a-zA-Z ]*$', value) or forms.ValidationError("Subiectul trebuie să înceapă cu literă mare și să conțină doar litere și spații.")
        ],
    )
    zile_asteptare = forms.IntegerField(min_value=1, required=True, label="Minim zile așteptare")
    mesaj = forms.CharField(
        widget=forms.Textarea,
        required=True,
        label="Mesaj (semnați cu numele dvs.)"
    )

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get('email')
        confirm_email = cleaned_data.get('confirm_email')
        if email != confirm_email:
            self.add_error('confirm_email', "E-mailurile nu coincid.")

        data_nasterii = cleaned_data.get('data_nasterii')
        varsta = 0
        if data_nasterii:
            today = datetime.date.today()
            age = today.year - data_nasterii.year - ((today.month, today.day) < (data_nasterii.month, data_nasterii.day))
            varsta = age
            if age < 18:
                self.add_error('data_nasterii', "Trebuie să fiti major.")

        mesaj = cleaned_data.get('mesaj')
        if mesaj:
            if "http://" in mesaj or "https://" in mesaj:
                self.add_error('mesaj', "Mesajul nu poate contine linkuri.")
            if len(re.findall(r'\b\w+\b', mesaj)) < 5 or len(re.findall(r'\b\w+\b', mesaj)) > 100:
                self.add_error('mesaj', "Mesajul trebuie să contina între 5 si 100 de cuvinte.")
            nume = cleaned_data.get('nume')
            if not mesaj.endswith(nume):
                self.add_error('mesaj', "Mesajul trebuie sa se termine cu numele dvs.")
                
        if not self.is_valid():
            print(self.errors)

        if self.is_valid():
            folder_path = os.path.join(settings.BASE_DIR, 'mesaje') 
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            timestamp = datetime.datetime.now().time()
            timestamp = re.sub(r'[^a-zA-Z0-9_-]', '', str(timestamp))
            file_name = f"mesaj_{timestamp}.json"
            file_path = os.path.join(folder_path, file_name)

            message_data = {
                'nume': cleaned_data.get('nume'),
                'prenume': cleaned_data.get('prenume'),
                'varsta': varsta,
                'email': cleaned_data.get('email'),
                'tip_mesaj': cleaned_data.get('tip_mesaj'),
                'subiect': cleaned_data.get('subiect'),
                'zile_asteptare': cleaned_data.get('zile_asteptare'),
                'mesaj': cleaned_data.get('mesaj'),
            }

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(message_data, f, ensure_ascii=False, indent=4)

        return cleaned_data
    
    
class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    phone_number = forms.CharField(max_length=15, required=True)
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    address = forms.CharField(widget=forms.Textarea, required=True)
    loyalty = forms.IntegerField(required=False, min_value=0)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if username.lower() == 'admin':
            subject = "cineva incearca sa ne preia site-ul"
            message_html = f"""
            <h1 style="color: red;">{subject}</h1>
            <p>Email: {email}</p>
            """
            message_text = f"Email: {email}"
            mail_admins(subject, message_text, html_message=message_html)
            raise ValidationError("Nu poți folosi username-ul 'admin'.")
        return username

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        if len(phone_number) < 10:
            raise ValidationError("Phone number must be at least 10 digits long.")
        return phone_number

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth.year > 2010:
            raise ValidationError("You must be at least 14 years old to register.")
        return date_of_birth

    def clean_loyalty(self):
        loyalty = self.cleaned_data.get('loyalty')
        if loyalty and loyalty < 0:
            raise ValidationError("Loyalty points cannot be negative.")
        return loyalty


class BookForm(forms.ModelForm):
    additional_discount = forms.DecimalField(
        required=False,
        initial=0.0,
        label="Additional Discount (%)",
        help_text="Introduceți un discount suplimentar în procente (ex: 10 pentru 10%).",
        max_digits=5,
        decimal_places=2
    )
    additional_quantity = forms.IntegerField(
        required=False,
        initial=0,
        label="Additional Quantity",
        help_text="Introduceți cantitatea suplimentară care va fi adăugată la stoc."
    )
    final_price = forms.DecimalField(
        required=False,
        label="Preț Final",
        disabled=True,
        max_digits=8,
        decimal_places=2
    )
    total_quantity = forms.IntegerField(
        required=False,
        label="Cantitate Totală",
        disabled=True 
    )

    class Meta:
        model = Book
        fields = ['title', 'isbn', 'publication_date', 'price', 'authors', 'category', 'publisher', 'description']
        labels = {
            'title': 'Titlu',
            'isbn': 'ISBN',
            'publication_date': 'Data publicării',
            'price': 'Preț',
            'authors': 'Autori',
            'category': 'Categorie',
            'publisher': 'Editor',
            'description': 'Descriere',
        }
        error_messages = {
            'title': {
                'required': 'Este necesar să introduceți un titlu pentru carte!',
            },
            'isbn': {
                'required': 'Introduceti ISBN-ul cărții!',
                'unique': 'Acest ISBN este deja înregistrat!',
            },
            'price': {
                'required': 'Prețul este obligatoriu!',
                'invalid': 'Introduceti un preț valid!',
            },
            'publication_date': {
                'required': 'Data publicării este obligatorie!',
            },
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError('Prețul trebuie să fie mai mare decât 0.')
        return price

    def clean_additional_discount(self):
        discount = self.cleaned_data.get('additional_discount')
        if discount is not None and discount < 0:
            raise forms.ValidationError('Discount-ul suplimentar nu poate fi negativ.')
        return discount

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if Book.objects.filter(isbn=isbn).exists():
            raise forms.ValidationError('Acest ISBN este deja înregistrat!')
        return isbn

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        discount = cleaned_data.get('additional_discount')

        if discount and discount > 100:
            raise forms.ValidationError(
                'Discount-ul nu poate depăși 100%.'
            )

        category = cleaned_data.get('category')
        if category and price:
            if category.name == 'Premium' and price < 50:
                raise forms.ValidationError(
                    'Cărțile din categoria Premium trebuie să aibă un preț mai mare de 50!'
                )

        return cleaned_data

    def save(self, commit=False):
        book = super().save(commit=False)

        price = book.price
        additional_discount = self.cleaned_data.get('additional_discount', 0)
        final_price = price * (1 - additional_discount / 100)

        additional_quantity = self.cleaned_data.get('additional_quantity', 0)
        total_quantity = additional_quantity

        book.price = final_price
        book.save()
        
        if commit:
            from .models import Inventory
            inventory, created = Inventory.objects.get_or_create(book=book)
            inventory.stock_qty = total_quantity
            inventory.save()

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT setval(pg_get_serial_sequence('store_book', 'id'), 
                (SELECT MAX(id) FROM store_book) + 1);
            """)

        return book
    
    
class PromotieForm(forms.ModelForm):
    categoriile_promo = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple, 
        required=True
    )

    class Meta:
        model = Promotie
        fields = ['nume', 'subiect', 'mesaj', 'data_expirare', 'categoriile_promo', 'procent_discount', 'k_vizualizari_minime']