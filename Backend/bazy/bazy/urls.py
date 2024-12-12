from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', include('szkola_jazdy.urls')),
    path('', include('szkola_jazdy.urls')),
]
