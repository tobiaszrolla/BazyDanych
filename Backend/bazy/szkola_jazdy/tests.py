from datetime import time
from http.client import responses
from django.contrib.auth.models import User
from django.core import mail
from django.core.mail import send_mail
from django.http import JsonResponse
from django.test import TestCase, Client
import json
from django.contrib.auth import get_user_model
from .models import Samochód, Sala, Zajęcia, KursanciNaZajęciach, Użytkownik
from .create_admin import create_admin
from django.conf import settings
from django.urls import reverse
from django.db import connection


from .views import register


class RegisterTest(TestCase):  # Klasa testowa dziedziczy po TestCase
    def setUp(self):
        self.client = Client()
        self.client.session.clear()

    #Metody pomocnicze
    def delete_car(self, registration_number):
        response = self.client.delete(f'/delete_car/{registration_number}/')
        print(f"Status code for deleting car: {response.status_code}")
        print(f"Response content: {response.content.decode()}")
        return response

    def delete_room(self, room_name):
        response = self.client.delete(f'/delete_room/{room_name}/')
        print(f"Status code for deleting room: {response.status_code}")
        print(f"Response content: {response.content.decode()}")
        return response

    def delete_user(self, email):
        response = self.client.delete(f'/delete_user/{email}/')
        print(f"Status code for deleting user: {response.status_code}")
        print(f"Response content: {response.content.decode()}")
        return response

    def delete_zajęcia(self, numer_zajęć):
        response = self.client.delete(f'/delete_zajęcia/{numer_zajęć}/')
        print(f"Status code for deleting zajęcia: {response.status_code}")
        print(f"Response content: {response.content.decode()}")
        return response

    def register_user(self,
                      email,
                      password,
                      data_urodzenia,
                      typ_użytkownika
                      ):
        data = {
            'email': email,
            'nrTelefonu': '123456789',
            'imię': 'User',
            'nazwisko': 'User',
            'data_urodzenia': data_urodzenia,
            'typ_użytkownika': typ_użytkownika,
            'password': password
        }
        response = self.client.post(
            '/register/',
            data=json.dumps(data),
            content_type='application/json'
        )
        return response

    def login_user(self, email, password):
        data = {
            'email': email,
            'password': password,
        }
        response = self.client.post(
            '/login/',
            data=json.dumps(data),
            content_type='application/json'
        )
        return response
    def logout_user(self):
        response = self.client.post('/logout_user/')
        return response
    def logout_user(self):
        response=self.client.post('/logout/')
        return response

    def add_sala(self, capacity, availability, nazwa):
        data = {
            'capacity': capacity,
            'availability': availability,
            'nazwa': nazwa,
        }
        response = self.client.post(
            '/add_room/',
            data=json.dumps(data),
            content_type='application/json'
        )
        print(response.status_code)
        return response
    def add_car(self, registration_number, model, production_year, availability):
        data = {
            'registration_number': registration_number,
            'model': model,
            'production_year': production_year,
            'availability': availability
        }
        response = self.client.post(
            '/add_car/',
            data=json.dumps(data),
            content_type='application/json'
        )
        print(response.status_code)
        return response
    def add_Zajęcia(self, nazwa_sali, registration_number, godzina_rozpoczęcia, godzina_zakończenia,data):
        if(registration_number==''):
            data = {
                'nazwa_sali': nazwa_sali,
                'godzina_rozpoczęcia': godzina_rozpoczęcia,
                'godzina_zakończenia': godzina_zakończenia,
                'data' : data
            }
        else :
            data = {
                'numer_rejestracyjny': registration_number,
                'godzina_rozpoczęcia': godzina_rozpoczęcia,
                'godzina_zakończenia': godzina_zakończenia,
                'data': data
            }
        response = self.client.post(
            '/add_zajęcia/',
            data=json.dumps(data),
            content_type='application/json'
        )
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.content.decode()}")
        return response

    def zapis_na_zajęcia(self, zajęcia_id):
        data = {
            'zajęcia_id': zajęcia_id
        }
        response = self.client.post(
            f'/zapisz_na_zajęcia/{zajęcia_id}/',
            data=json.dumps(data),
            content_type='application/json'
        )
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.content.decode()}")
        return response

    def zapis_na_kurs(self,kategoria,lekcje_teoretyczne,lekcje_praktyczne):
        data ={
            'kategoria': kategoria,
            'lekcje_teoretyczne': lekcje_teoretyczne,
            'lekcje_praktyczne': lekcje_praktyczne
        }
        response = self.client.put(
            f'/zapisz_na_kurs/',
            data=json.dumps(data),
            content_type='application/json'
        )
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.content.decode()}")
        return response

    def sprawdź_status_kodu(self, response, oczekiwany_status_kodu):
        """Pomocnicza funkcja do porównania statusu odpowiedzi"""
        self.assertEqual(response.status_code, oczekiwany_status_kodu,
                         f"Oczekiwany status kodu {oczekiwany_status_kodu}, ale otrzymano {response.status_code}")

    def sprawdź_zawartość_odpowiedzi(self, response, oczekiwana_zawartość):
        """Pomocnicza funkcja do porównania treści odpowiedzi"""
        self.assertIn(oczekiwana_zawartość, response.content.decode(),
                      f"Oczekiwana zawartość: '{oczekiwana_zawartość}' nie została znaleziona w odpowiedzi")
    def test_register(self):
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

    def test_logout(self):
        self.register_user('test@domena.com', 'strong_password', '2003-03-03', 'kursant')
        self.login_user('test@domena.com', 'strong_password')
        response = self.logout_user()
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Wylogowano pomyślnie.')
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
    def test_zapisz_na_kurs(self):
        session = self.client.session
        self.register_user('test@domena.com', 'strong_password', '2003-03-03', 'kursant')
        self.login_user('test@domena.com', 'strong_password')
        response = self.zapis_na_kurs('B',10,10)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Zapis na kurs zakończony sukcesem.')

    def test_newSala(self):
        session = self.client.session
        create_admin()
        self.login_user('admin@domain.com', 'strong_password')
        response = self.add_sala(13,True,'c123')
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Sala została dodana pomyślnie!')
        print(response_data['message'], 'Sala została dodana pomyślnie!\n')
    def test_newSamochód(self):
        session = self.client.session
        create_admin()
        self.login_user('admin@domain.com', 'strong_password')
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
        session = self.client.session
        create_admin()
        self.login_user('admin@domain.com', 'strong_password')
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
        session = self.client.session
        create_admin()
        self.login_user('admin@domain.com', 'strong_password')
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
        session = self.client.session
        create_admin()
        self.login_user('admin@domain.com', 'strong_password')
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

    def test_logout(self):
        self.register_user('test@domena.com', 'strong_password', '2003-03-03', 'kursant')
        self.login_user('test@domena.com', 'strong_password')
        response = self.logout_user()
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Wylogowano pomyślnie.')
        print(response_data['message'], '\n')
    def test_dodawanieZajęć(self):
        session = self.client.session #tworzy sesję
        create_admin()
        self.login_user('admin@domain.com', 'strong_password')
        self.register_user('test@domena.com', 'strong_password', '2003-03-03', 'instruktor')
        self.add_sala(13,True,'c123')
        self.logout_user()
        self.login_user('test@domena.com', 'strong_password')
        response = self.add_Zajęcia('c123', '', '13:14:00', '16:30:00','2024-03-03')
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Zajęcia zostały utworzone pomyślnie!')
        print(response_data['message'], '\n')

    def test_dodawanieZajęć_zajęta_sala(self):
        session = self.client.session
        create_admin()
        self.login_user('admin@domain.com', 'strong_password')
        self.register_user('test@domena.com', 'strong_password', '2003-03-03', 'instruktor')
        self.add_sala(13, True, 'c123')
        self.logout_user()
        self.login_user('test@domena.com', 'strong_password')
        self.add_Zajęcia('c123', '', '13:14:00', '16:30:00','2024-03-03')
        response = self.add_Zajęcia('c123', '', '14:14:00', '16:50:00','2024-03-03')
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Sala jest już zajęta')
        print(response_data['error'], '\n')
    def test_deleteZajęcia(self):
        session = self.client.session  # Tworzenie sesji
        create_admin()
        self.login_user('admin@domain.com', 'strong_password')
        self.register_user('test@domena.com', 'strong_password', '2003-03-03', 'instruktor')
        self.add_sala(13, True, 'c123')  # Dodanie sali
        self.logout_user()
        self.login_user('test@domena.com', 'strong_password')

        # Dodanie zajęć
        response = self.add_Zajęcia('c123', '', '13:14:00', '16:30:00','2024-03-03')
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Zajęcia zostały utworzone pomyślnie!')
        print(response_data['message'], '\n')

        # Pobieranie zajęć z bazy danych, jeśli numer zajęć nie jest w odpowiedzi
        if 'numer_zajęć' in response_data:
            numer_zajęć = response_data['numer_zajęć']
        else:
            zajęcia = Zajęcia.objects.get(
                sala__nazwa='c123',
                godzina_rozpoczęcia='13:14:00',
                godzina_zakończenia='16:30:00',
            )
            numer_zajęć = zajęcia.id

        self.assertIsNotNone(numer_zajęć,
                             "Numer zajęć nie został zwrócony w odpowiedzi ani odnaleziony w bazie danych.")

        # Usunięcie zajęć
        response = self.delete_zajęcia(numer_zajęć)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('success', response_data)  # Zmienione z 'message' na 'success'
        self.assertEqual(response_data['success'],
                         'Zajęcia zostały pomyślnie usunięte.')  # Zmienione z 'message' na 'success'
        print(response_data['success'], '\n')

    def test_zapis_na_zajęcia(self):
        session = self.client.session
        create_admin()
        self.login_user('admin@domain.com', 'strong_password')
        self.register_user('test@domena.com', 'strong_password', '2003-03-03', 'instruktor')
        self.register_user('test2@domena.com', 'strong_password', '2003-03-03', 'kursant')
        self.add_car('DH1234', 'Toyota Yaris', '1980', True)
        self.assertTrue(Samochód.objects.filter(registration_number='DH1234').exists(),"Samochód nie został dodany do bazy danych")

        self.logout_user()
        self.login_user('test@domena.com', 'strong_password')
        response = self.add_Zajęcia('', 'DH1234', '13:14:00', '16:30:00','2024-03-03')
        self.logout_user()
        self.login_user('test2@domena.com', 'strong_password')
        zajęcia = Zajęcia.objects.get(samochód__registration_number='DH1234', godzina_rozpoczęcia='13:14:00', godzina_zakończenia='16:30:00')
        #print(zajęcia)
        zajęcia_id = zajęcia.id
        self.assertIsNotNone(zajęcia_id,"Numer zajęć nie został zwrócony w odpowiedzi ani odnaleziony w bazie danych.")
        response = self.zapis_na_zajęcia(zajęcia_id)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Zostałeś zapisany na zajęcia!')
        print(response_data['message'], '\n')

    def test_cryptography(self):
        session = self.client.session
        self.register_user('test@domena.com', 'strong_password', '2003-03-03', 'instruktor')
    # Testy resetowania hasła
    def test_reset_password_success(self):
        """Test poprawnego żądania resetu hasła."""
        response = self.client.post(
            reverse('reset_password_request'),
            data=json.dumps({"email": "test@example.com"}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Wysłano e-mail z linkiem do resetowania hasła."})

        # Sprawdzenie, czy e-mail został wygenerowany
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Resetowanie hasła", mail.outbox[0].subject)
        self.assertIn("http://localhost:8000/reset_password/", mail.outbox[0].body)

    def test_reset_password_nonexistent_email(self):
        """Test próby resetu hasła dla nieistniejącego e-maila."""
        response = self.client.post(
            reverse('reset_password_request'),
            data=json.dumps({"email": "nonexistent@example.com"}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "Nie znaleziono użytkownika z podanym adresem e-mail."})
        self.assertEqual(len(mail.outbox), 0)

    def test_reset_password_no_email(self):
        """Test, gdy nie podano e-maila."""
        response = self.client.post(
            reverse('reset_password_request'),
            data=json.dumps({}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Podaj adres e-mail."})
        self.assertEqual(len(mail.outbox), 0)

    def test_reset_password_invalid_data(self):
        """Test, gdy dane wejściowe są niepoprawne (np. nie JSON)."""
        response = self.client.post(
            reverse('reset_password_request'),
            data="niepoprawne dane",
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Nieprawidłowe dane wejściowe."})
        self.assertEqual(len(mail.outbox), 0)

    def test_reset_password_invalid_method(self):
        """Test użycia metody innej niż POST."""
        response = self.client.get(reverse('reset_password_request'))
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {"error": "Nieobsługiwana metoda żądania. Użyj POST."})
        self.assertEqual(len(mail.outbox), 0)

'''''    def test_dostępne_zajęcia(self):
        # Dodanie sali i samochodu
        sala = Sala.objects.create(nazwa="Sala 101", capacity=10, availability=True)
        samochód = Samochód.objects.create(registration_number="XYZ123", model="Toyota Corolla", production_year="2020",
                                           availability=True)

        # Dodanie instruktora
        instruktor = Użytkownik.objects.create_user(
            email="instruktor@test.com",
            password="strong_password",
            imię="Jan",
            nazwisko="Kowalski",
            typ_użytkownika="instruktor"
        )

        # Tworzenie zajęć z wolnymi miejscami
        zajęcia = Zajęcia.objects.create(
            sala=sala,
            samochód=samochód,
            instruktor=instruktor,
            godzina_rozpoczęcia="08:00",
            godzina_zakończenia="10:00"
        )

        user = Użytkownik.objects.get(email="test@domena.com")

        #kontrola poprawności rejestracji
        self.assertEqual(user.nrTelefonu, "123456789")
        self.assertEqual(user.imię, "User")
        self.assertEqual(user.nazwisko, "User")

        #surowe dane z bazy
        with connection.cursor() as cursor:
            cursor.execute("SELECT nrTelefonu, imię, nazwisko FROM szkola_jazdy_użytkownik WHERE email = %s",
                           ["test@domena.com"])
            raw_data = cursor.fetchone()

        print("Zaszyfrowane dane z bazy:", raw_data)
        self.assertNotEqual(raw_data[0], "123456789")
        self.assertNotEqual(raw_data[1], "Jan")
        self.assertNotEqual(raw_data[2], "Kowalski")
        # Sprawdzanie zawartości odpowiedzi JSON
        response_data = response.json()
        self.assertEqual(len(response_data), 1)  # Sprawdzamy, czy zwrócono 1 zajęcia
        self.assertEqual(response_data[0]["id"], zajęcia.id)
        self.assertEqual(response_data[0]["wolne_miejsca"], 9)  # Jedno miejsce zajęte, sala na 10 osób
        self.assertIn("Instruktor: Jan Kowalski", response_data[0]["title"])

        print("Test dostępne_zajęcia zakończony pomyślnie.")'''


