from django.test import TestCase, Client
import json


class RegisterTest(TestCase):  # Klasa testowa dziedziczy po TestCase
    def test_json_post(self):
        client = Client()
        data = {
            'email': 'test@domena.com',
            'nrTelefonu': '123456789',
            'imię': 'User',
            'nazwisko': 'User',
            'data_urodzenia': '2003-03-03',  # Poprawny format daty
            'typ_użytkownika': 'kursant',  # Dodano brakujący przecinek
            'password': 'strong_password',
        }

        # Wysyłanie żądania POST
        response = client.post(
            '/register/',  # Pełna ścieżka URL
            data=json.dumps(data),
            content_type='application/json'
        )

        # Sprawdzenie kodu statusu HTTP
        self.assertEqual(response.status_code, 201)

        # Sprawdzenie treści odpowiedzi
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Użytkownik został zarejestrowany pomyślnie!')
from django.test import TestCase

# Create your tests here.
