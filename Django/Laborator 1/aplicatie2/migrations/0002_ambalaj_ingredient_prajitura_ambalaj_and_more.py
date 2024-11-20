# Generated by Django 5.1 on 2024-10-31 13:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicatie2', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ambalaj',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nume', models.CharField(max_length=20, unique=True)),
                ('material', models.CharField(choices=[('plastic', 'Plastic'), ('hartie', 'Hartie'), ('carton', 'Carton')], max_length=10)),
                ('pret', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nume', models.CharField(max_length=30, unique=True)),
                ('calorii', models.PositiveIntegerField()),
                ('unitate', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='prajitura',
            name='ambalaj',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prajituri', to='aplicatie2.ambalaj'),
        ),
        migrations.AddField(
            model_name='prajitura',
            name='ingrediente',
            field=models.ManyToManyField(blank=True, related_name='prajituri', to='aplicatie2.ingredient'),
        ),
    ]