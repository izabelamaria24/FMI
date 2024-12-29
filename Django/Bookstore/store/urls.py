from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('books/', views.book_list, name='book_list'), 
    path('contact/', views.contact_view, name='contact'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('add_book/', views.add_book, name='add_book'),
    path('confirm_mail/<str:code>/', views.confirm_email, name='confirm_email'),
    path('confirmation_success/', views.confirmation_success, name='confirmation_success'),
    path('check_email/', views.check_email, name='check_email'),
    path('books/<int:id>/', views.book_detail, name='book_detail'),
    path('promotii/', views.add_promo, name='add_promo'),
    path('promotii/success/', views.promo_success, name='promotii_success'),
    path("claim-offer/", views.claim_offer, name="claim_offer"),
    path("oferta/", views.oferta_view, name="oferta"),
    path('book/<int:id>/', views.book_detail, name='book_detail'),
    path('author/<int:id>/', views.author_detail, name='author_detail'),
    path('category/<int:id>/', views.category_detail, name='category_detail'),
    path('publisher/<int:id>/', views.publisher_detail, name='publisher_detail'),
    path('promotie/<int:id>/', views.promotie_detail, name='promotie_detail'),
]
