from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import User
from .models import Zajęcia, KursanciNaZajęciach, Użytkownik, Sala, Samochód


class ZapiszNaZajeciaEmailTestCase(TestCase):

    def setUp(self):
        self.kursant = Użytkownik.objects.create_user(
            username="kursant@test.com",
            email="kursant@test.com",
            password="strong_password",
            typ_użytkownika="kursant",
            posiadane_lekcje_teoretyczne = 10
        )

        self.instruktor = Użytkownik.objects.create_user(
            username="instruktor@test.com",
            email="instruktor@test.com",
            password="strong_password",
            typ_użytkownika="instruktor"
        )

        self.room = Sala.objects.create(
            nazwa="Sala A",
            availability=True,
            capacity=30
        )

        self.car = Samochód.objects.create(
            registration_number="FH31313",
            availability=True,
            model="HONDA",
            production_year="2020"
        )

        self.zajęcia1 = Zajęcia.objects.create(
            sala=self.room,
            samochód=None,
            dostempne_miejsca=5,
            data="2024-12-20",
            godzina_rozpoczęcia="10:00",
            godzina_zakończenia="11:00"
        )
        self.zajęcia2 = Zajęcia.objects.create(
            sala=self.room,
            samochód=None,
            dostempne_miejsca=0,
            data="2024-12-20",
            godzina_rozpoczęcia="11:00",
            godzina_zakończenia="12:00"
        )
        self.zajęcia3 = Zajęcia.objects.create(
            samochód=self.car,
            dostempne_miejsca=1,
            data="2024-12-20",
            godzina_rozpoczęcia="11:00",
            godzina_zakończenia="12:00"
        )


        # Logowanie użytkownika
        self.client.login(username="kursant@test.com", password="strong_password")
        self.zapis1_url = reverse('zapisz_na_zajęcia', args=[self.zajęcia1.id])
        self.zapis2_url = reverse('zapisz_na_zajęcia', args=[self.zajęcia2.id])
        self.zapis3_url = reverse('zapisz_na_zajęcia', args=[self.zajęcia3.id])

    def test_email_wysłany_po_zapisie(self):
        # Wysłanie żądania POST
        response = self.client.post(self.zapis1_url,data={},content_type="application/json")

        # Sprawdzenie odpowiedzi
        print(response.content)
        print(f"Status code: {response.status_code}")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()['message'],
            "Zostałeś zapisany na zajęcia! E-mail potwierdzający został wysłany."
        )

        # Sprawdzenie, czy e-mail został wysłany
        self.assertEqual(len(mail.outbox), 1)  # Powinien być 1 e-mail w skrzynce
        email = mail.outbox[0]

        # Sprawdzenie tematu e-maila
        self.assertEqual(email.subject, "Potwierdzenie zapisu na zajęcia")

        # Sprawdzenie treści e-maila
        self.assertIn("Cześć kursant@test.com,", email.body)

        # Sprawdzenie odbiorców
        self.assertEqual(email.to, ["kursant@test.com"])
    def test_zapisz_Na_zajęcia_pełnaSala(self):
        response = self.client.post(self.zapis2_url,data={},content_type="application/json")
        print(response.content)
        print(f"Status code: {response.status_code}")
        self.assertEqual(response.status_code, 400)
    def test_zapisz_Na_zajęcia_instruktor(self):
        self.client.logout()
        self.client.login(username="instruktor@test.com", password="strong_password")
        response = self.client.post(self.zapis1_url,data={},content_type="application/json")
        print(response.content)
        print(f"Status code: {response.status_code}")
        self.assertEqual(response.status_code, 400)
    def test_zapisz_Na_zajęcia_liczba_miejsca(self):
        response = self.client.post(self.zapis1_url, data={}, content_type="application/json")
        print(response.content)
        print(f"Status code: {response.status_code}")
        self.assertEqual(response.status_code, 201)
        self.zajęcia1.refresh_from_db()
        nowe_dostempne_miejsca = self.zajęcia1.dostempne_miejsca
        self.assertEqual(nowe_dostempne_miejsca, 4)
        self.kursant.refresh_from_db()
    def test_zapisz_Na_zajencia_samochod(self):
        response = self.client.post(self.zapis3_url, data={}, content_type="application/json")
        print(response.content)
        print(f"Status code: {response.status_code}")
        self.assertEqual(response.status_code, 201)
        self.zajęcia1.refresh_from_db()
        nowe_dostempne_miejsca = self.zajęcia1.dostempne_miejsca


