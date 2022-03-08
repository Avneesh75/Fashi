from itertools import product
from django.conf import settings
from django.contrib.messages.api import error
from django.http.response import Http404
from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from mainApp.models import *

count=0
def home(request):
    global count
    cart = request.session.get('cart',None)
    if(cart):
        count=len(cart)
    request.session['count']=count
    return render(request,"index.html",{"Count":count})

@login_required(login_url='/login/')
def checkoutPage(request):
    return render(request,"check-out.html",{"Count":count})

def contactPage(request):
    return render(request,"contact.html",{"Count":count})

def faqPage(request):
    return render(request,"faq.html",{"Count":count})

def productPage(request,num):
    global count
    product = Product.objects.get(pid=num)
    if(request.method=="POST"):
        q = int(request.POST.get('q'))
        cart = request.session.get('cart',None)
        if(cart):
            keys = cart.keys()
            if(str(product.pid) in keys):
                cart[str(product.key)]=cart[str(product.pid)]+q
            else:
                count=count+1
                cart.setdefault(str(product.pid),q)
        else:
            cart = {str(product.pid):q}
            count=count+1
        request.session['cart']=cart
        count=count+1
        return HttpResponseRedirect('/cart/')
    return render(request,"product.html",{"Product":product,
                                        "Count":count})


def registerPage(request):
    if(request.method=="POST"):
        if(request.POST.get('actype')=="seller"):
            s = Seller()
            s.name = request.POST.get('name')
            s.username = request.POST.get('username')
            s.email = request.POST.get('email')
            s.phone = request.POST.get('phone')
            s.pic = request.FILES.get('pic')
            pward = request.POST.get('password')
            cpward= request.POST.get('cpassword')
            if(pward==cpward):
                try:
                    user = User.objects.create_user(username=s.username,
                                                    password=pward,
                                                    email=s.email,
                                                    first_name=s.name
                                                )
                                
                    user.save()
                    s.save()
                    return HttpResponseRedirect("/login/")
                except:
                   messages.error(request,"User Name is Already Taken")
            
            else:
                messages.error(request,"Password and Confirm Password Does not Match")
        else:
            b = Buyer()
            b.name = request.POST.get('name')
            b.username = request.POST.get('username')
            b.email = request.POST.get('email')
            b.phone = request.POST.get('phone')
            b.pic = request.FILES.get('pic')
            pward = request.POST.get('password')
            cpward= request.POST.get('cpassword')
            if(pward==cpward):
                try:
                    user = User.objects.create_user(username=b.username,
                                                    password=pward,
                                                    email=b.email,
                                                    first_name=b.name
                                                )
                                
                    user.save()
                    b.save()
                    return HttpResponseRedirect("/login/")
                except:
                    messages.error(request,"User Name is Already Taken")
            
            else:
                messages.error(request,"Password and Confirm Password Does not Match")
    
    return render(request,"register.html")

def loginPage(request):
    if(request.method=="POST"):
        username = request.POST.get("username")
        password = request.POST.get("pass")
        user = auth.authenticate(username=username,password=password)
        if(user is not None):
            auth.login(request,user)
            if(user.is_superuser):
                return HttpResponseRedirect("/admin/")
            else:
                return HttpResponseRedirect("/profile/")
        else:
            messages.error(request,"Invalid Username or Password")
    return render(request,"login.html")

@login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

@login_required(login_url='/login/')
def Profile(request):
    user = User.objects.get(username=request.user)
    if(user.is_superuser):
        return HttpResponseRedirect("/admin")
    else:
        print(request.user)
        try:
            seller = Seller.objects.get(username=request.user)
            return HttpResponseRedirect("/sellerProfile/")
        except:
            return HttpResponseRedirect("/buyerProfile/")

@login_required(login_url='/login/')
def sellerProfile(request):
    seller = Seller.objects.get(username=request.user)
    product = Product.objects.filter(seller=seller)
    return render(request,"buyerProfile.html",{'User':seller,
                                                'Product':product,
                                                })

@login_required(login_url='/login/')
def buyerProfile(request):
    buyer = Buyer.objects.get(username=request.user)
    wishlist = Wishlist.objects.filter(buyer=buyer)
    return render(request,"buyerProfile.html",{'User':buyer,
                                                'Wishlist':wishlist, 
                                                "Count":count,                                           
                                                })

@login_required(login_url='/login/')
def editProfileSeller(request):
    s = Seller.objects.get(username=request.user)
    if(request.method=="POST"):
        s.name = request.POST.get('name')
        s.email = request.POST.get('email')
        s.phone = request.POST.get('phone')
        s.addressline1 = request.POST.get('addressline1')
        s.addressline2 = request.POST.get('addressline1')
        s.addressline3 = request.POST.get('addressline1')
        s.pin = request.POST.get('pin')
        s.city = request.POST.get('city')
        s.state = request.POST.get('state')
        if(not request.FILES.get('pic')==None): 
            s.pic = request.FILES.get('pic')
        s.save()
        return HttpResponseRedirect('/sellerProfile')   
    return render(request,"editProfile.html",{'User':s})

@login_required(login_url='/login/')
def editProfileBuyer(request):
    b = Buyer.objects.get(username=request.user)
    if(request.method=="POST"):
        b.name = request.POST.get('name')
        b.email = request.POST.get('email')
        b.phone = request.POST.get('phone')
        b.addressline1 = request.POST.get('addressline1')
        b.addressline2 = request.POST.get('addressline1')
        b.addressline3 = request.POST.get('addressline1')
        b.pin = request.POST.get('pin')
        b.city = request.POST.get('city')
        b.state = request.POST.get('state')
        if(not request.FILES.get('pic')==None): 
            b.pic = request.FILES.get('pic')
        b.save()
        return HttpResponseRedirect('/buyerProfile')   
    return render(request,"editProfileBuyer.html",{'User':b,
                                            "Count":count,
                                            })

def shopPage(request,MC,SC,BR):
    mainCat = MainCat.objects.all()
    subCat = SubCat.objects.all()
    brand = Brand.objects.all()
    if(MC=="d" and SC=="d" and BR=="d"):
        product = Product.objects.all()
    elif(MC!="d" and SC=="d" and BR=="d"):
        product = Product.objects.filter(mainCat=mainCat.objects.get(name=MC))
    elif(MC=="d" and SC!="d" and BR=="d"):
        product = Product.objects.filter(subCat=subCat.objects.get(name=SC))
    elif(MC=="d" and SC=="d" and BR!="d"):
        product = Product.objects.filter(brand=Brand.objects.get(name=BR)) 
    elif(MC!="d" and SC!="d" and BR=="d"):
        product = Product.objects.filter(mainCat=mainCat.objects.get(name=BR),subCat=subCat.objects.get(name=SC))   
    elif(MC!="d" and SC=="d" and BR!="d"):
        product = Product.objects.filter(mainCat=mainCat.objects.get(name=BR),brand=Brand.objects.get(name=BR))  
    elif(MC=="d" and SC!="d" and BR!="d"):
        product = Product.objects.filter(subCat=subCat.objects.get(name=SC),brand=Brand.objects.get(name=BR)) 
    else:
        product = Product.objects.filter(subCat=subCat.objects.get(name=SC),brand=Brand.objects.get(name=BR),mainCat=mainCat.objects.get(name=BR)) 
    
    product=product[::-1]
    return render(request,"shop.html",{
                            "mainCat":mainCat,
                            "subCat":subCat,
                            "Brand":brand,
                            "Product":product,
                            "MC":MC,
                            "BR":BR,
                            "SC":SC,
                            "Count":count,
    })


def cartPage(request):
    cart = request.session.get('cart',None)
    if(request.method=='POST'):
        q = int(request.POST.get('q'))
        if(q>0):
            pid = request.POST.get('pid')
            cart[str(pid)]=q
            request.session['cart']=cart
    cart = request.session.get('cart',None)
    products = []
    subtotal = 0
    total = 0
    shipping = 0
    if(cart):  
        for i in cart.keys():
            p = Product.objects.get(pid=int(i))
            products.append(p)
            subtotal = subtotal+p.finalPrice*cart[i]
        if(subtotal<1000):
            shipping = 150
        else:
            shipping=0
        total = subtotal+shipping
    return render(request,"shopping-cart.html",{"Products":products,
                                                "SubTotal":subtotal,
                                                "Shipping":shipping,
                                                "Total":total,
                                                "Count":count,
                                                })

def deleteCart(request,pid):
    global count
    cart = request.session.get('cart',None)
    if(cart):
        cart.pop(str(pid))
        request.session['cart']=cart
        count=count-1
        return HttpResponseRedirect("/cart/")


@login_required(login_url='/login/')
def addProduct(request):
    mainCat = MainCat.objects.all()
    subCat = SubCat.objects.all()
    brand = Brand.objects.all()
    if(request.method=="POST"):
        p = Product()
        p.name = request.POST.get("name")
        p.mainCat = MainCat.objects.get(name = request.POST.get("mainCat"))
        p.subCat = SubCat.objects.get(name = request.POST.get("subCat"))
        p.brand = Brand.objects.get(name = request.POST.get("brand"))
        p.seller = Seller.objects.get(username=request.user)
        p.basePrice = int(request.POST.get("baseprice"))
        p.discount = int(request.POST.get("discount"))
        p.finalPrice = p.basePrice- p.basePrice*p.discount/100
        p.color = request.POST.get("color")
        p.size = request.POST.get("size")
        p.stock = bool(request.POST.get("stock"))
        p.description = request.POST.get("description")
        p.specification = request.POST.get("specification")
        p.pic1 = request.FILES.get("pic1")
        p.pic2 = request.FILES.get("pic2")
        p.pic3 = request.FILES.get("pic3")
        p.pic4 = request.FILES.get("pic4")
        p.save()
        return HttpResponseRedirect("/sellerProfile/")
    return render (request,"addProduct.html",{
                            "MC":mainCat,
                            "SC":subCat,
                            "BR":brand
                            })

@login_required(login_url='/login/')
def editProduct(request,num):
    mainCat = MainCat.objects.all()
    subCat = SubCat.objects.all()
    brand = Brand.objects.all()
    p = Product.objects.get(pid=num)
    if(request.method=="POST"):

        p.name = request.POST.get("name")
        p.mainCat = MainCat.objects.get(name = request.POST.get("mainCat"))
        p.subCat = SubCat.objects.get(name = request.POST.get("subCat"))
        p.brand = Brand.objects.get(name = request.POST.get("brand"))
        p.seller = Seller.objects.get(username=request.user)
        p.basePrice = int(request.POST.get("baseprice"))
        p.discount = int(request.POST.get("discount"))
        p.finalPrice = p.basePrice- p.basePrice*p.discount/100
        p.color = request.POST.get("color")
        p.size = request.POST.get("size")
        p.stock = bool(request.POST.get("stock"))
        p.description = request.POST.get("description")
        p.specification = request.POST.get("specification")
        if( not request.FILES.get("pic1")==None):
            p.pic1 = request.FILES.get("pic1")
        if( not request.FILES.get("pic2")==None):
            p.pic2 = request.FILES.get("pic2")
        if( not request.FILES.get("pic3")==None):
            p.pic3 = request.FILES.get("pic3")
        if( not request.FILES.get("pic4")==None):
            p.pic4 = request.FILES.get("pic4")
        p.save()
        return HttpResponseRedirect("/sellerProfile/")
    return render (request,"editProduct.html",{
                            "MC":mainCat,
                            "SC":subCat,
                            "BR":brand,
                            "Product":p
                            })

@login_required(login_url='/login/')
def deleteProduct(request,num):
    product= Product.objects.get(pid=num)
    seller = Seller.objects.get(username=request.user)
    if(product.seller==seller):
        product.delete()
    return HttpResponseRedirect('/sellerProfile/')



@login_required(login_url='/login/')
def wishlist(request,num):
    product= Product.objects.get(pid=num)
    buyer = Buyer.objects.get(username=request.user)
    wishlist = Wishlist.objects.filter(buyer=buyer)
    flag = False
    for i in Wishlist:
        if(product==i.product):
            flag = True
    if(flag==False):
        w = Wishlist()
        w = product=product
        w.buyer=buyer
        w.save()
    return HttpResponseRedirect('/buyerProfile/')


@login_required(login_url='/login/')
def deleteWishlist(request,num):
    wishlist= Wishlist.objects.get(wid=num)
    buyer = Buyer.objects.get(username=request.user)
    if(wishlist.buyer==buyer):
        wishlist.delete()
    return HttpResponseRedirect('/buyerProfile/')
    
