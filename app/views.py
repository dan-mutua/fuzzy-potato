from django.shortcuts import render
from django.views import View
from .models import *
from .forms import*
from .models import Product
from  django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from dotenv import load_dotenv
import os

from django.http import FileResponse
from django.shortcuts import get_object_or_404


# def home(request):

class ProductView(View):
    def get(self, request):
        finance = Product.objects.filter(category='Finance')
        mindfulness = Product.objects.filter(category='Mindfulness')

        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
        else:
            totalitems = 0

        context = {
            'finance': finance,
            'mindfulness': mindfulness,
            'totalitems': totalitems
        }
        return render(request, 'app/home.html', context)


class productDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(id=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
            item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()

        else:
            totalitems=0
        context={'product':product,'item_already_in_cart':item_already_in_cart,'totalitems':totalitems}
        return render(request, 'app/productdetail.html',context)


def download_pdf(request, pdf_file_id):
        """
        Returns the PDF file with the given ID.
        """
        pdf_file = get_object_or_404(Product, pk=pdf_file_id)
        if pdf_file.is_purchased:
            response = FileResponse(pdf_file.pdf_files.file)
            response['Content-Disposition'] = 'attachment; filename={}'.format(pdf_file.title)
            return response
        else:
            return HttpResponse(status=403)
  
@login_required
def add_to_cart(request):
    user=request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user =request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
        else:
            totalitems=0
        if cart_product:
            for p in cart_product:
                tempamount = (p.quatity * p.product.selling_price)
                amount += tempamount
                total_amount = amount 
            context ={'carts':cart,'amount':amount,'total_amount':total_amount,'totalitems':totalitems}
            return render(request, 'app/addtocart.html',context)
        else:
             return render(request, 'app/emptycart.html')
    
def plus_cart(request):
    if request.method == 'GET':
        prod_id =request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id,) & Q(user=request.user))
        c.quatity +=1
        c.save()
        amount = 0.0
 
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        print(cart_product)
        for pr in cart_product:
            tempamount = (pr.quatity * pr.product.selling_price)
            amount = amount+tempamount
            
            
        data = {
            'quatity':c.quatity,
            'amount':amount,
            'totalamount':amount + 70.6
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id =request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id,) & Q(user=request.user))
        c.quatity -=1
        c.save()
        amount = 0.0
 
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        print(cart_product)
        for pr in cart_product:
            tempamount = (pr.quatity * pr.product.selling_price)
            amount = amount+tempamount
            
            
        data = {
            'quatity':c.quatity,
            'amount':amount,
            'totalamount':amount + 70.6
        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id =request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id,) & Q(user=request.user))
        c.delete()
        amount = 0.0
 
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        print(cart_product)
        for pr in cart_product:
            tempamount = (pr.quatity * pr.product.selling_price)
            amount = amount+tempamount
            
            
        data = {
            'amount':amount,
            'totalamount':amount + 70.6
        }
        return JsonResponse(data)
    

def buy_now(request):
    return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
    add = Customer.objects.filter(user=request.user)
    if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
    context = {'add':add,'totalitems':totalitems}
    return render(request, 'app/address.html',context)

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
    context={'order_palced':op,'totalitems':totalitems}
    return render(request, 'app/orders.html',context)




def mindfulnessBooks(request):
    mindfulness = Product.objects.filter(category='mindfulness')
    context={'mindfulness':mindfulness}
    return render(request, 'app/laptop.html',context)

def financebooks(request):
    finance= Product.objects.filter(category='Finance')
    context={'finance':finance}
    return render(request, 'app/bottomwear.html',context)

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        context = {'form':form}
        return render(request, 'app/customerregistration.html',context)
    
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations!!! you registered succesfully ')
        context = {'form':form}
        return render(request, 'app/customerregistration.html',context)
@login_required
def checkout(request):
    user = request.user
    load_dotenv() 
    paypal_client_id = os.getenv('PAYPAL_CLIENT_ID')
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
    if cart_product:
        for p in cart_product:
            temamount=(p.quatity * p.product.selling_price)
            amount =temamount
        total_amount=amount
    context={'add':add,'totalamount':total_amount,'cartitems':cart_items,'totalitems':totalitems,'paypal_client_id': paypal_client_id}
    return render(request, 'app/checkout.html',context)

@login_required
def payment_done(request):
    user = request.user
    print("__________________________________________")
    custid=request.GET.get('custid')
    print("hello")
    print(custid)
    customer = Customer.objects.get(id=custid)
    print(customer)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quatity=c.quatity).save()
        c.delete()
    return redirect('orders')

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form =CustomerProfileForm()
        context = {'form':form}
        return render(request,'app/profile.html',context)
    def post(self,request):
        form =CustomerProfileForm(request.POST)
        context = {'form':form}
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            redirect('/profile/')
            messages.success(request,'Congragulation !!! Profile updated successfully')
            reg =Customer
            form =CustomerProfileForm('')
        return render(request,'app/profile.html',context)


