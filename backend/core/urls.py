from django.contrib.auth import views
from django.urls import path

from core.views import HomePage, shop, signup, myaccount, edit_myaccount,search,login
from product.views import product
#app_name='core'
urlpatterns = [
    path('', HomePage, name='frontpage'),
    path('signup/', signup, name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', login, name='login'),
    path('myaccount/', myaccount, name='myaccount'),
    path('myaccount/edit/', edit_myaccount, name='edit_myaccount'),
    path('shop/', shop, name='shop'),
    path('shop/<slug:slug>/', product, name='product'),
    
]