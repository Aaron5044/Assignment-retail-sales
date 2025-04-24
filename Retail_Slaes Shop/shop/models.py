from django.db import models
from django.contrib.auth.models import User
import datetime
import os

def getFileName(request, filename):
    current_time = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")
    new_filename = "%s%s"%(current_time, filename)
    return os.path.join('uploads/', new_filename)

class Catagory(models.Model):
    name = models.CharField(max_length = 150,null = False,blank = False)
    image = models.ImageField(upload_to = getFileName, null = True,blank = True)
    desc = models.TextField(max_length=500,null=False,blank=False)
    status = models.BooleanField(default=False,help_text="0-Show,1-Hidden")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Products(models.Model):
    category=models.ForeignKey(Catagory, on_delete=models.CASCADE)
    name = models.CharField(max_length = 150,null = False,blank = False)
    vendor = models.CharField(max_length = 150,null = False,blank = False)
    prod_image = models.ImageField(upload_to = getFileName, null = True,blank = True)
    quantity=models.IntegerField(null=False, blank=False)
    original_price=models. FloatField(null=False, blank=False)
    selling_price=models. FloatField(null=False, blank=False)
    desc = models.TextField(max_length=500,null=False,blank=False)
    status = models.BooleanField(default=False,help_text="0-Show,1-Hidden")
    trending = models.BooleanField(default=False,help_text="0-Default,1-Trending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE) 
    product=models.ForeignKey(Products, on_delete=models.CASCADE) 
    product_qty=models.IntegerField(null=False, blank=False)
    created_at=models.DateTimeField (auto_now_add=True)
        

        