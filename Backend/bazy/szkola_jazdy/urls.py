from django.urls import path
from . import views
from django.urls import reverse


app_name = 'szkola_jazdy'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('add_room/',views.add_room, name='add_room'),
    path('add_car/', views.add_car, name='add_car')
]
