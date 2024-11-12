from django.shortcuts import render
from datetime import date
from django.http import HttpResponse

nr_accesari = 0
valori_stocate = []

def index(request):
    global nr_accesari
    nr_accesari += 1
    return HttpResponse("Primul raspuns")


def mesaj(request):
    global nr_accesari
    nr_accesari += 1
    return HttpResponse("Buna ziua!")

def data(request):
    global nr_accesari
    nr_accesari += 1
    return HttpResponse(date.today())

def accesari(request):
    global nr_accesari
    return HttpResponse(nr_accesari)

def suma(request):
    a = int(request.GET.get("a", 0))
    b = int(request.GET.get("b", 0))
    
    return HttpResponse(a + b)


def text(request):
    global valori_stocate
    t = request.GET.get('t', '')
    
    if t and t.isalpha():
        valori_stocate.append(t)
    
    return HttpResponse(', '.join(valori_stocate))


def nr_parametri(request):
    return HttpResponse(len(valori_stocate))


def operatie(request):
    global valori_stocate
    if len(valori_stocate) < 2:
        return HttpResponse("Trebuie sa avem minim 2 parametri")
    
    op = request.GET.get('op', '')
    if op not in ['+', '-', '*', '/']:
        return HttpResponse("Operatie invalida")

    a = float(valori_stocate[0])
    b = float(valori_stocate[1])
    
    if op == '+':
        result = a + b
    elif op == '-':
        result = a - b
    elif op == '*':
        result = a * b
    elif op == '/':
        if b == 0:
            return HttpResponse("Nu se poate imparti la 0")
        result = a / b
        
    return HttpResponse(f"{a} {op} {b} = {result}")


accesari_aduna_numere = 0
suma_aduna_numere = 0

def aduna_numere(request, page_number):
    global accesari_aduna_numere
    global suma_aduna_numere
    accesari_aduna_numere += 1
    suma_aduna_numere += int(page_number)
    return HttpResponse(f"numar cereri:{accesari_aduna_numere} suma numere: {suma_aduna_numere}")


def afiseaza_liste(request):
    query_params = {key: request.GET.getlist(key) for key in request.GET}
    
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Query Parameters</title>
    </head>
    <body>
        <h1>Query Parameters</h1>
        <ul>
    """

    for key, values in query_params.items():
        html += f"<li><strong>{key}:</strong><ul>"
        for value in values:
            html += f"<li>{value}</li>"
        html += "</ul></li>"

    html += """
        </ul>
    </body>
    </html>
    """
    
    return HttpResponse(html)


cnt_numere = 0

def numara_nume(request, nume):
    global cnt_numere
    cnt_numere += 1
    
    return HttpResponse(f"Numar nume corecte: {cnt_numere}")


def cauta_subsir(request, subsir):
    return HttpResponse(len(subsir))


from django.shortcuts import render

def operatii(request):
    d = {
        "lista": [
            {"a": 10, "b": 20, "operatie": "suma"},
            {"a": 40, "b": 20, "operatie": "diferenta"},
            {"a": 25, "b": 30, "operatie": "suma"},
            {"a": 40, "b": 30, "operatie": "diferenta"},
            {"a": 100, "b": 50, "operatie": "diferenta"},
        ]
    }

    for item in d["lista"]:
        if item["operatie"] == "suma":
            item["rezultat"] = item["a"] + item["b"]
        elif item["operatie"] == "diferenta":
            item["rezultat"] = item["a"] - item["b"]

    return render(request, 'operatii.html', {'data': d})

