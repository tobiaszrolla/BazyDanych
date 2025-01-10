from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from ..forms import RegistrationForm, LoginForm
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import Samochód

from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_superuser

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
    return render(request, "szkola_jazdy/add_car.html")

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
    return render(request, "szkola_jazdy/delete_car.html")
'''
@csrf_exempt
@user_passes_test(is_admin)
def modify_car(request, registration_number):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            registration_number = data.get("registration_number")

            # Sprawdzenie, czy numer rejestracyjny został podany
            if not registration_number:
                return JsonResponse({"error": "Numer rejestracyjny jest wymagany."}, status=400)

            # Pobranie samochodu do modyfikacji
            car = Samochód.objects.get(registration_number=registration_number)

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

    return render(request, "szkola_jazdy/modify_car.html")'''
@csrf_exempt
@user_passes_test(is_admin)
def modify_car(request):
    if request.method == "PUT":
        try:
            # Parsowanie danych JSON z żądania
            data = json.loads(request.body)
            registration_number = data.get("registration_number")

            # Sprawdzenie, czy numer rejestracyjny został podany
            if not registration_number:
                return JsonResponse({"error": "Numer rejestracyjny jest wymagany."}, status=400)

            # Pobranie samochodu do modyfikacji
            car = Samochód.objects.get(registration_number=registration_number)

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

    return render(request, "szkola_jazdy/modify_car.html")
