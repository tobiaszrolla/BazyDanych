from django.contrib import admin

# Register your models here.
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'create first admin user'

    def handle(self, *args, **kwargs):
        # Sprawdzamy, czy już istnieje superużytkownik
        if not User.objects.filter(is_superuser=True).exists():
            # Tworzymy nowego superużytkownika
            User.objects.create_superuser(
                username='admin',
                email='admin@domain.com',
                password='adminpassword'
            )
            self.stdout.write(self.style.SUCCESS('Superużytkownik został utworzony.'))
        else:
            self.stdout.write(self.style.SUCCESS('Superużytkownik już istnieje.'))
