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
from .models import Użytkownik
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

'''def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False  # Ustawiamy użytkownika na nieaktywny
            user.save()

            # Generowanie tokena aktywacji
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode())
            mail_subject = 'Weryfikacja adresu e-mail'
            message = render_to_string('account/activation_email.html', {
                'user': user,
                'domain': 'twoja-domena.com',
                'uid': uid,
                'token': token,
            })
            send_mail(mail_subject, message, 'no-reply@yourdomain.com', [user.email])

            #return redirect('szkola_jazdy:login')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'szkola_jazdy/register.html', {'form': form})
'''

def home(request):
    return render(request, 'szkola_jazdy/home.html')
'''
class LoginView(TemplateView):
    def get(self, request):
        form = LoginForm()
        return render(request, 'szkola_jazdy/login.html', {'form': form})
'''
