from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from .forms import RegistrationForm, LoginForm
from django.views.generic import TemplateView


def register(request):
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


def home(request):
    return render(request, 'szkola_jazdy/home.html')

class LoginView(TemplateView):
    def get(self, request):
        form = LoginForm()
        return render(request, 'szkola_jazdy/login.html', {'form': form})

#Testowanie