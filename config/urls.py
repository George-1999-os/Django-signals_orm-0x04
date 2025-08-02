# config/urls.py or django_chat/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('messages/', include('messaging.urls')),  # <-- include messaging app routes
]
