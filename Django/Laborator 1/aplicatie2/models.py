from django.db import models

class Prajitura(models.Model):
    CATEGORII = [
        ('comanda speciala', 'Comanda Speciala'),
        ('aniversara', 'Aniversara'),
        ('editie limitata', 'Editie Limitata'),
        ('pentru copii', 'Pentru Copii'),
        ('dietetica', 'Dietetica'),
        ('comuna', 'Comuna'),
    ]

    TIPURI_PRODUSE = [
        ('cofetarie', 'Cofetarie'),
        ('patiserie', 'Patiserie'),
        ('gelaterie', 'Gelaterie'),
    ]

    id = models.AutoField(primary_key=True)
    nume = models.CharField(max_length=50, unique=True)
    descriere = models.TextField(blank=True, null=True)
    pret = models.DecimalField(max_digits=8, decimal_places=2)
    gramaj = models.PositiveIntegerField()
    tip_produs = models.CharField(max_length=20, choices=TIPURI_PRODUSE, default='cofetarie')
    calorii = models.PositiveIntegerField()
    categorie = models.CharField(max_length=20, choices=CATEGORII, default='comuna')
    pt_diabetici = models.BooleanField(default=False)
    imagine = models.URLField(max_length=300, blank=True, null=True)
    data_adaugare = models.DateTimeField(auto_now_add=True)
    
    ambalaj = models.ForeignKey('Ambalaj', related_name='prajituri', on_delete=models.CASCADE, null=True)
    ingrediente = models.ManyToManyField('Ingredient', related_name='prajituri', blank=True)

    def __str__(self):
        return self.nume


class Ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    nume = models.CharField(max_length=30, unique=True)
    calorii = models.PositiveIntegerField()
    unitate = models.CharField(max_length=10)

    def __str__(self):
        return self.nume


class Ambalaj(models.Model):
    id = models.AutoField(primary_key=True)
    nume = models.CharField(max_length=20, unique=True)
    material = models.CharField(max_length=10, choices=[('plastic', 'Plastic'), ('hartie', 'Hartie'), ('carton', 'Carton')])
    pret = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.nume
