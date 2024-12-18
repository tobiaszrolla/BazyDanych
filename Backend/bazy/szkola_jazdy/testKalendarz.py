from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Zajęcia, Sala, KursanciNaZajęciach
from .create_admin import create_admin

class KalendarzTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()

        # Tworzenie użytkowników
        self.kursant = self.User.objects.create_user(
            username="kursant@test.com",
            email="kursant@test.com",
            password="strong_password",
            typ_użytkownika="kursant"
        )
        self.instruktor = self.User.objects.create_user(
            username="instruktor@test.com",
            email="instruktor@test.com",
            password="strong_password",
            typ_użytkownika="instruktor"
        )

        # Tworzenie sali i zajęć
        self.sala = Sala.objects.create(nazwa="Sala 1", capacity=10, availability=True)
        self.zajęcia = Zajęcia.objects.create(
            sala=self.sala,
            godzina_rozpoczęcia="10:00",
            godzina_zakończenia="12:00",
            data="2024-03-15",
            instruktor=self.instruktor
        )

        # Dodanie kursanta do zajęć
        KursanciNaZajęciach.objects.create(użytkownik=self.kursant, zajęcia=self.zajęcia)

    def test_kalendarz_kursant(self):
        # Logowanie kursanta
        logged_in = self.client.login(email="kursant@test.com", password="strong_password")
        self.assertTrue(logged_in, "Logowanie kursanta nie powiodło się")

        # Wywołanie widoku kalendarza
        response = self.client.post('/kalendarz/')
        self.assertEqual(response.status_code, 200)

        # Sprawdzanie odpowiedzi
        response_data = response.json()
        self.assertIn("zajęcia", response_data)
        self.assertEqual(len(response_data["zajęcia"]), 1)
        self.assertEqual(response_data["zajęcia"][0]["id"], self.zajęcia.id)

    def test_kalendarz_instruktor(self):
        # Logowanie instruktora
        self.client.login(email="instruktor@test.com", password="strong_password")

        # Wywołanie widoku kalendarza
        response = self.client.post('/kalendarz/')
        self.assertEqual(response.status_code, 200)

        # Sprawdzanie odpowiedzi
        response_data = response.json()
        self.assertIn("zajęcia", response_data)
        self.assertEqual(len(response_data["zajęcia"]), 1)
        self.assertEqual(response_data["zajęcia"][0]["id"], self.zajęcia.id)

    def test_kalendarz_admin(self):
        # Tworzenie administratora
        create_admin()
        self.client.login(email="admin@domain.com", password="strong_password")

        # Wywołanie widoku kalendarza
        response = self.client.post('/kalendarz/')
        self.assertEqual(response.status_code, 403)

        # Sprawdzanie odpowiedzi
        response_data = response.json()
        self.assertIn("error", response_data)
        self.assertEqual(response_data["error"], "Administrator nie zapisuje się na zajęcia")
