from django.urls import path
from .views import ExchangesListView

urlpatterns = [
    path('', ExchangesListView.as_view()),
]