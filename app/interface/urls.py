from django.urls import path
from interface import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:code>/', views.details, name='details')
]