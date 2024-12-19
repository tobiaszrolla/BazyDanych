from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Zajęcia, Sala, Samochód, Użytkownik
from django.db.models import Count
class DostępneZajęciaTestCase(TestCase):
    def setUp(self):
        self.kursant = Użytkownik.objects.create_user(
            username="kursant@test.com",
            email="kursant@test.com",
            password="strong_password",
            typ_użytkownika="kursant",
            kategoria = "B"
        )

        self.instruktor = Użytkownik.objects.create_user(
            username="instruktor@test.com",
            email="instruktor@test.com",
            password="strong_password",
            typ_użytkownika="instruktor"
        )
        self.car = Samochód.objects.create(
            registration_number="ABC123",
            model="Toyota",
            production_year="2020",
            availability=True,
        )

        self.room = Sala.objects.create(
            nazwa="Sala A",
            availability=True,
            capacity=30
        )

        self.zajęcia1 = Zajęcia.objects.create(
            sala=self.room,
            samochód=None,
            dostempne_miejsca=5,
            data="2024-12-20",
            godzina_rozpoczęcia="10:00",
            godzina_zakończenia="11:00",
            instruktor=self.instruktor,
            kategoria="B"
        )

        self.zajęcia2 = Zajęcia.objects.create(
            samochód=self.car,
            dostempne_miejsca=1,
            data="2024-12-20",
            godzina_rozpoczęcia="11:00",
            godzina_zakończenia="12:00",
            instruktor=self.instruktor,
            kategoria="B"
        )

        self.client.login(username="kursant@test.com", password="strong_password")
        self.url = reverse('dostępne_zajęcia')

    def test_success(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(len(data), 2)
        data = response.json()
        print("Brak dostemnych miejsc",data)
    def test_brak_dostępnych_miejsc(self):
        self.zajęcia2.dostempne_miejsca = 0
        self.zajęcia2.save()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(len(data), 1)
        data = response.json()
        print("Brak dostemnych miejsc",data)
    def test_brak_uprawnien(self):
        self.client.logout()
        self.client.login(username="instruktor@test.com", password="strong_password")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 400)
        data = response.json()
    def test_inna_kategoria(self):
        self.zajęcia2.kategoria = "C"
        self.zajęcia2.save()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(len(data), 1)
        data = response.json()
        print("Brak dostemnych miejsc", data)


