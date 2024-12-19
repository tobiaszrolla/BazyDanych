from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Zajęcia, Użytkownik, KursanciNaZajęciach, Sala, Samochód


class ZakonczZajeciaTestCase(TestCase):
    def setUp(self):
        self.kursant = Użytkownik.objects.create_user(
            username="kursant@test.com",
            email="kursant@test.com",
            password="strong_password",
            typ_użytkownika="kursant",
            godziny_lekcji_praktycznych = 0,
            godziny_lekcje_teoretyczne = 0,
            posiadane_lekcje_teoretyczne = 10,
            posiadane_lekcje_praktyczne = 10

        )
        self.car = Samochód.objects.create(
            registration_number="ABC123",
            model="Toyota",
            production_year="2020",
            availability=True
        )
        self.zajęcia = Zajęcia.objects.create(
            samochód=self.car,
            kategoria="B",
            godzina_rozpoczęcia="10:00",
            godzina_zakończenia="12:00",
            dostempne_miejsca=10
        )
        self.zapisany = KursanciNaZajęciach.objects.create(
            użytkownik=self.kursant,
            zajęcia=self.zajęcia
        )
        self.client = Client()

    def test_zakoncz_zajecia_success(self):
        # Logowanie użytkownika
        self.client.login(username="kursant@test.com", password="strong_password")

        # Wysyłanie żądania POST
        url = reverse('zakoncz_zajecia', args=[self.zajęcia.id, self.kursant.id])
        response = self.client.post(url,content_type="application/json")

        # Sprawdzanie odpowiedzi
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "Transakcja zakończona sukcesem!"})

        # Sprawdzenie, czy zajęcia zostały usunięte
        self.assertFalse(Zajęcia.objects.filter(id=self.zajęcia.id).exists())

        # Sprawdzenie aktualizacji kursanta
        self.kursant.refresh_from_db()
        self.assertEqual(self.kursant.godziny_lekcji_praktycznych, 1)
        self.assertEqual(self.kursant.posiadane_lekcje_praktyczne, 9)
