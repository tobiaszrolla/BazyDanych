import random
import string
import json

from django.test import TestCase, Client
from django.urls import reverse
from .models import Użytkownik


class ResetPasswordRequestTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('reset_password_request')
        self.user = Użytkownik.objects.create_user(username='testuser', email='testuser@example.com',
                                                   password='old_password')
        print("Test setup completed: użytkownik testowy został utworzony.")

    def test_missing_email(self):
        print("Rozpoczynam test: test_missing_email")
        response = self.client.post(self.url, data=json.dumps({}), content_type='application/json')
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {"error": "Podaj adres e-mail."})

    def test_user_not_found(self):
        print("Rozpoczynam test: test_user_not_found")
        response = self.client.post(self.url, data=json.dumps({"email": "notfound@example.com"}),
                                    content_type='application/json')
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, {"error": "Nie znaleziono użytkownika z podanym adresem e-mail."})

    def test_successful_password_reset(self):
        print("Rozpoczynam test: test_successful_password_reset")
        response = self.client.post(self.url, data=json.dumps({"email": "testuser@example.com"}),
                                    content_type='application/json')
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"message": "Wysłano e-mail z nowym hasłem."})

        # Sprawdzenie, czy hasło użytkownika zostało zmienione
        self.user.refresh_from_db()
        updated_user = Użytkownik.objects.get(email="testuser@example.com")
        print(f"Stare hasło: old_password, nowe hasło: {updated_user.password}")
        self.assertFalse(updated_user.check_password('old_password'))

        # Nowe hasło generowane losowo
        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        updated_user.set_password(new_password)
        updated_user.save()

        print(f"Po zresetowaniu: nowe hasło użytkownika: {new_password}")
        self.assertTrue(updated_user.check_password(new_password))

    def test_invalid_input_data(self):
        print("Rozpoczynam test: test_invalid_input_data")
        response = self.client.post(self.url, data='invalid json', content_type='application/json')
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {"error": "Nieprawidłowe dane wejściowe."})

    def test_unsupported_method(self):
        print("Rozpoczynam test: test_unsupported_method")
        response = self.client.get(self.url)
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(response.content, {"error": "Nieobsługiwana metoda żądania. Użyj POST."})

    def assertJSONEqual(self, raw, expected_data):
        """
        Metoda pomocnicza do porównywania odpowiedzi JSON.
        """
        print(f"Porównuję odpowiedź JSON: {raw} z oczekiwanym wynikiem: {expected_data}")

        # Dekodowanie JSON z odpowiedzi i oczekiwanego obiektu
        parsed_response = json.loads(raw.decode('utf-8'))

        # Użycie json.dumps() z ensure_ascii=False w celu wyświetlania tekstów w normalnym formacie
        pretty_response = json.dumps(parsed_response, ensure_ascii=False)
        pretty_expected = json.dumps(expected_data, ensure_ascii=False)

        print(f"Porównanie odpowiedzi:\n{pretty_response} == {pretty_expected}")

        # Porównanie bez uciekania do znaków Unicode
        self.assertEqual(pretty_response, pretty_expected)
