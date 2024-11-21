from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('books/', views.book_list, name='book_list'), 
    path('contact/', views.contact_view, name='contact'),
    path('login/', views.login_view, name='login'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('add_book/', views.add_book, name='add_book'),
]
