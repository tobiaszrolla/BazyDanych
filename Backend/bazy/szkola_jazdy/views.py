from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from .forms import RegistrationForm, LoginForm
from django.views.generic import TemplateView

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import Użytkownik, Samochód, Sala
from django.contrib.auth import authenticate


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
            user = authenticate(username=email, password=password)

            if user is not None:
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

def home(request):
    return render(request, 'szkola_jazdy/home.html')
@csrf_exempt
def add_car(request):
    if request.method == "POST":
        try:
            # Parsowanie danych JSON z żądania
            data = json.loads(request.body)
            registration_number = data.get("registration_number")
            model = data.get("model")
            production_year = data.get("production_year")
            availability = data.get("availability")

            # Walidacja: Sprawdzanie, czy wymagane dane są dostępne
            if not registration_number or not model or not production_year or availability is None:
                return JsonResponse({"error": "Brak wymaganych danych."}, status=400)

            # Sprawdzenie, czy samochód o tym numerze rejestracyjnym już istnieje
            if Samochód.objects.filter(registration_number=registration_number).exists():
                return JsonResponse({"error": "Samochód o tym numerze rejestracyjnym już istnieje."}, status=400)

            # Tworzenie samochodu
            car = Samochód.objects.create(
                registration_number=registration_number,
                model=model,
                production_year=production_year,
                availability=availability
            )

            return JsonResponse({"message": "Samochód został dodany pomyślnie!", "car_id": car.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Nieprawidłowe dane wejściowe. Upewnij się, że wysyłasz poprawny JSON."}, status=400)

        except Exception as e:
            return JsonResponse({"error": f"Wystąpił błąd: {str(e)}"}, status=500)

    # Jeśli metoda żądania nie jest POST
    return JsonResponse({"error": "Nieobsługiwana metoda żądania. Użyj POST."}, status=405)
@csrf_exempt
def add_room(request):
    if request.method == "POST":
        try:
            # Parsowanie danych JSON z żądania
            data = json.loads(request.body)
            capacity = data.get("capacity")
            availability = data.get("availability")
            nazwa = data.get("nazwa")

            # Walidacja: Sprawdzanie, czy wymagane dane są dostępne
            if not capacity or availability is None or nazwa is None:
                return JsonResponse({"error": "Brak wymaganych danych."}, status=400)

            # Tworzenie sali
            room = Sala.objects.create(
                capacity=capacity,
                availability=availability,
                nazwa=nazwa
            )

            return JsonResponse({"message": "Sala została dodana pomyślnie!", "room_id": room.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Nieprawidłowe dane wejściowe. Upewnij się, że wysyłasz poprawny JSON."}, status=400)

        except Exception as e:
            return JsonResponse({"error": f"Wystąpił błąd: {str(e)}"}, status=500)

    # Jeśli metoda żądania nie jest POST
    return JsonResponse({"error": "Nieobsługiwana metoda żądania. Użyj POST."}, status=405)

