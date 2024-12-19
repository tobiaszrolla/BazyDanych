from django.test import TestCase,Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Samochód, Sala, Użytkownik
import json
from .create_admin import create_admin

class DeleteViewsTestCase(TestCase):
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
        self.kursant = self.User.objects.create_user(
            username="kursant@test.com",
            email="kursant@test.com",
            password="strong_password",
            typ_użytkownika="kursant"
        )

        # Tworzymy adres URL do testów
        self.delete_car_url = reverse('delete_car', kwargs={'registration_number': self.car.registration_number})
        self.delete_room_url = reverse('delete_room', kwargs={'nazwa': self.room.nazwa})
        self.delete_user_url = reverse('delete_user', kwargs={'email': self.kursant.email})

    def test_delete_car_success(self):
        self.client.login(username="admin", password="strong_password")
        response = self.client.delete(self.delete_car_url, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_delete_car_noAdmin(self):
        self.client.login(username="instruktor@test.com", password="strong_password")
        response = self.client.delete(self.delete_car_url, content_type="application/json")
        self.assertEqual(response.status_code, 302)

    def test_delete_room_success(self):
        self.client.login(username="admin", password="strong_password")
        response = self.client.delete(self.delete_room_url, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_delete_room_noAdmin(self):
        self.client.login(username="instruktor@test.com", password="strong_password")
        response = self.client.delete(self.delete_room_url, content_type="application/json")
        self.assertEqual(response.status_code, 302)

    def test_delete_user_success(self):
        self.client.login(username="admin", password="strong_password")
        response = self.client.delete(self.delete_user_url, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_delete_user_noAdmin(self):
        self.client.login(username="instruktor@test.com", password="strong_password")
        response = self.client.delete(self.delete_user_url, content_type="application/json")
        self.assertEqual(response.status_code, 302)