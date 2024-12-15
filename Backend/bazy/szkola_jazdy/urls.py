from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('car/add/', views.add_car, name='add_car'),
    path('car/delete/<str:registration_number>/', views.delete_car, name='delete_car'),
    path('room/add/', views.add_room, name='add_room'),
    path('room/delete/<str:nazwa>/', views.delete_room, name='delete_room'),
    path('user/modify/<str:email>/', views.modify_user, name='modify_user'),
    path('car/modify/<str:registration_number>/', views.modify_car, name='modify_car'),
    path('room/modify/<str:nazwa>/', views.modify_room, name='modify_room'),
]
