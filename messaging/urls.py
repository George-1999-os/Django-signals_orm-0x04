from django.urls import path
from .views import inbox_view, delete_user

urlpatterns = [
    path('', inbox_view, name='inbox'),
    path('delete/', delete_user, name='delete_user'),
]
