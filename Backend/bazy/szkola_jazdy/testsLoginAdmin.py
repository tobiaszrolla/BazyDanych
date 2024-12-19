from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.mail import send_mail
from unittest.mock import patch
from .create_admin import create_admin
import json
from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import Użytkownik


class LoginTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.admin_user = create_admin()

        self.login_url = reverse('login')
        self.verify_url = reverse('verify_code')

    def test_login_admin_without_verification_code(self):
        # Logowanie admina, kiedy nie ma kodu weryfikacyjnego
        response = self.client.post(self.login_url, json.dumps({
            "email": "admin@domain.com",
            "password": "strong_password"
        }), content_type="application/json")

        # Sprawdzamy, czy wysłano e-mail
        self.assertEqual(response.status_code, 202)
        self.assertEqual(len(mail.outbox), 1)  # Powinien być 1 e-mail w skrzynce

    def test_login_admin_with_incorrect_verification_code(self):
        # Ustawienie kodu weryfikacyjnego dla admina
        self.admin_user.verification_code = "123456"
        self.admin_user.save()

        # Próba wprowadzenia nieprawidłowego kodu
        response = self.client.post(self.verify_url, json.dumps({
            "email": "admin@domain.com",
            "code": "654321"
        }), content_type="application/json")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"], "Nieprawidłowy kod weryfikacyjny lub kod wygasł.")

    def test_verify_code_success(self):
        # Ustawienie kodu weryfikacyjnego dla admina
        self.admin_user.verification_code = "123456"
        self.admin_user.save()

        # Weryfikacja poprawnego kodu
        response = self.client.post(self.verify_url, json.dumps({
            "email": "admin@domain.com",
            "code": "123456"
        }), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Administrator zalogowany pomyślnie.")

    def test_verify_code_invalid_user(self):
        # Weryfikacja kodu dla nieistniejącego użytkownika
        response = self.client.post(self.verify_url, json.dumps({
            "email": "nonexistent@test.com",
            "code": "123456"
        }), content_type="application/json")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"], "Użytkownik o podanym adresie email nie istnieje.")

