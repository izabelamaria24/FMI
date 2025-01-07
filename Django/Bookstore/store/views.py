from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from .models import Book, UserProfile, Vizualizare, User, Promotie, Publisher, Category, Author, Cart, CartItem, Inventory, Order, OrderItem
from .forms import BookFilterForm, ContactForm, CustomAuthenticationForm, BookForm, UserRegistrationForm, PromotieForm
import time
import json
import datetime
from datetime import timedelta
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, EmailMessage, mail_admins
import uuid
from django.utils.timezone import now
from django.contrib.auth.models import Permission
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import logging
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

logger = logging.getLogger('django')

failed_logins = {}

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def book_list(request):
    logger.debug('Entering book_list view')

    if request.method == 'POST':
        form = BookFilterForm(request.POST)
        logger.debug('Form data received: %s', request.POST)
        books = Book.objects.all()

        if form.is_valid():
            logger.debug('Form is valid, filtering books based on attributes')
            attributes = ['id', 'isbn', 'description', 'title', 'author', 'category', 'publisher', 'publication_date', 'price']

            for attr in attributes:
                value = form.cleaned_data.get(attr)
                if value:  
                    logger.debug('Filtering by %s with value %s', attr, value)
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
        logger.debug('Form is not POST, displaying all books')

    books_in_cart = set()
    if request.user.is_authenticated:
        logger.debug('User is authenticated, fetching cart items')
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            books_in_cart = set(cart.items.values_list('inventory__book_id', flat=True))
            logger.debug('Books in cart: %s', books_in_cart)

    logger.debug('Rendering book_list template')
    return render(request, 'book_list.html', {
        'form': form,
        'books': books,
        'books_in_cart': books_in_cart
    })


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            logger.info('Contact form submitted successfully by user %s', form.cleaned_data['email'])
            data_nasterii = form.cleaned_data['data_nasterii']
            mesaj = form.cleaned_data['mesaj']
            mesaj = " ".join(mesaj.replace("\n", " ").split()) 

            varsta = 20

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
            logger.warning('Contact form submission failed with errors: %s', form.errors)
            return JsonResponse({"success": False, "errors": form.errors})

    form = ContactForm()
    return render(request, "contact.html", {"form": form})


def calcul_varsta(data_nasterii):
    azi = datetime.datetime.now().time()
    delta = azi - data_nasterii
    luni = (delta.days // 30) % 12
    ani = delta.days // 365
    return f"{ani} ani și {luni} luni"


def logout_view(request):
    permission = Permission.objects.get(codename="vizualizeaza_oferta")
    request.user.user_permissions.remove(permission)
    
    logout(request)
    return redirect('login')


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST, request=request)
        username = request.POST.get('username')
        ip = get_client_ip(request)

        if username not in failed_logins:
            failed_logins[username] = []

        if form.is_valid():
            user = form.get_user()

            if hasattr(user, 'profile') and user.profile.blocked:
                messages.error(request, "Your account is blocked. Please contact an administrator.")
                logger.warning(f"Blocked user {username} attempted to log in from IP {ip}")
                return redirect('login') 

            login(request, user)
            logger.info('User %s logged in successfully from IP %s', username, ip)

            failed_logins[username] = [] 
            return redirect('/store/profile')  

        else:
            failed_logins[username].append((ip, now()))
            messages.error(request, "Invalid username or password.")
            logger.warning('Failed login attempt for user %s from IP %s', username, ip)

            failed_attempts = [
                attempt for attempt in failed_logins[username]
                if now() - attempt[1] <= timedelta(minutes=2)
            ]

            if len(failed_attempts) >= 3:
                subject = "Suspicious Login Attempts"
                message_text = f"Username: {username}\nIP: {ip}"
                message_html = f"""
                <h1 style="color: red;">{subject}</h1>
                <p>Username: {username}</p>
                <p>IP: {ip}</p>
                """
                mail_admins(subject, message_text, html_message=message_html)
                failed_logins[username] = []  

    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'profile.html')

def claim_offer(request):
    if request.method == "POST":
        permission = Permission.objects.get(codename="vizualizeaza_oferta")
        
        request.user.user_permissions.add(permission)
        request.user.refresh_from_db()
        
        print(f"User permissions: {request.user.get_all_permissions()}")
        
        return JsonResponse({"success": True})
    
    return HttpResponseForbidden()

def oferta_view(request):
    print(f"User permissions: {request.user.get_all_permissions()}")
    
    if not request.user.has_perm("auth.vizualizeaza_oferta"):
        titlu = "Eroare afisare oferta"
        mesaj_personalizat = "Nu ai voie să vizualizezi oferta"
        return render(request, '403.html', {'titlu': titlu, 'mesaj_personalizat': mesaj_personalizat})
    
    return render(request, "oferta.html")


def add_book(request):
    if not request.user.has_perm('store.add_book'):
        titlu = "Eroare adaugare produse"
        mesaj_personalizat = "Nu ai voie să adaugi cărți"
        return render(request, '403.html', {'titlu': titlu, 'mesaj_personalizat': mesaj_personalizat})
    
    if request.method == 'POST':
        form = BookForm(request.POST)
        if not form.is_valid():
            logger.error('Error occurred while submitting book form: %s', form.errors)
            print(form.errors)
            
        if form.is_valid():
            logger.info('Book added successfully: %s', form.instance.title)
            form.save() 
            return redirect('/store/books')
    else:
        form = BookForm()

    return render(request, 'add_book.html', {'form': form})


def confirm_email(request, code):
    user_profile = get_object_or_404(UserProfile, code=code)
    if not user_profile.email_confirmed:
        user_profile.email_confirmed = True
        user_profile.save()
        return redirect('confirmation_success')
    
    return HttpResponse('Email already confirmed.')


def confirmation_success(request):
    return render(request, 'confirmation_success.html')


def send_confirmation_email(user, confirmation_link):
    """Send the confirmation email to the user, including both plain text and HTML."""
    subject = "Confirm your email"

    html_message = render_to_string('confirmation_email.html', {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'confirmation_link': confirmation_link,
    })

    plain_message = f"Hi {user.first_name},\n\nPlease confirm your email by clicking the following link: {confirmation_link}"

    email = EmailMultiAlternatives(
        subject,       
        plain_message,  
        'noreply@yourwebsite.com',  
        [user.email],        
    )

    email.attach_alternative(html_message, "text/html")
    email.send()


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            
            user.set_password(form.cleaned_data['password'])
            user.save()

            confirmation_code = str(uuid.uuid4())[:20]

            UserProfile.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone_number'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                address=form.cleaned_data['address'],
                loyalty=form.cleaned_data.get('loyalty', 0),
                code=confirmation_code
            )

            confirmation_link = f"http://127.0.0.1:8000/store/confirm_mail/{confirmation_code}/"

            send_confirmation_email(user, confirmation_link)

            return redirect('check_email')
        else:
            logger.critical('Critical error during user registration: %s')
            return JsonResponse({
                "success": False,
                "errors": form.errors
            })
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

def check_email(request):
    return render(request, 'check_email.html')


def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    
    if request.user.is_authenticated:
        Vizualizare.objects.create(
            user=request.user,
            book=book,
            viewed_at=datetime.datetime.now()  
        )
        
        n = 5
        user_views = Vizualizare.objects.filter(user=request.user).order_by('-viewed_at')
        if user_views.count() > n:
            excess_view_ids = user_views[n:].values_list('id', flat=True)
            
            Vizualizare.objects.filter(id__in=excess_view_ids).delete()

    return render(request, 'book_detail.html', {'book': book})



def save_vizualizare(user, book):
    N = 5
    
    Vizualizare.objects.create(user=user, book=book)
    vizualizari = Vizualizare.objects.filter(user=user).order_by('-viewed_at')

    if vizualizari.count() > N:
        excess_view_ids = vizualizari[N:].values_list('id', flat=True)
        Vizualizare.objects.filter(id__in=excess_view_ids).delete()


def trimite_promo_mail(promo_id):
    promotie = Promotie.objects.get(id=promo_id)
    categoriile = promotie.categoriile_promo.all()
    data_expirare = promotie.data_expirare
    subiect = promotie.subiect
    mesaj = promotie.mesaj

    utilizatori = User.objects.filter(vizualizare__book__category__in=categoriile)
    utilizatori = set(utilizatori)
    
    for user in utilizatori:
        vizualizari_categorii = Vizualizare.objects.filter(user=user, book__category__in=categoriile)
        
        if vizualizari_categorii.count() >= promotie.k_vizualizari_minime:
            context = {
                'user': user,
                'promo_name': promotie.nume,
                'data_expirare': data_expirare,
                'mesaj': mesaj,
                'discount': promotie.procent_discount
            }
            
            email_content = render_to_string('promo_email.html', context)
            
            email = EmailMessage(
                subiect,
                mesaj,  
                'noreply@yourwebsite.com', 
                [user.email]  
            )
            
            email.content_subtype = "html"
            email.body = email_content  
            
            email.send()

    

def add_promo(request):
    if request.method == 'POST':
        form = PromotieForm(request.POST)
        if form.is_valid():
            form.save()
            promo = form.instance
            trimite_promo_mail(promo.id)
            return redirect('promotii_success') 
    else:
        form = PromotieForm()
    
    return render(request, 'add_promo.html', {'form': form})


def promo_success(request):
    return render(request, 'promo_success.html')

def book_detail(request, id):
    book = Book.objects.get(id=id)
    return render(request, 'book_detail.html', {'book': book})

def author_detail(request, id):
    author = Author.objects.get(id=id)
    return render(request, 'author_detail.html', {'author': author})

def category_detail(request, id):
    category = Category.objects.get(id=id)
    return render(request, 'category_detail.html', {'category': category})

def publisher_detail(request, id):
    publisher = Publisher.objects.get(id=id)
    return render(request, 'publisher_detail.html', {'publisher': publisher})

def promotie_detail(request, id):
    promotie = Promotie.objects.get(id=id)
    return render(request, 'promotie_detail.html', {'promotie': promotie})


@login_required
def add_to_cart(request, book_id):
    if request.method == "POST":
        inventory = get_object_or_404(Inventory, book__id=book_id)
        cart, created = Cart.objects.get_or_create(user=request.user)

        quantity = int(request.POST.get('quantity', 1))  

        cart_item, created = CartItem.objects.get_or_create(cart=cart, inventory=inventory)
        if created:
            if quantity <= inventory.stock_qty:
                cart_item.quantity = quantity
            else:
                messages.error(request, "Cannot add more items than available in stock.")
                return redirect('book_detail', book_id=book_id)
        else:
            if cart_item.quantity + quantity <= inventory.stock_qty:
                cart_item.quantity += quantity
            else:
                messages.error(request, "Cannot add more items than available in stock.")
                return redirect('book_detail', book_id=book_id)

        cart_item.save()
        messages.success(request, f"{inventory.book.title} added to your cart.")
        return redirect('book_list')


@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 0))
    if 0 <= quantity <= cart_item.inventory.stock_qty:
        cart_item.quantity = quantity
        cart_item.save()
    return redirect('cart_detail')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart_detail')


@login_required
def cart_detail(request):
    cart = Cart.objects.prefetch_related('items__inventory__book').get(user=request.user)

    sort_by = request.GET.get('sort_by', '')
    items = cart.items.all()

    if sort_by == 'name_asc':
        items = items.order_by('inventory__book__title')
    elif sort_by == 'name_desc':
        items = items.order_by('-inventory__book__title')
    elif sort_by == 'price_asc':
        items = items.order_by('inventory__book__price')
    elif sort_by == 'price_desc':
        items = items.order_by('-inventory__book__price')

    for item in items:
        item.total_price = item.quantity * item.inventory.book.price 

    total = sum(item.total_price for item in items) 

    return render(request, 'cart_detail.html', {'cart': cart, 'sorted_items': items, 'total': total})


@login_required
def place_order(request):
    cart = get_object_or_404(Cart, user=request.user) 
    if not cart.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart_detail')

    total_price = sum(item.quantity * item.inventory.book.price for item in cart.items.all())
    order = Order.objects.create(user=request.user, total_price=total_price)

    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            inventory=cart_item.inventory,
            quantity=cart_item.quantity,
            price=cart_item.inventory.book.price
        )
        cart_item.inventory.stock_qty -= cart_item.quantity
        cart_item.inventory.save()

    cart.items.all().delete()

    pdf_path = generate_invoice(order)

    send_invoice_email(order, pdf_path)

    messages.success(request, "Order placed successfully! An invoice has been sent to your email.")
    return redirect('cart_detail')

def generate_invoice(order):
    user_folder = f"temporar-facturi/{order.user.username}/"
    os.makedirs(user_folder, exist_ok=True)
    pdf_path = os.path.join(user_folder, f"factura-{int(time.time())}.pdf")

    with open(pdf_path, "wb") as pdf_file:
        c = canvas.Canvas(pdf_file, pagesize=letter)

        c.drawString(100, 800, f"Invoice for Order {order.id}")
        c.drawString(100, 780, f"Date: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        c.drawString(100, 760, f"Customer: {order.user.username} ({order.user.email})")

        y = 720
        cnt = 0
        for item in order.items.all():
            book_title = item.inventory.book.title
            book_link = item.inventory.book.get_absolute_url()
            cnt += item.quantity

            c.drawString(100, y, f"{book_title} (x{item.quantity}) - ${item.price}")

            c.linkURL(book_link, (100, y-5, 400, y+10), relative=1)

            y -= 20

        y -= 20
        c.drawString(100, y, f"Total: ${order.total_price}")
        c.drawString(100, y - 20, f"Total items: {cnt}")
        c.drawString(100, y - 40, f"Customer support: izabelajilavu@gmail.com")
        c.save()

    return pdf_path


def send_invoice_email(order, pdf_path):
    subject = f"Invoice for Order {order.id}"
    message = render_to_string('email/invoice_email.html', {'order': order}) 
    email = EmailMessage(
        subject,
        message,  
        'admin@yourwebsite.com',
        [order.user.email],
    )
    email.content_subtype = "html" 
    email.attach_file(pdf_path)
    email.send()


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'password_change.html'
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        print("Password changed successfully!")
        return super().form_valid(form)