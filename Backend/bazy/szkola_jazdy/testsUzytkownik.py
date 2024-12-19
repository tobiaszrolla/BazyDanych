from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.http import urlsafe_base64_encode
from django.core import mail
import json
from datetime import datetime

# Zakładam, że masz model użytkownika "Użytkownik"
from .models import Użytkownik, Zajęcia


class ViewTests(TestCase):
    def setUp(self):
        self.user_data = {
            "email": "testuser@example.com",
            "username": "testuser@example.com",
            "password": "strongpassword123",
            "imię": "Jan",
            "nazwisko": "Kowalski",
            "data_urodzenia": "2000-01-01",
            "typ_użytkownika": "kursant"
        }

    def test_register_success(self):
        response = self.client.post(reverse('register'), data=json.dumps(self.user_data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], "Użytkownik został zarejestrowany pomyślnie!")

    def test_register_user_exists(self):
        Użytkownik.objects.create_user(username="testuser@example.com",email="testuser@example.com", password="existingpassword123")
        response = self.client.post(reverse('register'), data=json.dumps(self.user_data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "Email jest już zajęty.")

    def test_register_missing_fields(self):
        incomplete_data = {key: value for key, value in self.user_data.items() if key != "email"}
        response = self.client.post(reverse('register'), data=json.dumps(incomplete_data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "Brak wymaganych danych.")

    def test_login_success(self):
        Użytkownik.objects.create_user(**self.user_data)
        login_data = {"email": "testuser@example.com", "password": "strongpassword123"}
        response = self.client.post(reverse('login'), data=json.dumps(login_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "Zalogowano pomyślnie.")

    def test_login_invalid_credentials(self):
        login_data = {"email": "testuser@example.com", "password": "wrongpassword"}
        response = self.client.post(reverse('login'), data=json.dumps(login_data), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()['error'], "Nieprawidłowy email lub hasło.")

    def test_logout_success(self):
        user = Użytkownik.objects.create_user(**self.user_data)
        self.client.login(username=user.email, password="strongpassword123")
        response = self.client.post(reverse('logout'), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "Wylogowano pomyślnie.")

    def test_reset_password_success(self):
        Użytkownik.objects.create_user(**self.user_data)
        reset_data = {"email": "testuser@example.com"}
        response = self.client.post(reverse('reset_password_request'), data=json.dumps(reset_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "Wysłano e-mail z nowym hasłem.")
        self.assertEqual(len(mail.outbox), 1)

    def test_reset_password_user_not_found(self):
        reset_data = {"email": "nonexistentuser@example.com"}
        response = self.client.post(reverse('reset_password_request'), data=json.dumps(reset_data), content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], "Nie znaleziono użytkownika z podanym adresem e-mail.")

    def test_zapisz_na_kurs_success(self):
        Użytkownik.objects.create_user(**self.user_data)
        user = Użytkownik.objects.get(email="testuser@example.com")
        user.typ_użytkownika = "kursant"
        user.save()

        zajęcia = Zajęcia.objects.create(
            sala=None, samochód=None, dostempne_miejsca=5,
            data="2024-12-20", godzina_rozpoczęcia="10:00", godzina_zakończenia="11:00"
        )
        self.client.login(username="testuser@example.com", password="strongpassword123")
        data = {"kategoria": "B", "lekcje_teoretyczne": 2, "lekcje_praktyczne": 5}
        response = self.client.put(reverse('zapisz_na_kurs'), data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "Zapis na kurs zakończony sukcesem.")

    def test_zapisz_na_kurs_not_authenticated(self):
        data = {"kategoria": "B", "lekcje_teoretyczne": 2, "lekcje_praktyczne": 5}
        response = self.client.put(reverse('zapisz_na_kurs'), data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()['error'], "Musisz być zalogowany, aby stworzyć zajęcia.")

    def test_zapisz_na_kurs_wrong_user_type(self):
        admin_user = Użytkownik.objects.create_superuser(**self.user_data)
        self.client.login(username="testuser@example.com", password="strongpassword123")
        data = {"kategoria": "B", "lekcje_teoretyczne": 2, "lekcje_praktyczne": 5}
        response = self.client.put(reverse('zapisz_na_kurs'), data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['error'], "Musisz być pracownikiem, aby tworzyć zajęcia.")

    def test_zapisz_na_kurs_invalid_data(self):
        Użytkownik.objects.create_user(**self.user_data)
        user = Użytkownik.objects.get(email="testuser@example.com")
        self.client.login(username="testuser@example.com", password="strongpassword123")
        data = {"kategoria": "B"}
        response = self.client.put(reverse('zapisz_na_kurs'), data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "Brak wymaganych danych.")

