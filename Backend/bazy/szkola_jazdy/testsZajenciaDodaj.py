from django.test import TestCase,Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Samochód, Sala, Użytkownik, Zajęcia
import json
from .create_admin import create_admin

class ZajenciaTasteCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        create_admin()

        #instruktor dla testu weryfikacji
        self.instruktor = self.User.objects.create_user(
            username="instruktor@test.com",
            email="instruktor@test.com",
            password="strong_password",
            typ_użytkownika="instruktor"
        )

        self.kursant = self.User.objects.create_user(
            username="kursant@test.com",
            email="kursant@test.com",
            password="strong_password",
            typ_użytkownika="kursant"
        )

        self.car = Samochód.objects.create(
            registration_number="ABC123",
            model="Toyota",
            production_year="2020",
            availability=True
        )


        self.room = Sala.objects.create(
            nazwa="Sala A",
            availability=True,
            capacity=30
        )
        self.add_zajencia_url = reverse('add_zajęcia')
    def test_add_zajencia_success_car(self):
        self.client.login(username="instruktor@test.com", password="strong_password")
        data = {
            'numer_rejestracyjny': self.car.registration_number,
            'godzina_rozpoczęcia': "16:00",
            'godzina_zakończenia': "17:00",
            'kategoria': "B",
            'data' : "2025-01-01",
        }
        response = self.client.post(self.add_zajencia_url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        print(Zajęcia.objects.all().first().dostempne_miejsca)
    def test_add_zajencia_success_room(self):
        self.client.login(username="instruktor@test.com", password="strong_password")
        data = {
            'nazwa_sali': self.room.nazwa,
            'godzina_rozpoczęcia': "16:00",
            'godzina_zakończenia': "17:00",
            'kategoria': "B",
            'data' : "2025-01-01",
        }
        response = self.client.post(self.add_zajencia_url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        print(Zajęcia.objects.all().first().dostempne_miejsca)
    def test_add_zajencia_Admin(self):
        self.client.login(username="admin", password="strong_password")
        data = {
            'numer_rejestracyjny': self.car.registration_number,
            'godzina_rozpoczęcia': "16:00",
            'godzina_zakończenia': "17:00",
            'kategoria': "B",
            'data': "2025-01-01",
        }
        response = self.client.post(self.add_zajencia_url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 403)
    def test_add_zajencia_Kursant(self):
        self.client.login(username="kursant@test.com", password="strong_password")
        data = {
            'numer_rejestracyjny': self.car.registration_number,
            'godzina_rozpoczęcia': "16:00",
            'godzina_zakończenia': "17:00",
            'kategoria': "B",
            'data': "2025-01-01",
        }
        response = self.client.post(self.add_zajencia_url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 403)