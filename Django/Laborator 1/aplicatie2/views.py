from django.shortcuts import render
from .models import Prajitura

def afisare_prajituri(request):
    prajituri = Prajitura.objects.all()
    return render(request, 'prajituri_list.html', {'prajituri': prajituri})
