from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from ..forms import RegistrationForm, LoginForm
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST
from django.conf import settings
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from ..models import Użytkownik, Samochód, Sala, Zajęcia, KursanciNaZajęciach
from django.contrib.auth import logout, authenticate, login as django_login #konflikt nazw z widokiem login()
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime
import random
import string
def is_admin(user):
    return user.is_superuser

@csrf_exempt
def register(request):
    if request.method == "POST":
        try:
            # Parsowanie danych JSON z żądania
            data = json.loads(request.body)
            email = data.get("email")
            nrTelefonu = data.get("nrTelefonu", None)
            imię = data.get("imię")
            nazwisko = data.get("nazwisko")
            data_urodzenia = data.get("data_urodzenia", None)
            typ_użytkownika = data.get("typ_użytkownika")
            password = data.get("password")

            # Walidacja: Sprawdzanie, czy wymagane dane są dostępne
            if not email or not imię or not nazwisko or not typ_użytkownika or not password:
                return JsonResponse({"error": "Brak wymaganych danych."}, status=400)

            # Sprawdzenie, czy e-mail jest już zajęty
            if Użytkownik.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email jest już zajęty."}, status=400)

            # Tworzenie użytkownika
            user = Użytkownik.objects.create(
                email=email,
                username=email,
                nrTelefonu=nrTelefonu,
                imię=imię,
                nazwisko=nazwisko,
                data_urodzenia=data_urodzenia,
                typ_użytkownika=typ_użytkownika,
                password=make_password(password)  # Hashowanie hasła
            )
            user.save()
            return JsonResponse({"message": "Użytkownik został zarejestrowany pomyślnie!"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Nieprawidłowe dane wejściowe"}, status=400)

        except Exception as e:
            return JsonResponse({"error": f"Wystąpił błąd: {str(e)}"}, status=500)

    # Jeśli metoda żądania nie jest POST
    return JsonResponse({"error": "Nieobsługiwana metoda żądania. Użyj POST."}, status=405)

@csrf_exempt
def login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            #Walidacja czy hasło email zostały przesłane
            if not email or not password:
                return JsonResponse({"error": "Email i hasło są wymagane."}, status=400)

            # Uwierzytelnienie użytkownika
            user = authenticate(request, username=email, password=password)  # Sprawdź poprawność danych

            if user is not None:
                django_login(request,user)
                # Zwrócenie odpowiedzi w przypadku poprawnej pary
                return JsonResponse({"message": "Zalogowano pomyślnie."}, status=200)
            else:
                # Odpowiedź w przypadku błędnych danych logowania
                return JsonResponse({"error": "Nieprawidłowy email lub hasło."}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Nieprawidłowe dane wejściowe. Upewnij się, że wysyłasz poprawny JSON."}, status=400)

        except Exception as e:
            return JsonResponse({"error": f"Wystąpił błąd: {str(e)}"}, status=500)

    return JsonResponse({"error": "Nieobsługiwana metoda żądania. Użyj POST."}, status=405)

@csrf_exempt
def logout(request):
    if request.method=="POST":
        try:
            logout(request)
            return JsonResponse({"message": "Wylogowano pomyślnie."}, status=200)
        except Exception as e:
            return JsonResponse({"error": f"Wsystąpił błąd: {str(e)}"}, status=500)

    return JsonResponse({"error": "Nieobsługiwana metoda żądania. Użyj POST."}, status=405)
@csrf_exempt
@user_passes_test(is_admin)
def delete_user(request, email):
    if request.method == "DELETE":
        try:
            # Pobranie użytkownika o danym e-mailu
            user = Użytkownik.objects.get(email=email)
            user.delete()
            return JsonResponse({"message": "Użytkownik został usunięty pomyślnie!"}, status=200)
        except Użytkownik.DoesNotExist:
            return JsonResponse({"error": "Użytkownik o tym e-mailu nie istnieje."}, status=404)
        except Exception as e:
            return JsonResponse({"error": f"Wystąpił błąd: {str(e)}"}, status=500)

    # Jeśli metoda żądania nie jest DELETE
    return JsonResponse({"error": "Nieobsługiwana metoda żądania. Użyj DELETE."}, status=405)
@csrf_exempt
@user_passes_test(is_admin)
def modify_user(request, email):
    if request.method == "PUT":
        try:
            # Pobranie użytkownika do modyfikacji
            user = Użytkownik.objects.get(email=email)

            # Parsowanie danych JSON z żądania
            data = json.loads(request.body)

            # Aktualizacja danych użytkownika
            user.imię = data.get("imię", user.imię)
            user.nazwisko = data.get("nazwisko", user.nazwisko)
            user.nrTelefonu = data.get("nrTelefonu", user.nrTelefonu)
            user.data_urodzenia = data.get("data_urodzenia", user.data_urodzenia)
            user.typ_użytkownika = data.get("typ_użytkownika", user.typ_użytkownika)

            # Jeśli przesłano nowe hasło, ustaw je
            if "password" in data:
                user.password = make_password(data["password"])

            user.save()
            return JsonResponse({"message": "Dane użytkownika zostały zmodyfikowane pomyślnie!"}, status=200)

        except Użytkownik.DoesNotExist:
            print("brak usera\n")
            return JsonResponse({"error": "Użytkownik o tym e-mailu nie istnieje."}, status=404)
        except Exception as e:
            return JsonResponse({"error": f"Wystąpił błąd: {str(e)}"}, status=500)

@csrf_exempt
def reset_password_request(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")

            if not email:
                return JsonResponse({"error": "Podaj adres e-mail."}, status=400)

            user = User.objects.filter(email=email).first()
            if not user:
                return JsonResponse({"error": "Nie znaleziono użytkownika z podanym adresem e-mail."}, status=404)

            # Generowanie nowego losowego hasła
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

            # Ustawienie nowego hasła dla użytkownika
            user.set_password(new_password)
            user.save()

            # Wysłanie e-maila z nowym hasłem (wyświetlanego w konsoli lokalnej)
            subject = "Twoje nowe hasło"
            message = f"Twoje nowe hasło to: {new_password}\nZalecamy, aby po zalogowaniu zmienić hasło na swoje własne."
            from_email = settings.DEFAULT_FROM_EMAIL
            send_mail(subject, message, from_email, [user.email])

            return JsonResponse({"message": "Wysłano e-mail z nowym hasłem."}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Nieprawidłowe dane wejściowe."}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Wystąpił błąd: {str(e)}"}, status=500)

    return JsonResponse({"error": "Nieobsługiwana metoda żądania. Użyj POST."}, status=405)
