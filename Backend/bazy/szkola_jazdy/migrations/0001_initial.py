# Generated by Django 5.1.4 on 2024-12-10 15:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sala',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pojemność', models.IntegerField()),
                ('dostępność', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Samochód',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numer_rejestracyjny', models.CharField(max_length=20)),
                ('model', models.CharField(max_length=50)),
                ('rok_produkcji', models.CharField(max_length=4)),
                ('dostępność', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Użytkownik',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('nrTelefonu', models.CharField(blank=True, max_length=15, null=True)),
                ('imię', models.CharField(max_length=50)),
                ('nazwisko', models.CharField(max_length=50)),
                ('data_urodzenia', models.DateField(blank=True, null=True)),
                ('typ_użytkownika', models.CharField(choices=[('kursant', 'Kursant'), ('instruktor', 'Instruktor')], max_length=10)),
                ('godziny_wyjeżdżone', models.IntegerField(default=0)),
                ('posiadane_lekcje', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='KursanciNaZajęciach',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('użytkownik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='szkola_jazdy.użytkownik')),
            ],
        ),
        migrations.CreateModel(
            name='Zajęcia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('godzina_rozpoczęcia', models.TimeField()),
                ('godzina_zakończenia', models.TimeField()),
                ('instruktor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='instruktor', to='szkola_jazdy.użytkownik')),
                ('kursanci', models.ManyToManyField(through='szkola_jazdy.KursanciNaZajęciach', to='szkola_jazdy.użytkownik')),
                ('sala', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='szkola_jazdy.sala')),
                ('samochód', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='szkola_jazdy.samochód')),
            ],
        ),
        migrations.AddField(
            model_name='kursancinazajęciach',
            name='zajęcia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='szkola_jazdy.zajęcia'),
        ),
        migrations.AlterUniqueTogether(
            name='kursancinazajęciach',
            unique_together={('użytkownik', 'zajęcia')},
        ),
    ]
