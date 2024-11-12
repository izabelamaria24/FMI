from django.urls import path, re_path
from . import views

urlpatterns = [
	path("", views.index, name="index"),
    path("mesaj", views.mesaj, name="mesaj"),
    path("data", views.data, name="data"),
    path("accesari", views.accesari, name="accesari"),
    path("suma", views.suma, name="suma"),
    path("text", views.text, name="text"),
    path("nr_parametri", views.nr_parametri, name="nr_parametri"),
    re_path(r'^pag/[a-zA-Z]*(\d+)/$', views.aduna_numere, name='aduna_numere'),
    path("liste", views.afiseaza_liste, name="afiseaza_liste"),
    re_path(r'^numara_nume/[A-Z][a-z]+(-[A-Z][a-z]+)?\+[A-Z][a-z]*$', views.numara_nume, name="numara_nume"),
    re_path(r'^subsir/(\d+[ab]*\d+)$', views.cauta_subsir, name="cauta_subsir"),    
    path("operatii", views.operatii, name="operatii"),
]
