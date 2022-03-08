from itertools import product
from typing import final
from django.db import models


# Create your models here.
class MainCat(models.Model):
    mcid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class SubCat(models.Model):
    scid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Brand(models.Model):
    bid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Seller(models.Model):
    sid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    addressline1 = models.CharField(max_length=30,default=None,null=True,blank=True)
    addressline2 = models.CharField(max_length=30,default=None,null=True,blank=True)
    addressline3 = models.CharField(max_length=30,default=None,null=True,blank=True)
    pin = models.CharField(max_length=30,default=None,null=True,blank=True)
    city = models.CharField(max_length=30,default=None,null=True,blank=True)
    state = models.CharField(max_length=30,default=None,null=True,blank=True)
    pic = models.ImageField(upload_to="images/",default=None,null=True,blank=True)

    def __str__(self):
        return self.username

class Product(models.Model):
    pid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    mainCat = models.ForeignKey(MainCat,on_delete=models.CASCADE)
    subCat = models.ForeignKey(SubCat,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller,on_delete=models.CASCADE)
    basePrice = models.IntegerField()
    discount = models.IntegerField(default=0,null=True,blank=True)
    finalPrice = models.IntegerField(default=0,null=True,blank=True)
    color = models.CharField(max_length=20)
    size = models.CharField(max_length=10)
    description = models.TextField()
    time = models.DateTimeField(auto_now=True)
    stock = models.BooleanField(default=True)
    pic1 = models.ImageField(upload_to="images/")
    pic2 = models.ImageField(upload_to="images/")
    pic3 = models.ImageField(upload_to="images/")
    pic4 = models.ImageField(upload_to="images/")

    def __str__(self):
        return str(self.pid)+"\t"+self.name


class Buyer(models.Model):
    bid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    addressline1 = models.CharField(max_length=30,default=None,null=True,blank=True)
    addressline2 = models.CharField(max_length=30,default=None,null=True,blank=True)
    addressline3 = models.CharField(max_length=30,default=None,null=True,blank=True)
    pin = models.CharField(max_length=30,default=None,null=True,blank=True)
    city = models.CharField(max_length=30,default=None,null=True,blank=True)
    state = models.CharField(max_length=30,default=None,null=True,blank=True)
    pic = models.ImageField(upload_to="images/",default=None,null=True,blank=True)

    def __str__(self):
        return self.username

class Wishlist(models.Model):
    wid = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)


    def __str__(self):
        return str(self.eid)+"\t"+self.buyer.username

class Checkout(models.Model):
    cid = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    product = models.TextField()
    total = models.IntegerField()
    shipping = models.IntegerField()
    final = models.IntegerField()
    final = models.IntegerField()
    time = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.cid+ " "+self.buyer.username+" "+str(self.active)
    