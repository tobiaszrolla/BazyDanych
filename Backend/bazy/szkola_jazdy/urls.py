from django.urls import path
from .views import other_view, sala_views, samochod_views,uzytkownik_views,zajencia_view

urlpatterns = [
    path('register/', uzytkownik_views.register, name='register'),
    path('login/', uzytkownik_views.login, name='login'),
    path('logout/', uzytkownik_views.logout, name='logout'),
    path('add_car/', samochod_views.add_car, name='add_car'),
    path('add_room/', sala_views.add_room, name='add_room'),
    path('add_zajęcia/', zajencia_view.add_zajęcia, name='add_zajęcia'),  # Dodajemy ten endpoint
    path('delete_car/<str:registration_number>/', samochod_views.delete_car, name='delete_car'),
    path('delete_room/<str:room_name>/', sala_views.delete_room, name='delete_room'),
    path('delete_user/<str:email>/', uzytkownik_views.delete_user, name='delete_user'),
    path('delete_zajęcia/<str:numer_zajęć>/', zajencia_view.delete_zajęcia, name='delete_zajęcia'),
    path('zapisz_na_zajęcia/<str:zajęcia_id>/', zajencia_view.zapisz_na_zajęcia, name='zapisz_na_zajęcia'),
    path('zajecia/dostepne/', zajencia_view.dostępne_zajęcia, name='dostępne_zajęcia'),
    path('reset_password_request/', uzytkownik_views.reset_password_request, name='reset_password_request'),
    path('', other_view.home, name='home'),
]
