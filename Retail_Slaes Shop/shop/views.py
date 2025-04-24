from http.client import HTTPResponse
from django.shortcuts import redirect, render
from . models import *
from django.contrib import messages

def home(request):
    return render(request,"store/index.html")

def register(request):
    return render(request,"store/register.html")

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
    

