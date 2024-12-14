from http.client import responses

from django.test import TestCase, Client
import json
from django.contrib.auth import get_user_model
from .models import Samochód, Sala
from .create_admin import create_admin

class RegisterTest(TestCase):  # Klasa testowa dziedziczy po TestCase
    #Metody pomocnicze
    def delete_car(self, registration_number):
        client = Client()
        response = client.delete(f'/delete_car/{registration_number}/')
        print(f"Status code for deleting car: {response.status_code}")
        print(f"Response content: {response.content.decode()}")
        return response

    def delete_room(self, room_name):
        client = Client()
        response = client.delete(f'/delete_room/{room_name}/')
        print(f"Status code for deleting room: {response.status_code}")
        print(f"Response content: {response.content.decode()}")
        return response

    def delete_user(self, email):
        client = Client()
        response = client.delete(f'/delete_user/{email}/')
        print(f"Status code for deleting user: {response.status_code}")
        print(f"Response content: {response.content.decode()}")
        return response

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
        return response
    def add_sala(self, capacity, availability, nazwa):
        client = Client()
        data = {
            'capacity': capacity,
            'availability': availability,
            'nazwa': nazwa,
        }
        response = client.post(
            '/add_room/',
            data=json.dumps(data),
            content_type='application/json'
        )
        print(response.status_code)
        return response
    def add_car(self, registration_number, model, production_year, availability):
        client = Client()
        data = {
            'registration_number': registration_number,
            'model': model,
            'production_year': production_year,
            'availability': availability
        }
        response = client.post(
            '/add_car/',
            data=json.dumps(data),
            content_type='application/json'
        )
        print(response.status_code)
        return response
    def test_register(self):
        client = Client()
        response = self.register_user('test@domena.com','strong_password', '2003-03-03','kursant')
        self.assertEqual(response.status_code, 201)
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
        # Logowanie użytkownika
        response = self.login_user('test@domena.com', 'strong_password')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        # Sprawdzanie odpowiedzi
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Zalogowano pomyślnie.')
        print(response_data['message'], '\n')

    def test_uniqemail(self):
        #1 user
        response = self.register_user('test@domena.com', 'strong_password', '2003-03-03', 'kursant')
        self.assertEqual(response.status_code, 201)
        #2 user z takim samym mailem
        response = self.register_user('test@domena.com', 'strong_password', '2003-03-03', 'kursant')
        #wypisanie błędu
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Email jest już zajęty.')
        print(response_data['error'], "\n Faktycznie nieda się utworzyć takich samych maili.\n")
    def test_wrong_password(self):
        #rejestracja
        response = self.register_user('test@domena.com', 'strong_password', '2003-03-03', 'kursant')
        self.assertEqual(response.status_code, 201)
        #logowanie z błędnym hasłem
        response = self.login_user('test@domena.com', 'wrong_password')
        self.assertEqual(response.status_code, 401)
        response_data = response.json()
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Nieprawidłowy email lub hasło.')
        print(response_data['error'], "\n Wykryto nieprawidłowe hasło.\n")
    def test_newSala(self):
        response = self.add_sala(13,True,'c123')
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Sala została dodana pomyślnie!')
        print(response_data['message'], 'Sala została dodana pomyślnie!\n')
    def test_newSamochód(self):
        response = self.add_car('DH1234', 'Toyota Yaris', '1410', True)
        print(f"Status code: {response.status_code}")
        print(f"Response content: {response.content.decode()}")
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertIn('message', response_data)
        print(Samochód.objects.filter(registration_number="DH1234").exists())
        self.assertEqual(response_data['message'],'Samochód został dodany pomyślnie!')
        print(response_data['message'], '\n')

    def test_deleteCar(self):
        # Dodawanie samochodu
        self.add_car('DH1234', 'Toyota Yaris', '1410', True)
        # Sprawdzanie, czy samochód istnieje przed usunięciem
        self.assertTrue(Samochód.objects.filter(registration_number='DH1234').exists())
        # Usuwanie samochodu
        response = self.delete_car('DH1234')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Samochód został usunięty pomyślnie!')
        # Sprawdzanie, czy samochód został usunięty
        self.assertFalse(Samochód.objects.filter(registration_number='DH1234').exists())
        print(response_data['message'], '\n')

    def test_deleteRoom(self):
        # Dodawanie sali
        self.add_sala(13, True, 'c123')
        # Sprawdzanie, czy sala istnieje przed usunięciem
        self.assertTrue(Sala.objects.filter(nazwa='c123').exists())
        # Usuwanie sali
        response = self.delete_room('c123')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Sala została usunięta pomyślnie!')
        # Sprawdzanie, czy sala została usunięta
        self.assertFalse(Sala.objects.filter(nazwa='c123').exists())
        print(response_data['message'], '\n')

    def test_deleteUser(self):
        # Rejestracja użytkownika
        self.register_user('test@domena.com', 'strong_password', '2003-03-03', 'kursant')
        # Sprawdzanie, czy użytkownik istnieje przed usunięciem
        self.assertTrue(get_user_model().objects.filter(email='test@domena.com').exists())
        # Usuwanie użytkownika
        response = self.delete_user('test@domena.com')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Użytkownik został usunięty pomyślnie!')
        # Sprawdzanie, czy użytkownik został usunięty
        self.assertFalse(get_user_model().objects.filter(email='test@domena.com').exists())
        print(response_data['message'], '\n')
    def test_logadmin(self):
        admin = create_admin()
        response = self.login_user('admin@domain.com', 'strong_password')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Zalogowano pomyślnie.')
        print(response_data['message'], '\n')


