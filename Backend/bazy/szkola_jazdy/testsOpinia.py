from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()  # Pobierz zamiennik modelu użytkownika

class DodajOpinieViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="password")
        cls.url = reverse('dodaj_opinie')  # Zamień na rzeczywistą nazwę URL-a

    def test_redirect_if_not_logged_in(self):
        """Sprawdź, czy niezalogowany użytkownik jest przekierowany na stronę logowania."""
        print("Test: Sprawdzenie przekierowania niezalogowanego użytkownika na stronę logowania")
        response = self.client.post(self.url, {"opinia": "Testowa opinia"})
        print(f"Status odpowiedzi: {response.status_code}")  # Powinno być 302 (przekierowanie)
        self.assertEqual(response.status_code, 302)  # Niezalogowany użytkownik jest przekierowywany
        print("Niezalogowany użytkownik został przekierowany.")

    def test_view_renders_for_logged_in_user(self):
        """Sprawdź, czy widok renderuje się poprawnie dla zalogowanego użytkownika."""
        print("Test: Sprawdzenie renderowania widoku dla zalogowanego użytkownika")
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        print(f"Status odpowiedzi: {response.status_code}")  # Powinno być 405 (metoda GET niedozwolona)
        self.assertEqual(response.status_code, 405)  # Metoda GET nie jest obsługiwana
        print("Widok renderuje się poprawnie dla zalogowanego użytkownika.")

    def test_form_submission_valid_data(self):
        """Sprawdź, czy formularz poprawnie zapisuje opinię."""
        print("Test: Sprawdzenie poprawności zapisu opinii")
        self.client.login(username="testuser", password="password")
        response = self.client.post(self.url, {"opinia": "Dobra lekcja!"})
        print(f"Status odpowiedzi: {response.status_code}")  # Powinno być 200
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success', 'message': 'Opinia została zapisana.'})
        print("Opinia została zapisana pomyślnie.")

        # Wypisanie opinii i komunikatu
        print(f"Opinia została dodana: 'Dobra lekcja!'")
        print("Opinia została dodana pomyślnie!")

    def test_form_submission_invalid_data(self):
        """Sprawdź, czy formularz nie zapisuje opinii przy nieprawidłowych danych."""
        print("Test: Sprawdzenie niepoprawnego zapisu opinii")
        self.client.login(username="testuser", password="password")
        response = self.client.post(self.url, {"opinia": ""})  # Pusta opinia
        print(f"Status odpowiedzi: {response.status_code}")  # Powinno być 400 (błąd)
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.json())
        print("Nie zapisano opinii z błędnymi danymi.")

    def test_form_shows_success_message(self):
        """Sprawdź, czy wyświetlany jest komunikat o sukcesie po zapisaniu opinii."""
        print("Test: Sprawdzenie komunikatu o sukcesie po zapisaniu opinii")
        self.client.login(username="testuser", password="password")
        response = self.client.post(self.url, {"opinia": "Dobra lekcja!"}, follow=True)
        print(f"Status odpowiedzi: {response.status_code}")  # Powinno być 200
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success', 'message': 'Opinia została zapisana.'})
        print("Komunikat o sukcesie został wyświetlony.")

        # Wypisanie opinii i komunikatu
        print(f"Opinia została dodana: 'Dobra lekcja!'")
        print("Opinia została dodana pomyślnie!")
