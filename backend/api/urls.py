from django.urls import path, include
from .views import ProductList

urlpatterns = [
    path('products/', ProductList.as_view()),
]
