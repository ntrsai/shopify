
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from seller.models import Product
from user.models import Cart
from django.db.models import Q
from django.contrib import messages
# Create your views here.

products = Product.objects.none()
def home(request):
   data={}
   global products
   global filtered_products
   products = Product.objects.all()
   filtered_products = products
   user_specific_products= Cart.objects.filter(uid=request.user.id)
   data['cart_items']=user_specific_products.count()
   data['products'] = products
   
   return render(request, "user/home.html", context=data)
def register(request):
    data={}
    is_staff = False
    if(request.method=="POST"):
        uname = request.POST['username']
        upass = request.POST['password']
        cpass = request.POST['cpassword']
        utype = request.POST['type']
        print(uname, upass, utype)

        if(utype=='seller'):
            is_staff = True
        
        if(uname=="" or upass=="" or cpass==""):
         data['error_msg'] = "fields cannot be empty"
         return render(request, 'user/register.html', context=data)
        elif(upass != cpass):
         data['error_msg'] = "Password did not match"
         return render(request, 'user/register.html', context=data)
        elif(User.objects.filter(username=uname).exists()):
         data['error_msg'] = uname+" username already exists"
         return render(request, 'user/register.html', context=data)
        else:
         user = User.objects.create(username=uname, is_staff=is_staff)
         user.set_password(upass)
         user.save()
         return redirect("/login")
       
    return render(request, "user/register.html", context=data)

def user_login(request):
   data={}
   if(request.method=="POST"):
      uname=request.POST['username']
      upass=request.POST['password']
      # print(username,password,cpassowrd)
      if(uname=="" or upass==""):
         # print("fields cant be empty")
         data['error_msg']="fields cant be empty"
         return render(request,'user/login.html',context=data)
      elif(not User.objects.filter(username=uname).exists()):
         # print(uname + " is already exist")
         data['error_msg']=uname + " is does not exist"
         return render(request,'user/login.html',context=data)
      else:
         user=authenticate(username=uname, password=upass)
         if user is None:
            data['error_msg']="Wrong password"
            return render(request, "user/login.html", context=data)
         else:
            login(request, user)
            if(user.is_staff==True):
            #   return render(request, "seller/dashboard.html")
                return redirect("/dashboard")
            else:
             return redirect('/')

   return render(request, "user/login.html")

def user_logout(request):
   logout(request)
   return redirect("/")

def add_to_cart(request, product_id):
   if(request.user.is_authenticated):
      user_id = request.user.id 
      user=User.objects.get(id=user_id)
      product=Product.objects.get(id=product_id)
      q1 = Q(pid=product_id)
      q2 = Q(uid=user_id)
      in_cart = Cart.objects.filter(q1 & q2)
      if(in_cart.count()>0):
         messages.error(request, "Product alreday in the cart")
         return redirect("/")
      else:
         cart = Cart.objects.create(uid=user, pid=product)
         cart.save()
         messages.success(request, "Product added to the cart")
         return redirect("/")
   else:
      return redirect("/login")
   

def cart_items_count(request): 
   user_specific_products=Cart.objects.filter(uid=request.user.id)
   print(user_specific_products.count()) 
   user_specific_cart_count=user_specific_products.count() 
   return user_specific_cart_count

def cart(request):
   data={}
   total_items=0
   total_price=0 
   cart_items=Cart.objects.filter(uid=request.user.id) 
   data['products'] = cart_items 
   data['cart_items']=cart_items_count(request) 
   #getting cart items based on quantity 
   for item in cart_items: 
      total_items+=item.quantity 
      total_price+=(item.quantity*item.pid.price) 
   data['total_items' ]=total_items 
   data['total_price']=total_price 
   return render(request, 'user/cart.html',context=data)


def update_cart_quantity(request, flag, cart_id):
   cart_items = Cart.objects.filter(id=cart_id)
   actual_quantity = cart_items[0].quantity
   print("")
   if(flag=="inc"):
      cart_items.update(quantity=actual_quantity+1)
   else:
      if(actual_quantity==1):
         pass
      else:
         cart_items.update(quantity=actual_quantity-1)
   return redirect("/cart")


# sort by category 
# products = Product.objects.none()

def filter_by_category(request, category_value):
   data={}
   global products
   global filtered_products
   filtered_products = products.filter(category=category_value)
   data['products'] = filtered_products
   return render(request, "user/home.html", context=data)

def sort_by_price(request, flag):
   global filtered_products
   data={}
   if(flag=='asc'):
      sorted_products = filtered_products.order_by("price")
   else:
      sorted_products = filtered_products.order_by("-price")
   data['products'] = sorted_products
   return render(request, 'user/home.html', context=data)

def search(request):
   data={}
   if(request.method=="POST"):
      product_name = request.POST.get('product_name')
      print(product_name)
      all_products = Product.objects.all()
      searched_products = all_products.filter(Q(name__icontains=product_name))
      data['products']=searched_products
      return render(request, 'user/home.html', context=data)

def delete_cart_items(request,cart_id):
   cart_item=Cart.objects.get(id=cart_id)
   cart_item.delete()
   return redirect('/cart')

import razorpay
def order_summary(request):
   data1={}
   total_items=0
   total_price=0 
   cart_items=Cart.objects.filter(uid=request.user.id) 
   data1['products'] = cart_items 
   data1['cart_items']=cart_items_count(request) 
   #getting cart items based on quantity 
   for item in cart_items: 
      total_items+=item.quantity 
      total_price+=(item.quantity*item.pid.price) 
   data1['total_items' ]=total_items 
   data1['total_price']=total_price 

   client = razorpay.Client(auth=("rzp_test_XRjX6qJ69ajxxs", "s56837vKNGmoW2BiQkQbC3sH"))
   data = { "amount": total_price*100, "currency": "INR", "receipt": "order_rcptid_11" }
   payment = client.order.create(data=data)

   return render(request, 'user/order_summary.html',context=data1)

