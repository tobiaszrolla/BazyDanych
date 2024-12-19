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
from django.contrib.auth.hashers import make_password
from ..models import Sala
from django.contrib.auth import logout, authenticate, login as django_login #konflikt nazw z widokiem login()
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime

def is_admin(user):
    return user.is_superuser

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
def modify_room(request, nazwa):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            room = Sala.objects.get(nazwa=nazwa)
            # Logika modyfikacji
            room.availability = data.get('availability', room.availability)
            room.capacity = data.get('capacity', room.capacity)
            room.save()
            return JsonResponse({"message": "Sala została zmodyfikowana pomyślnie!"}, status=200)
        except Sala.DoesNotExist:
            return JsonResponse({"error": "Sala o tej nazwie nie istnieje."}, status=404)
        except Exception as e:
            return JsonResponse({"error": f"Wystąpił błąd: {str(e)}"}, status=500)

    # Jeśli metoda żądania nie jest PUT
    return JsonResponse({"error": "Nieobsługiwana metoda żądania. Użyj PUT."}, status=405)

