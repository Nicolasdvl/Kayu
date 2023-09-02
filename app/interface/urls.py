from django.urls import path
from interface import views

urlpatterns = [
    path('', views.home),
]