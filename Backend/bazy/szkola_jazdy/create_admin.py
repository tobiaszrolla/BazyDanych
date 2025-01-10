'''from .models import (Użytkownik)

def create_admin():
    if not Użytkownik.objects.filter(email='admin@domain.com').exists():
        admin = Użytkownik.objects.create_superuser(
            username='admin',
            email='admin@domain.com',
            password='strong_password',
            imię='admin',
            nazwisko='admin'
        )
        print("Administrator został utworzony!")
        return admin
    else:
        print("Administrator już istnieje.")
        return Użytkownik.objects.get(email='admin@domain.com')
'''

