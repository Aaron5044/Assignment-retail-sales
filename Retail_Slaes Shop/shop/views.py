from http.client import HTTPResponse
import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from shop.form import CustomUserForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

def home(request):
    return render(request,"store/index.html")


import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Products, Cart  # Assuming your models are in the same directory

def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            try:
                data = json.loads(request.body)  # Load JSON data from request body
                product_qty = int(data.get('product_qty'))  # Access product quantity using .get() to avoid KeyError
                product_id = int(data.get('pid'))  # Access product ID using .get()
            except (json.JSONDecodeError, ValueError, KeyError) as e:
                return JsonResponse({'status': f'Invalid JSON data: {str(e)}'}, status=400)  # Handle JSON decoding errors and missing keys

            try:
                product_status = get_object_or_404(Products, id=product_id)  # Get product or return 404 if not found
            except Products.DoesNotExist:
                return JsonResponse({'status': 'Product Not Found'}, status=404)

            if Cart.objects.filter(user=request.user, product=product_status).exists():
                return JsonResponse({'status': 'Product Already in Cart'}, status=200)
            else:
                if product_status.quantity >= product_qty:
                    Cart.objects.create(user=request.user, product=product_status, product_qty=product_qty)
                    return JsonResponse({'status': 'Product Added to Cart'}, status=200)
                else:
                    return JsonResponse({'status': 'Product Stock Not Available'}, status=200)
        else:
            return JsonResponse({'status': 'Login to Add Cart'}, status=401)  # Use 401 Unauthorized status code
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=400)  # Use 400 Bad Request status code

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out Successfully")
    return redirect("/")
        

def login_page(request):
    if request.method=='POST':
        name=request.POST.get('username')
        pwd=request.POST.get('password')
        user=authenticate(request, username=name, password=pwd)
        if user is not None:
            login(request,user)
            messages.success(request, "Logged in Successfully")
            return redirect("/") 
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect("/login") 
    return render(request,"store/login.html")

def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration Successfull')
            return redirect('/login')
    return render(request,"store/register.html", {'form' : form})

def collections(request):
    catagory=Catagory.objects.filter(status=0)
    return render(request,"store/collections.html",{"catagory" : catagory})

def collectionsview(request,name):
    if(Catagory.objects.filter(name=name,status=0)):
        products=Products.objects.filter(category__name=name)
        return render(request,"store/products/index.html",{"products" : products,"category_name": name })
    else:
        messages.warning(request, "No catagory")
        return redirect('collections')
    

def product_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
        if(Products.objects.filter(name=pname,status=0)):
            products=Products.objects.filter(name=pname,status=0).first()
            return render(request,"store/products/product_details.html",{"products" : products})
        else:
            messages.error(request, "No catagory")
            return redirect('collections')
    else:
        messages.error(request, "No catagory")
        return redirect('collections')
    

