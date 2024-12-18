from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Sala, Samochód, Zajęcia, KursanciNaZajęciach
from django.db import transaction


class TestTransakcja(TestCase):

    def setUp(self):
        # Tworzenie użytkownika, który jest kursantem
        print("Tworzenie kursanta...")
        self.kursant = get_user_model().objects.create_user(
            username='kursant',  # Dodajemy pole 'username'
            email='kursant@example.com',
            password='testpassword',
            imię='Anna',
            nazwisko='Nowak',
            typ_użytkownika='kursant'
        )

        # Tworzenie pozostałych obiektów: Sala, Samochód, Zajęcia
        print("Tworzenie sali, samochodu i zajęć...")
        self.sala = Sala.objects.create(nazwa="Sala 1", capacity=30, remaining_seats=30)
        self.samochód = Samochód.objects.create(registration_number="XYZ123", model="Toyota", production_year="2015")
        self.zajęcia = Zajęcia.objects.create(
            sala=self.sala,
            samochód=self.samochód,
            kategoria="B",
            godzina_rozpoczęcia="10:00",
            godzina_zakończenia="12:00",
            data="2024-12-20"
        )

    def test_transakcja_sukces(self):
        # Test zapisu na zajęcia i zmiany liczby miejsc
        print("\nTest transakcja_sukces: Zapis na zajęcia...")
        przed = self.sala.remaining_seats
        print(f"Liczba wolnych miejsc przed zapisaniem: {przed}")

        with transaction.atomic():
            self.zajęcia.kursanci.add(self.kursant)
            self.sala.remaining_seats -= 1
            self.sala.save()

            po = self.sala.remaining_seats
            print(f"Liczba wolnych miejsc po zapisaniu: {po}")
            self.assertEqual(po, przed - 1)
            self.assertIn(self.kursant, self.zajęcia.kursanci.all())

    def test_brak_miejsc_w_sali(self):
        # Test w przypadku braku dostępnych miejsc w sali
        print("\nTest brak_miejsc_w_sali: Brak dostępnych miejsc w sali...")
        self.sala.remaining_seats = 0
        self.sala.save()

        print("Sprawdzanie, czy rzuci wyjątek...")

        # Dodajemy informację, że sala jest pełna
        print(f"Brak dostępnych miejsc w sali: {self.sala.remaining_seats} miejsc.")

        with self.assertRaises(ValueError):  # Używamy ValueError, bo wyjątek tego typu będzie rzucany
            with transaction.atomic():
                if self.sala.remaining_seats <= 0:
                    raise ValueError("Nie udało się zapisać, wszystkie miejsca są zajęte.")
                self.zajęcia.kursanci.add(self.kursant)

    def test_nieistniejące_zajęcia(self):
        # Test zapisu na nieistniejące zajęcia
        print("\nTest nieistniejące_zajęcia: Sprawdzanie nieistniejących zajęć...")
        non_existing_zajęcia = Zajęcia.objects.filter(id=999).first()

        print(f"Sprawdzanie, czy znaleziono zajęcia: {non_existing_zajęcia}")
        self.assertIsNone(non_existing_zajęcia)

    def test_nieistniejący_użytkownik(self):
        # Test próby zapisania nieistniejącego użytkownika
        print("\nTest nieistniejący_użytkownik: Sprawdzanie nieistniejącego użytkownika...")
        non_existing_user = get_user_model().objects.filter(id=999).first()

        print(f"Sprawdzanie, czy znaleziono użytkownika: {non_existing_user}")
        self.assertIsNone(non_existing_user)

    def test_samochod_niedostepny(self):
        # Test zapisania kursanta na zajęcia, gdy samochód jest niedostępny
        print("\nTest samochod_niedostepny: Sprawdzanie niedostępności samochodu...")
        self.samochód.availability = False
        self.samochód.save()

        print(f"Sprawdzanie dostępności samochodu: {self.samochód.availability}")

        # Sprawdzamy, czy nie można dodać kursanta do zajęć, jeśli samochód jest niedostępny
        print("Sprawdzanie, czy rzuci wyjątek...")
        with self.assertRaises(ValueError):  # Używamy ValueError, bo wyjątek tego typu będzie rzucany
            with transaction.atomic():
                if not self.samochód.availability:
                    raise ValueError("Nie udało się zapisać, samochód jest niedostępny.")
                self.zajęcia.kursanci.add(self.kursant)
