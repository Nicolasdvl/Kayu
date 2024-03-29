from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from product import views

urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('products/<int:code>/', views.ProductDetail.as_view()),
    path('categories/', views.CategoryList.as_view()),
    path('substitutes/', views.ProductSubstitutes.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)