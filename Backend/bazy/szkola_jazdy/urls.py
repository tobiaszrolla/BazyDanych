from django.urls import path
from .views import other_view, sala_views, samochod_views, uzytkownik_views, zajencia_view, kalendarz, transakcje_views

urlpatterns = [
    path('register/', uzytkownik_views.register, name='register'),
    path('login/', uzytkownik_views.login, name='login'),
    path('logout/', uzytkownik_views.logout, name='logout'),
    path('add_car/', samochod_views.add_car, name='add_car'),
    path('add_room/', sala_views.add_room, name='add_room'),
    path('add_zajęcia/', zajencia_view.add_zajęcia, name='add_zajęcia'),  # Dodajemy ten endpoint
    path('delete_car/<str:registration_number>/', samochod_views.delete_car, name='delete_car'),
    path('delete_room/<str:nazwa>/', sala_views.delete_room, name='delete_room'),
    path('delete_user/<str:email>/', uzytkownik_views.delete_user, name='delete_user'),
    path('delete_zajęcia/<str:zajęcia_id>/', zajencia_view.delete_zajęcia, name='delete_zajęcia'),
    path('modify_car/<str:registration_number>/', samochod_views.modify_car, name='modify_car'),
    path('modify_room/<str:nazwa>/', sala_views.modify_room, name='modify_room'),
    path('modify_user/<str:email>/', uzytkownik_views.modify_user, name='modify_user'),
    path('zapisz_na_zajęcia/<str:zajęcia_id>/', zajencia_view.zapisz_na_zajęcia, name='zapisz_na_zajęcia'),
    path('dostępne_zajęcia/', zajencia_view.dostępne_zajęcia, name='dostępne_zajęcia'),
    path('reset_password_request/', uzytkownik_views.reset_password_request, name='reset_password_request'),
    path('zapisz_na_kurs/', uzytkownik_views.zapisz_na_kurs, name='zapisz_na_kurs'),
    path('dodaj_opinie/', uzytkownik_views.dodaj_opinie, name='dodaj_opinie'),
    path('kalendarz/', zajencia_view.kalendarz, name='kalendarz'),
    path('transakcja/<int:zajęcia_id>/<int:kursant_id>/', transakcje_views.transakcja, name='transakcja'),
    path('zakoncz_zajecia/<int:zajęcia_id>/<int:kursant_id>/', zajencia_view.zakoncz_zajecia, name='zakoncz_zajecia'),
    path('zajęcia/<int:zajęcia_id>/zapisz/', zajencia_view.zapisz_na_zajęcia, name='zapisz_na_zajacia'),
    path('verify_code/', uzytkownik_views.verify_code, name='verify_code'),
    path('', other_view.home, name='home'),
    path('info/', other_view.info, name='info'),
    path('loggedin/', other_view.loggedin, name='loggedin'),
    path('zapiskurs/', uzytkownik_views.zapisz_na_kurs, name='zapiskurs')
]