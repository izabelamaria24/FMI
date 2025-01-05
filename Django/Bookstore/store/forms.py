from django import forms
from django.contrib.auth.models import User
from .models import Category, Publisher, Author, Book, Promotie, Inventory
import re
import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
import os
import json
from django.conf import settings
from django.db import connection
from django.core.mail import mail_admins
from decimal import Decimal
from django.utils import timezone

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
    address = forms.CharField(max_length=150, required=True)

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


TAX_RATE = 0.1  # 10%
class BookForm(forms.ModelForm):
    # Additional fields
    
    additional_discount = forms.DecimalField(
        required=False,
        initial=0.0,
        label="Discount suplimentar (%)",
        help_text="Introduceți un discount suplimentar în procente (ex: 10 pentru 10%).",
        max_digits=5,
        decimal_places=2,
        error_messages={
            'invalid': 'Introduceți un procent valid pentru discount!',
        }
    )
    initial_stock = forms.IntegerField(
        required=False,
        initial=0,
        label="Stoc inițial",
        help_text="Introduceți cantitatea inițială de stoc pentru carte.",
        error_messages={
            'invalid': 'Introduceți o cantitate validă!',
        }
    )
    total_price = forms.DecimalField(
        required=False,
        label="Preț Total",
        disabled=True,
        max_digits=12,
        decimal_places=2,
        help_text="Prețul final calculat după aplicarea discount-ului."
    )
    projected_tax = forms.DecimalField(
        required=False,
        label="Taxă Proiectată",
        disabled=True,
        max_digits=12,
        decimal_places=2,
        help_text="Taxa estimată pe baza prețului total și a stocului."
    )

    class Meta:
        model = Book
        fields = ['title', 'price', 'category', 'description', 'publication_date']
        labels = {
            'title': 'Titlu',
            'price': 'Preț',
            'category': 'Categorie',
            'description': 'Descriere',
            'publication_date': 'Data publicare'
        }
        error_messages = {
            'title': {
                'required': 'Este necesar să introduceți un titlu pentru carte!',
            },
            'price': {
                'required': 'Prețul este obligatoriu!',
                'invalid': 'Introduceți un preț valid!',
            },
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError('Prețul trebuie să fie mai mare decât 0.')
        return price

    def clean_additional_discount(self):
        discount = self.cleaned_data.get('additional_discount')
        if discount is not None and (discount < 0 or discount > 100):
            raise forms.ValidationError('Discount-ul suplimentar trebuie să fie între 0 și 100%.')
        return discount

    def clean_initial_stock(self):
        stock = self.cleaned_data.get('initial_stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError('Stocul inițial nu poate fi negativ.')
        return stock

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        discount = cleaned_data.get('additional_discount')
        stock = cleaned_data.get('initial_stock')

        if price and discount:
        
            total_price = Decimal(price) * (Decimal(1) - Decimal(discount) / Decimal(100))
            if total_price < 0:
                raise forms.ValidationError('Prețul total nu poate fi negativ după aplicarea discount-ului.')

            cleaned_data['total_price'] = total_price

        return cleaned_data

    def save(self, commit=False):
        # Partially save the Book instance
        book = super().save(commit=False)

        # Extract additional fields from cleaned_data
        price = Decimal(book.price)
        discount = Decimal(self.cleaned_data.get('additional_discount', 0))
        initial_stock = self.cleaned_data.get('initial_stock', 0) or 0  # Ensure non-null value

        # Calculate total price and projected tax
        total_price = price * (Decimal(1) - discount / Decimal(100))
        projected_tax = total_price * Decimal(initial_stock) * Decimal(TAX_RATE)

        # Assign total_price to book if applicable
        if hasattr(book, 'total_price'):
            book.total_price = total_price

        # Save book instance
        book.save()

        # Debugging logs
        print(f"Debug - Book saved: {book}")
        print(f"Debug - initial_stock: {initial_stock}, total_price: {total_price}, projected_tax: {projected_tax}")

        # Create or update the associated inventory
        inventory, created = Inventory.objects.get_or_create(
            book=book,
            defaults={
                'stock_qty': initial_stock,
                'projected_tax': projected_tax,
                'restock_date': timezone.now().date(),
            }
        )
        if not created:  # If the inventory already exists, update its fields
            inventory.stock_qty = initial_stock
            inventory.projected_tax = projected_tax
            inventory.restock_date = timezone.now().date()
            inventory.save()

        # Debugging final state
        print(f"Debug - Inventory saved: {inventory}")

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