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


def home(request):
    return render(request, 'szkola_jazdy/home.html')


def info(request):
    return render(request, 'szkola_jazdy/info.html')

def loggedin(request):
    return render(request, 'szkola_jazdy/loggedin.html')

def Hinstruktor(request):
    return render(request, 'szkola_jazdy/Hinstruktor.html')

def Hadmin(request):
    return render(request, 'szkola_jazdy/Hadmin.html')

def Huser(request):
    return render(request, 'szkola_jazdy/Huser.html')

