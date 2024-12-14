from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('add_car/', views.add_car, name='add_car'),
    path('add_room/', views.add_room, name='add_room'),
    path('delete_car/<str:registration_number>/', views.delete_car, name='delete_car'),
    path('delete_room/<str:room_name>/', views.delete_room, name='delete_room'),
    path('delete_user/<str:email>/', views.delete_user, name='delete_user'),
    path('', views.home, name='home'),
]
