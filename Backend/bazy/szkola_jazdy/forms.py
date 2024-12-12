from django import forms
from django.contrib.auth.models import User
from .models import Użytkownik

from szkola_jazdy.models import Użytkownik



#Ma działać na naszej encji
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label="Potwierdź hasło")

    class Meta:
        model = Użytkownik  # Formularz powiązany z modelem 'Użytkownik'
        fields = ['imię', 'nazwisko', 'email', 'nrTelefonu', 'typ_użytkownika', 'data_urodzenia']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError('Hasła nie pasują do siebie.')
        return password_confirm

#formularz logowania
class LoginForm(forms.Form):
    username = forms.CharField(label='Email', max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Użytkownik
        fields = ['email', 'username']