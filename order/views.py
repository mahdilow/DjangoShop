
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect

from cart.cart import Cart

from .models import Order, OrderItem

def start_order(request):
    cart = Cart(request)   
    total_price = 0


    for item in cart:
        product = item['product']
        total_price += product.price * int(item['quantity'])
  


    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    address = request.POST.get('address')
    zipcode = request.POST.get('zipcode')
    place = request.POST.get('place')
    phone = request.POST.get('phone')       
        
        
    order = Order.objects.create(user=request.user, first_name=first_name, last_name=last_name, email=email, phone=phone, address=address, zipcode=zipcode, place=place)
    order.paid_amount = total_price
    order.paid = True
    order.save()

    for item in cart:
        product = item['product']
        quantity = int(item['quantity'])
        price = product.price * quantity

        item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)

    
    return redirect('myaccount')
    
