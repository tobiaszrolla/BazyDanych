from django.test import TestCase,Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Samochód, Sala, Użytkownik
import json
from .create_admin import create_admin

class ModifyViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        create_admin()
        # Tworzenie testowego samochodu
        self.car = Samochód.objects.create(
            registration_number="ABC123",
            model="Toyota",
            production_year="2020",
            availability=True
        )

        # Tworzenie testowej sali
        self.room = Sala.objects.create(
            nazwa="Sala A",
            availability=True,
            capacity=30
        )
        self.instruktor = self.User.objects.create_user(
            username="instruktor@test.com",
            email="instruktor@test.com",
            password="strong_password",
            typ_użytkownika="instruktor"
        )

        # Tworzymy adres URL do testów
        self.modify_car_url = reverse('modify_car', kwargs={'registration_number': self.car.registration_number})
        self.modify_room_url = reverse('modify_room', kwargs={'nazwa': self.room.nazwa})
        self.modify_user_url = reverse('modify_user', kwargs={'email': self.instruktor.email})

    def test_modify_car_success(self):
        data = {
            "model": "Honda",
            "production_year": "2022"
        }

        self.client.login(username="admin", password="strong_password")  # Logowanie admina
        response = self.client.put(self.modify_car_url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_modify_car_not_found(self):
        data = {
            "model": "Honda"
        }

        self.client.login(username="admin", password="strong_password")
        response = self.client.put(reverse('modify_car', kwargs={'registration_number': "NONEXISTENT"}), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_modify_car_invalid_method(self):
        data = {
            "model": "Honda"
        }

        self.client.login(username="admin", password="strong_password")
        response = self.client.post(self.modify_car_url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 405)

    def test_modify_room_success(self):
        data = {
            "capacity": 30
        }

        self.client.login(username="admin", password="strong_password")
        response = self.client.put(self.modify_room_url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_modify_room_not_found(self):
        data = {
            "capacity": 30
        }

        self.client.login(username="admin", password="strong_password")
        response = self.client.put(reverse('modify_room', kwargs={'nazwa': "NONEXISTENT"}), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_modify_room_invalid_method(self):
        data = {
            "capacity": 30
        }

        self.client.login(username="admin", password="strong_password")
        response = self.client.post(self.modify_room_url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 405)

    def test_modify_user_success(self):
        data = {
            "imię": "John",
            "nazwisko": "Doe",
            "nrTelefonu": "123456789",
            "data_urodzenia": "1990-01-01",
            "typ_użytkownika": "instruktor"
        }

        self.client.login(username="admin", password="strong_password")
        response = self.client.put(self.modify_user_url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_modify_user_not_found(self):
        data = {
            "imię": "John"
        }

        self.client.login(username="admin", password="strong_password")
        response = self.client.put(reverse('modify_user', kwargs={'email': "nonexistent@example.com"}), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_modify_user_invalid_method(self):
        data = {
            "imię": "John"
        }

        self.client.login(username="admin", password="strong_password")
        response = self.client.post(self.modify_user_url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 405)
