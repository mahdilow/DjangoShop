import re
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from algoliasearch_django import raw_search
from algoliasearch_django.decorators import register
from django.contrib import messages

from django.shortcuts import render, redirect
from authapp.auth_service import AuthService

from product.models import Product, Category

from .forms import SignUpForm

def HomePage(request):
    products = Product.objects.all()[:8]  # Fetch the first 8 products
    categories = Category.objects.all()  # Fetch all categories

    return render(request, 'core/HomePage.html', {'products': products, 'categories': categories})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('/')
    else:
        form = SignUpForm()

    return render(request, 'core/signup.html', {'form': form})

@login_required
def myaccount(request):
    return render(request, 'core/myaccount.html')

@login_required
def edit_myaccount(request):
    if request.method == 'POST':
        user = request.user
        phone_number = request.POST.get('phone_number')
        otp = request.POST.get('otp')

        # Update basic information
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')

        # If phone number and OTP are provided, verify them
        if phone_number and otp:
            auth_service = AuthService()
            response, status = auth_service.verify_otp(phone_number, otp)
            
            if status == 200:
                user.phone_number = phone_number
                messages.success(request, 'شماره تلفن با موفقیت تایید شد')
            else:
                messages.error(request, response.get('error', 'خطا در تایید شماره تلفن'))
                return render(request, 'core/edit_myaccount.html')

        user.save()
        return redirect('myaccount')
        
    return render(request, 'core/edit_myaccount.html')

def shop(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    active_category = request.GET.get('category', '')

    if active_category:
        products = products.filter(category__slug=active_category)

    query = request.GET.get('query', '')

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    context = {
        'categories': categories,
        'products': products,
        'active_category': active_category
    }

    return render(request, 'core/shop.html', context)

#SAEARCH WITH ALGOLIA
def search(request):
    query = request.GET.get('query', '')  # Get the search query from the URL parameters
    products = []

    if query:
        # Use Algolia to search products
        algolia_results = raw_search(Product, query)  # Perform search using Algolia
        # Collect only the objectIDs from Algolia results
        product_ids = [hit['objectID'] for hit in algolia_results['hits']]
        # Fetch matching products from the database
        products = Product.objects.filter(id__in=product_ids)

    context = {      
        'products': products     
    }

    return render(request, 'core/shop.html', context)


#WITHOUT ALGOLIA (NORMAL SEARCH)
# def search(request):
#     products = Product.objects.all()
    
#     query = request.GET.get('query', '')

#     if query:
#         products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
        
#     context = {      
#         'products': products     
#     }


#     return render(request, 'core/shop.html',context)