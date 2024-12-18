from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Sala, Samochód, Zajęcia, KursanciNaZajęciach
from django.db import transaction
from django.urls import reverse


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
        self.samochód = Samochód.objects.create(registration_number="XYZ123", model="Toyota", production_year="2015", availability=True)
        self.zajęcia = Zajęcia.objects.create(
            sala=self.sala,
            samochód=self.samochód,
            kategoria="B",
            godzina_rozpoczęcia="10:00",
            godzina_zakończenia="12:00",
            data="2024-12-20"
        )

        # Logowanie użytkownika
        self.client.login(username='kursant', password='testpassword')

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

        with self.assertRaises(ValueError):  # Używamy ValueError, bo wyjątek tego typu będzie rzucany
            with transaction.atomic():
                if not self.samochód.availability:
                    raise ValueError("Nie udało się zapisać, samochód jest niedostępny.")
                self.zajęcia.kursanci.add(self.kursant)
    def test_zakoncz_zajecia_sukces(self):
        print("\nTest zakoncz_zajecia_sukces: Sprawdzanie zakończenia zajęć...")

        przed_godziny = self.kursant.godziny_lekcji_praktycznych
        przed_lekcje = self.kursant.posiadane_lekcje_praktyczne
        przed_zajecia_count = Zajęcia.objects.count()

        # Dodajemy kursanta do zajęć, aby mógł zakończyć zajęcia
        print(
            f"Przed zapisaniem na zajęcia: Kursant godziny lekcji praktycznych: {przed_godziny}, posiadane lekcje: {przed_lekcje}")
        self.zajęcia.kursanci.add(self.kursant)

        # Sprawdzanie godziny przed zakończeniem zajęć
        print(f"Godzina zajęć przed zakończeniem: {self.zajęcia.godzina_rozpoczęcia}")

        response = self.client.post(reverse('zakoncz_zajecia', args=[self.zajęcia.id, self.kursant.id]))

        # Sprawdzanie wyników po zakończeniu
        print(
            f"Po zakończeniu zajęć: Status odpowiedzi: {response.status_code}, wiadomość: {response.json().get('message')}")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], "Transakcja zakończona sukcesem!")

        self.kursant.refresh_from_db()
        print(
            f"Po zakończeniu zajęć: Kursant godziny lekcji praktycznych: {self.kursant.godziny_lekcji_praktycznych}, posiadane lekcje: {self.kursant.posiadane_lekcje_praktyczne}")
        self.assertEqual(self.kursant.godziny_lekcji_praktycznych, przed_godziny + 1)
        self.assertEqual(self.kursant.posiadane_lekcje_praktyczne, przed_lekcje - 1)

        print(f"Po zakończeniu zajęć: Liczba zajęć: {Zajęcia.objects.count()}")
        self.assertEqual(Zajęcia.objects.count(), przed_zajecia_count - 1)

    def test_kursant_nie_zapisany_na_zajecia(self):
        print("\nTest kursant_nie_zapisany_na_zajecia: Sprawdzanie, gdy kursant nie jest zapisany...")

        # Tworzymy innego kursanta, który nie jest zapisany na te zajęcia
        inny_kursant = get_user_model().objects.create_user(
            username='inny_kursant',
            email='inny_kursant@example.com',
            password='testpassword',
            imię='Jan',
            nazwisko='Kowalski',
            typ_użytkownika='kursant'
        )

        print(f"Sprawdzanie, czy kursant {inny_kursant.username} jest zapisany na zajęcia...")

        response = self.client.post(reverse('zakoncz_zajecia', args=[self.zajęcia.id, inny_kursant.id]))

        # Sprawdzanie wyników, gdy kursant nie jest zapisany
        print(f"Status odpowiedzi: {response.status_code}, błąd: {response.json().get('error')}")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "Kursant nie jest zapisany na te zajęcia.")

    def test_nieistniejące_zajecia(self):
        print("\nTest nieistniejące_zajecia: Sprawdzanie, gdy zajęcia nie istnieją...")

        # Próba zakończenia zajęć, które nie istnieją
        response = self.client.post(reverse('zakoncz_zajecia', args=[999, 1]))  # Zajęcia o id 999 nie istnieją

        # Sprawdzanie wyników
        print(f"Status odpowiedzi: {response.status_code}, błąd: {response.json().get('error')}")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Nie znaleziono wymaganych danych", response.json()['error'])

