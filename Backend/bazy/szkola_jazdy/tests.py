from django.test import TestCase, Client
import json
from django.contrib.auth import get_user_model

class RegisterTest(TestCase):  # Klasa testowa dziedziczy po TestCase
    #Metody pomocnicze
    def register_user(self,
                      email,
                      password,
                      data_urodzenia,
                      typ_użytkownika,
                      ):
        client = Client()
        data = {
            'email': email,
            'nrTelefonu': '123456789',
            'imię': 'User',
            'nazwisko': 'User',
            'data_urodzenia': data_urodzenia,
            'typ_użytkownika': typ_użytkownika,
            'password': password,
        }
        response = client.post(
            '/register/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        return response

    def login_user(self, email, password):
        client = Client()
        data = {
            'email': email,
            'password': password,
        }
        response = client.post(
            '/login/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        return response
    def test_register(self):
        client = Client()
        response = self.register_user('test@domena.com','strong_password', '2003-03-03','kursant')
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Użytkownik został zarejestrowany pomyślnie!')
        user_from_db = get_user_model().objects.get(email='test@domena.com')
        print(f'User ID: {user_from_db.id}')
        print(f'User Email: {user_from_db.email}')
        print(f'User Name: {user_from_db.imię} {user_from_db.nazwisko}')
        print(f'User Phone: {user_from_db.nrTelefonu}')
        print(f'User Type: {user_from_db.typ_użytkownika}')
        print(f'User Date of Birth: {user_from_db.data_urodzenia}')
        print(response_data['message'], '\n')

    def test_login(self):
        # Rejestracja użytkownika
        self.register_user('test@domena.com', 'strong_password', '2003-03-03', 'kursant')
        user_from_db = get_user_model().objects.get(email='test@domena.com')
        print(f'User ID: {user_from_db.id}')
        print(f'User Email: {user_from_db.email}')
        print(f'User Name: {user_from_db.imię} {user_from_db.nazwisko}')
        print(f'User Phone: {user_from_db.nrTelefonu}')
        print(f'User Type: {user_from_db.typ_użytkownika}')
        print(f'User Date of Birth: {user_from_db.data_urodzenia}')
        # Logowanie użytkownika
        response = self.login_user('test@domena.com', 'strong_password')
        response_data = response.json()

        # Sprawdzanie odpowiedzi
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Zalogowano pomyślnie.')
        print(response_data['message'], '\n')