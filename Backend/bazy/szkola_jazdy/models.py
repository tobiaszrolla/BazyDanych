from django.contrib.auth.models import AbstractUser
from django.db import models


class Sala(models.Model):
    pojemność = models.IntegerField()
    dostępność = models.BooleanField()

    def __str__(self):
        return f"Sala {self.id}: pojemność {self.pojemność}, dostępność {self.dostępność}"


class Samochód(models.Model):
    numer_rejestracyjny = models.CharField(max_length=20)
    model = models.CharField(max_length=50)
    rok_produkcji = models.CharField(max_length=4)
    dostępność = models.BooleanField()

    def __str__(self):
        return f"Samochód {self.model} ({self.numer_rejestracyjny})"


'''class Użytkownik(models.Model):
    TYP_UŻYTKOWNIKA = [
        ('kursant', 'Kursant'),
        ('instruktor', 'Instruktor'),
    ]

    email = models.EmailField(unique=True)
    nrTelefonu = models.CharField(max_length=15, null=True, blank=True)
    imię = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    data_urodzenia = models.DateField(null=True, blank=True)
    typ_użytkownika = models.CharField(max_length=10, choices=TYP_UŻYTKOWNIKA)
    godziny_wyjeżdżone = models.IntegerField(default=0)
    posiadane_lekcje = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.imię} {self.nazwisko} ({self.typ_użytkownika})"
'''
#testujemy Użytkownika jako Abstract User
class Użytkownik(AbstractUser):
    TYP_UŻYTKOWNIKA = [
        ('kursant', 'Kursant'),
        ('instruktor', 'Instruktor'),
    ]

    email = models.EmailField(unique=True)
    nrTelefonu = models.CharField(max_length=15, null=True, blank=True)
    imię = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    data_urodzenia = models.DateField(null=True, blank=True)
    typ_użytkownika = models.CharField(max_length=10, choices=TYP_UŻYTKOWNIKA)
    godziny_wyjeżdżone = models.IntegerField(default=0)
    posiadane_lekcje = models.IntegerField(default=0)

    #dodanie do grup i ustawienie uprawnień encji
    groups = models.ManyToManyField('auth.Group', related_name='szkola_jazdy_użytkownicy', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='szkola_jazdy_użytkownicy', blank=True)

    def __str__(self):
        return f"{self.imię} {self.nazwisko} ({self.typ_użytkownika})"
class Zajęcia(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.SET_NULL, null=True, blank=True)
    samochód = models.ForeignKey(Samochód, on_delete=models.SET_NULL, null=True, blank=True)
    kursanci = models.ManyToManyField('Użytkownik', through='KursanciNaZajęciach') #odwołanie do tablicy pośredniej
    instruktor = models.ForeignKey(Użytkownik, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='instruktor')
    godzina_rozpoczęcia = models.TimeField()
    godzina_zakończenia = models.TimeField()

    def __str__(self):
        return f"Zajęcia {self.id} - {self.godzina_rozpoczęcia} - {self.godzina_zakończenia}"


class KursanciNaZajęciach(models.Model):
    użytkownik = models.ForeignKey(Użytkownik, on_delete=models.CASCADE) #CASSCADE usunie powiązania gdy usuniemy użytkownika albo zajęcia
    zajęcia = models.ForeignKey(Zajęcia, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('użytkownik', 'zajęcia')
