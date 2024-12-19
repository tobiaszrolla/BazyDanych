from django.test import TestCase,Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Samochód, Sala, Użytkownik
import json
from .create_admin import create_admin

class AddingTasteCase(TestCase):
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
        self.add_car_url = reverse('add_car')
        self.add_room_url = reverse('add_room')
    def test_add_car_success(self):
        data = {
            "registration_number": "123456",
            "model": "Honda",
            "availability": True,
            'production_year': 2020
        }
        self.client.login(username="admin", password="strong_password")
        response = self.client.post(self.add_car_url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_add_car_notAdmin(self):
        data = {
            "registration_number": "123456",
            "model": "Honda",
            "availability": True,
            'production_year': 2020
        }
        self.client.login(username="instruktor@test.com", password="strong_password")
        response = self.client.post(self.add_car_url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 302)

    def test_add_car_incoractData(self):
        data = {
            "registration_number": "123456",
        }
        self.client.login(username="admin", password="strong_password")
        response = self.client.post(self.add_car_url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_add_room_success(self):
        data = {
            "nazwa": "C123",
            "availability": True,
            'capacity': 20
        }
        self.client.login(username="admin", password="strong_password")
        response = self.client.post(self.add_room_url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_add_room_notAdmin(self):
        data = {
            "nazwa": "C123",
            "availability": True,
            'capacity': 20
        }
        self.client.login(username="instruktor@test.com", password="strong_password")
        response = self.client.post(self.add_room_url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 302)
    def test_add_room_incoractData(self):
        data = {
            "nazwa": "C123",
        }
        self.client.login(username="admin", password="strong_password")
        response = self.client.post(self.add_room_url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)

