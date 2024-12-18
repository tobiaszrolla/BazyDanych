from django.conf import settings
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
from ..models import Użytkownik, Samochód, Sala, Zajęcia, KursanciNaZajęciach
from django.contrib.auth import logout, authenticate, login as django_login #konflikt nazw z widokiem login()
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime

def is_admin(user):
    return user.is_superuser
def str_to_time(time_str):
    return datetime.strptime(time_str, "%H:%M:%S").time()
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
        godzina_rozpoczęcia = data.get("godzina_rozpoczęcia")
        godzina_zakończenia = data.get("godzina_zakończenia")
        data = data.get("data")

        if not nazwa_sali and not numer_rejestracyjny:
            return JsonResponse({"error": "Brak sali samochodu."}, status=400)

        if nazwa_sali and not numer_rejestracyjny:
            sala = Sala.objects.filter(nazwa=nazwa_sali).first() #sala wyszukanie
            if not sala: #czy sala istnieje
                print("nie ma takiej sali\n")
                return JsonResponse({"error": "Nie znaleziono sali o podanej nazwie."}, status=404)
            if not sala.availability:
                return JsonResponse({"error": "Sala niedostępna"}, status=400)
            inne_zajęcia = Zajęcia.objects.filter(sala=sala, data=data)
            for zajęcia in inne_zajęcia:    #sprawdzenie czy zajęcia nie nachodzą na siebie
                if not (str_to_time(godzina_rozpoczęcia) >= zajęcia.godzina_zakończenia or
                str_to_time(godzina_zakończenia) <= zajęcia.godzina_rozpoczęcia):
                    return JsonResponse({"error": "Sala jest już zajęta"}, status=400)
            samochód = None
        elif numer_rejestracyjny and not nazwa_sali:
            samochód = Samochód.objects.filter(registration_number=numer_rejestracyjny).first()
            if not samochód:
                print("nie ma takiego numeru\n")
                return JsonResponse({"error": "Nie znaleziono samochodu o podanym numerze rejestracyjnym."}, status=404)
            if not samochód.availability:
                return JsonResponse({"error": "Samochód niedostępny"}, status=400)
            inne_zajęcia = Zajęcia.objects.filter(samochód=samochód, data=data)
            for zajęcia in inne_zajęcia:
                if not (str_to_time(godzina_rozpoczęcia) >= zajęcia.godzina_zakończenia or
                str_to_time(godzina_zakończenia) <= zajęcia.godzina_rozpoczęcia):
                        return JsonResponse({"error": "Samochód jest już zajęty"}, status=400)
            sala = None

        # Pobierz instruktora
        instruktor = request.user

        # Utwórz zajęcia
        zajęcia = Zajęcia.objects.create(
            sala=sala,
            samochód=samochód,
            instruktor=instruktor,
            godzina_rozpoczęcia=godzina_rozpoczęcia,
            godzina_zakończenia=godzina_zakończenia,
            data = data
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
@login_required
def dostępne_zajęcia(request):
    """
    Zwraca listę dostępnych zajęć z informacją o liczbie wolnych miejsc.
    """
    if request.method == "GET":
        try:
            # Adnotacja liczby zapisanych kursantów
            zajęcia_list = Zajęcia.objects.annotate(
                liczba_kursantów=Count('kursanci'),
                wolne_miejsca=('maksymalna_liczba_kursantów') - Count('kursanci')
            ).filter(wolne_miejsca__gt=0).select_related('sala', 'samochód', 'instruktor')

            # Przygotowanie listy zajęć z dodatkowymi informacjami
            events = []
            for zajęcia in zajęcia_list:
                events.append({
                    "id": zajęcia.id,
                    "title": f"Instruktor: {zajęcia.instruktor} | Sala: {zajęcia.sala.nazwa if zajęcia.sala else 'Brak'}",
                    "start": zajęcia.godzina_rozpoczęcia.strftime("%H:%M"),
                    "end": zajęcia.godzina_zakończenia.strftime("%H:%M"),
                    "wolne_miejsca": zajęcia.wolne_miejsca,
                })

            return JsonResponse(events, safe=False, status=200)

        except Exception as e:
            # Obsługa błędów
            return JsonResponse({"error": f"Wystąpił błąd: {str(e)}"}, status=500)

    # Jeśli metoda żądania nie jest GET
    return JsonResponse({"error": "Nieobsługiwana metoda żądania. Użyj GET."}, status=405)


@login_required
@require_POST
def email_na_zajęcia(request, zajęcia_id):
    try:
        zajęcia = Zajęcia.objects.get(id=zajęcia_id)
    except Zajęcia.DoesNotExist:
        return JsonResponse({"error": "Nie znaleziono zajęć."}, status=404)

    # Sprawdzenie, czy użytkownik już jest zapisany
    if KursanciNaZajęciach.objects.filter(użytkownik=request.user, zajęcia=zajęcia).exists():
        return JsonResponse({"error": "Już jesteś zapisany na te zajęcia."}, status=400)

    # Zapisanie użytkownika na zajęcia
    KursanciNaZajęciach.objects.create(użytkownik=request.user, zajęcia=zajęcia)

    # Przygotowanie danych do e-maila
    subject = "Potwierdzenie zapisu na zajęcia"
    message = (
        f"Cześć {request.user.imię},\n\n"
        f"Zostałeś zapisany na zajęcia:\n\n"
        f"Data: {zajęcia.data.strftime('%d.%m.%Y')}\n"
        f"Godzina: {zajęcia.godzina_rozpoczęcia.strftime('%H:%M')} - {zajęcia.godzina_zakończenia.strftime('%H:%M')}\n"
    )
    if zajęcia.sala:
        message += f"Sala: {zajęcia.sala.nazwa}\n"
    if zajęcia.samochód:
        message += f"Samochód: {zajęcia.samochód.model} ({zajęcia.samochód.registration_number})\n"
    if zajęcia.instruktor:
        message += f"Instruktor: {zajęcia.instruktor.imię} {zajęcia.instruktor.nazwisko}\n"

    message += "\nDziękujemy za zapisanie się i do zobaczenia na zajęciach!\n"

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [request.user.email]

    # Wysyłanie e-maila
    try:
        send_mail(subject, message, from_email, recipient_list)
        return JsonResponse({"message": "Zostałeś zapisany na zajęcia! E-mail potwierdzający został wysłany."},
                            status=201)
    except Exception as e:
        return JsonResponse({"error": f"Nie udało się wysłać e-maila: {str(e)}"}, status=500)
