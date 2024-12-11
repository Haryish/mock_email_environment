from django.urls import path
from .views import create_transaction

urlpatterns = [
    path('api/transaction/', create_transaction, name='create_transaction'),
]
