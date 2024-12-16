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
from .models import Użytkownik, Samochód, Sala, Zajęcia, KursanciNaZajęciach
from django.contrib.auth import logout, authenticate, login as django_login #konflikt nazw z widokiem login()
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST

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

def home(request):
    return render(request, 'szkola_jazdy/home.html')
@csrf_exempt
@user_passes_test(is_admin)
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
@user_passes_test(is_admin)
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


@csrf_exempt
@user_passes_test(is_admin)
def delete_car(request, registration_number):
    if request.method == "DELETE":
        try:
            # Pobranie samochodu o danym numerze rejestracyjnym
            car = Samochód.objects.get(registration_number=registration_number)
            car.delete()
            return JsonResponse({"message": "Samochód został usunięty pomyślnie!"}, status=200)
        except Samochód.DoesNotExist:
            return JsonResponse({"error": "Samochód o tym numerze rejestracyjnym nie istnieje."}, status=404)
        except Exception as e:
            return JsonResponse({"error": f"Wystąpił błąd: {str(e)}"}, status=500)

    # Jeśli metoda żądania nie jest DELETE
    return JsonResponse({"error": "Nieobsługiwana metoda żądania. Użyj DELETE."}, status=405)


@csrf_exempt
@user_passes_test(is_admin)
def delete_room(request, nazwa):
    if request.method == "DELETE":
        try:
            # Pobranie sali o danej nazwie
            room = Sala.objects.get(nazwa=nazwa)
            room.delete()
            return JsonResponse({"message": "Sala została usunięta pomyślnie!"}, status=200)
        except Sala.DoesNotExist:
            return JsonResponse({"error": "Sala o tej nazwie nie istnieje."}, status=404)
        except Exception as e:
            return JsonResponse({"error": f"Wystąpił błąd: {str(e)}"}, status=500)

    # Jeśli metoda żądania nie jest DELETE
    return JsonResponse({"error": "Nieobsługiwana metoda żądania. Użyj DELETE."}, status=405)


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
@login_required
def add_zajęcia(request):
    if request.method == "POST":
        # Sprawdzenie, czy użytkownik jest zalogowany
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Musisz być zalogowany, aby stworzyć zajęcia."}, status=401)

        # Sprawdzenie, czy użytkownik ma odpowiedni typ (instruktor lub pracownik)
        if request.user.typ_użytkownika.lower() not in ['instruktor', 'pracownik']:
            return JsonResponse({"error": "Musisz być pracownikiem, aby tworzyć zajęcia."}, status=403)

        # Załaduj dane z żądania
        data = json.loads(request.body)

        # Walidacja, czy nazwa sali lub numer rejestracyjny samochodu nie są puste
        nazwa_sali = data.get("nazwa_sali")
        numer_rejestracyjny = data.get("numer_rejestracyjny")

        if not nazwa_sali and not numer_rejestracyjny:
            return JsonResponse({"error": "Brak sali samochodu."}, status=400)

        if nazwa_sali and not numer_rejestracyjny:
            # Wyszukiwanie sali po nazwie
            sala = Sala.objects.filter(nazwa=nazwa_sali).first()
            if not sala:
                print("nie ma takiej sali\n")
                return JsonResponse({"error": "Nie znaleziono sali o podanej nazwie."}, status=404)
            samochód = None
        elif numer_rejestracyjny and not nazwa_sali:
            # Wyszukiwanie samochodu po numerze rejestracyjnym
            samochód = Samochód.objects.filter(numer_rejestracyjny=numer_rejestracyjny).first()
            if not samochód:
                print("nie ma takiego numeru\n")
                return JsonResponse({"error": "Nie znaleziono samochodu o podanym numerze rejestracyjnym."}, status=404)
            sala = None
        else:
            # Jeśli oba są podane, sprawdzimy oba
            sala = Sala.objects.filter(nazwa=nazwa_sali).first()
            samochód = Samochód.objects.filter(numer_rejestracyjny=numer_rejestracyjny).first()

            if not sala:
                return JsonResponse({"error": "Nie znaleziono sali o podanej nazwie."}, status=404)
            if not samochód:
                return JsonResponse({"error": "Nie znaleziono samochodu o podanym numerze rejestracyjnym."}, status=404)

        # Pobierz instruktora
        instruktor = request.user


        # Utwórz zajęcia
        zajęcia = Zajęcia.objects.create(
            sala=sala,
            samochód=samochód,
            instruktor=instruktor,
            godzina_rozpoczęcia=data.get("godzina_rozpoczęcia"),
            godzina_zakończenia=data.get("godzina_zakończenia")
        )

        # Zwróć odpowiedź
        return JsonResponse({
            "message": "Zajęcia zostały utworzone pomyślnie!"
        }, status=201)

    return JsonResponse({"error": "Nieobsługiwana metoda. Użyj POST."}, status=405)

    return JsonResponse({"error": "Nieobsługiwana metoda żądania. Użyj PUT."}, status=405)


@login_required
@require_POST
def zapisz_na_zajęcia(request, zajęcia_id):
    try:
        zajęcia = Zajęcia.objects.get(id=zajęcia_id)
    except Zajęcia.DoesNotExist:
        return JsonResponse({"error": "Nie znaleziono zajęć."}, status=404)

    # Sprawdzenie, czy kursant już jest zapisany na te zajęcia
    if KursanciNaZajęciach.objects.filter(użytkownik=request.user, zajęcia=zajęcia).exists():
        return JsonResponse({"error": "Już jesteś zapisany na te zajęcia."}, status=400)

    # Zapisanie kursanta na zajęcia
    KursanciNaZajęciach.objects.create(użytkownik=request.user, zajęcia=zajęcia)
    return JsonResponse({"message": "Zostałeś zapisany na zajęcia!"}, status=201)


@login_required
def delete_zajęcia(request, numer_zajęć):
    if request.method == "DELETE":
        # Sprawdzenie, czy użytkownik ma odpowiedni typ
        if request.user.typ_użytkownika.lower() not in ['instruktor', 'pracownik']:
            return JsonResponse({"error": "Musisz być pracownikiem, aby usuwać zajęcia."}, status=403)

        # Wyszukiwanie zajęć po `id`
        zajęcia = Zajęcia.objects.filter(id=numer_zajęć).first()
        if not zajęcia:
            return JsonResponse({"error": "Nie znaleziono zajęć o podanym numerze."}, status=404)

        # Sprawdzenie, czy użytkownik ma uprawnienia do usunięcia zajęć
        if zajęcia.instruktor != request.user:
            return JsonResponse({"error": "Nie masz uprawnień do usunięcia tych zajęć."}, status=403)

        # Usunięcie zajęć
        zajęcia.delete()
        return JsonResponse({"success": "Zajęcia zostały pomyślnie usunięte."}, status=200)

    return JsonResponse({"error": "Nieprawidłowa metoda HTTP."}, status=405)

@csrf_exempt
@user_passes_test(is_admin)
def modify_car(request, registration_number):
    if request.method == "PUT":
        try:
            # Pobranie samochodu do modyfikacji
            car = Samochód.objects.get(registration_number=registration_number)

            # Parsowanie danych JSON z żądania
            data = json.loads(request.body)

            # Aktualizacja danych samochodu
            car.model = data.get("model", car.model)
            car.production_year = data.get("production_year", car.production_year)
            car.availability = data.get("availability", car.availability)

            car.save()
            return JsonResponse({"message": "Dane samochodu zostały zmodyfikowane pomyślnie!"}, status=200)

        except Samochód.DoesNotExist:
            return JsonResponse({"error": "Samochód o tym numerze rejestracyjnym nie istnieje."}, status=404)
        except Exception as e:
            return JsonResponse({"error": f"Wystąpił błąd: {str(e)}"}, status=500)

    return JsonResponse({"error": "Nieobsługiwana metoda żądania. Użyj PUT."}, status=405)

@csrf_exempt
@user_passes_test(is_admin)
def modify_room(request, nazwa):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            room = Sala.objects.get(nazwa=nazwa)
            # Logika modyfikacji
            room.nazwa = data.get('nazwa', room.nazwa)
            room.save()
            return JsonResponse({"message": "Sala została zmodyfikowana pomyślnie!"}, status=200)
        except Sala.DoesNotExist:
            return JsonResponse({"error": "Sala o tej nazwie nie istnieje."}, status=404)
        except Exception as e:
            return JsonResponse({"error": f"Wystąpił błąd: {str(e)}"}, status=500)

    # Jeśli metoda żądania nie jest PUT
    return JsonResponse({"error": "Nieobsługiwana metoda żądania. Użyj PUT."}, status=405)
