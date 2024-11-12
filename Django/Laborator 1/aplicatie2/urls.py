from django.urls import path
from . import views

urlpatterns = [
    path('prajituri/', views.afisare_prajituri, name='prajituri_list'),
]