from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register((MainCat,
                    SubCat,
                    Brand,
                    Seller,
                    Product,
                    Buyer,
                    Wishlist,
                    Checkout))

