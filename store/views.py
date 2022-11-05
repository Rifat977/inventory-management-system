from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib import messages
from .models import *
from django.contrib.auth.forms import PasswordChangeForm
from .forms import AddToCartForm, ProductForm
import random
from django.db.models import When, F, Q
from django.db import IntegrityError

# Create your views here.
@login_required
def Dashboard(request):
    total_product = Product.objects.all().count()
    in_stock = Product.objects.filter(
        Q(qty__gte=1)
    ).count()
    warning = Product.objects.filter(
        Q(qty__lte=5) & Q(qty__gte=1)
    ).count()
    out_stock = Product.objects.filter(
        Q(qty=0)
    ).count()
    context = {
        'total_product' : total_product,
        'in_stock' : in_stock,
        'warning' : warning,
        'out_stock' : out_stock
    }
    return render(request, 'dashboard.html', context)

@unauthenticated_user
def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('store:dashboard')
        else:
            messages.info(request, 'Username or password is incorrect')
    return render(request, 'login.html')

@login_required
def Logout(request):
    logout(request)
    return redirect('store:login')

@login_required
def Profile(request):
    if request.user.is_admin:
        user_data = {
            'name' : request.user.admin.name,
            'address' : request.user.admin.address,
            'phone' : request.user.admin.phone,
            'email' : request.user.email,
        }
    elif request.user.is_buyer:
        user_data = {
            'name' : request.user.buyer.name,
            'address' : request.user.buyer.address,
            'phone' : request.user.buyer.phone,
            'email' : request.user.email,
        }
    elif request.user.is_supplier:
        user_data = {
            'name' : request.user.supplier.name,
            'address' : request.user.supplier.address,
            'phone' : request.user.supplier.phone,
            'email' : request.user.email,
        }
    context = {
        'user':user_data
    }

    if request.method=='POST':
        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']
        email = request.POST['email']
        user = User.objects.get(id=request.user.id)
        user.email = email
        user.save()
        if request.user.is_admin:
            profile = Admin.objects.get(user=request.user)
        elif request.user.is_buyer:
            profile = Buyer.objects.get(user=request.user)
        elif request.user.is_supplier:
            profile = Supplier.objects.get(user=request.user)
        profile.name = name
        profile.phone = phone
        profile.address = address
        profile.save()
        return redirect('store:profile')

    return render(request, 'profile.html', context)

@login_required()
def ChangePassword(request):

    old_password = request.POST['old_password']
    new_password1 = request.POST['new_password1']
    new_password2 = request.POST['new_password2']
    user = authenticate(username=request.user, password=old_password)
    if user is not None:
        if new_password1 != new_password2:
            messages.info(request, "retype password not matched!")
        else:
            u = User.objects.get(username=request.user)
            u.set_password(new_password1)
            u.save()
            messages.info(request, "Password changes")
    else:
        messages.info(request, "Old password in not correct")
    return redirect('store:profile')

@login_required
def SupplierView(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        rand = str(random.randint(1000,9999))
        username = name.split(" ",)[-1].lower()+ rand
        password = name.split(" ",)[-1].lower()+ rand
        user = User.objects.create_user(
            username=username, password=password, email=email
        )
        Supplier.objects.create(
            user = user, name = name, phone=phone, address=address
        )
    supplier_list = Supplier.objects.all()
    context = {
        'supplier': supplier_list
    }
        
    return render(request, 'supplier.html', context)

@login_required
def BuyerView(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        rand = str(random.randint(1000,9999))
        username = name.split(" ",)[-1].lower()+ rand
        password = name.split(" ",)[-1].lower()+ rand
        user = User.objects.create_user(
            username=username, password=password, email=email
        )
        Buyer.objects.create(
            user = user, name = name, phone=phone, address=address
        )
    buyer_list = Buyer.objects.all()
    context = {
        'supplier': buyer_list
    }
        
    return render(request, 'buyer.html', context)

@login_required
def CategoryView(request):
    if request.method == 'POST':
        name = request.POST['name']
        slug = name.replace(" ", "-").lower()
        try:
            Category.objects.create(name=name, slug=slug)
        except IntegrityError as e:
            messages.error(request, "Category already exists")
        return redirect('store:category')
    category = Category.objects.all()
    context = {
        'category' : category
    }
    return render(request, "category.html", context)

@login_required
def CategoryDelete(request, pk):
    category = Category.objects.get(id=pk)
    category.delete()
    return redirect('store:category')

@login_required
def CategoryEdit(request, pk):        
    category = Category.objects.get(id=pk)
    if request.method == 'POST': 
        name = request.POST['name']
        slug = name.replace(" ", "-").lower()
        try:
            cat = Category.objects.get(id=pk)
            cat.name = name
            cat.slug = slug
            cat.save()
        except IntegrityError as e:
            messages.error(request, "Category already exists")
        return redirect('store:category')
    context = {
        'category' : category
    }
    return render(request, './edit/category.html', context)


@login_required
def ProductView(request):
    if request.method=='POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('store:product')
    products = Product.objects.all().order_by('-id')
    context = {
        'products': products
    }
        
    return render(request, 'product.html', context)

@login_required
def AddSaleView(request):
    buyer_list = Buyer.objects.all()
    products = Product.objects.all()
    carts = Cart.objects.filter(seller_id=request.user.id)
    total_price = 0
    for item in carts:
        total_price += item.product.price * item.qty
    context = {
        'customers' : buyer_list,
        'products' : products,
        'carts': carts,
        'total_price': total_price
    }
    return render (request, 'sale.html', context)


@login_required
def AddToCart(request):
    if request.method=='POST':
        product_id = request.POST['product']
        qty = request.POST['qty']
        product = Product.objects.get(id=product_id)
        if (int(product.qty)-int(qty)) < 0:
            messages.info(request, "Not enough in stock")
        else:
            if not Cart.objects.filter(product=product_id).exists():
                form = AddToCartForm(request.POST)
                if form.is_valid:
                    form.save()
                    product.qty = product.qty-int(qty)
                    product.save()
            else:
                messages.info(request, "Product already added")
    return redirect('store:sale')

@login_required
def DeleteCartItem(request, pk, qty, product_id):
    product = Product.objects.get(id=product_id)
    product.qty += qty
    product.save()
    item = Cart.objects.get(id=pk)
    item.delete()
    return redirect('store:sale')

@login_required
def AddSale(request):
    if request.method == 'POST':
        payable = request.POST['payable']
        paid = request.POST['paid']
        customer_id = request.POST['customer']
        date = request.POST['date']
        seller = request.POST['seller_id']
        invoice = str(random.randint(100000,999999))
        if Cart.objects.all().exists():
            Sale.objects.create(
                payable=payable, paid=paid, customer_id=customer_id, date=date, invoice=invoice, seller_id=seller
            )
            Cart.objects.all().delete()
    return redirect('store:sale')

@login_required
def SaleReportView(request):
    sales = Sale.objects.all()
    context = {
        'sales':sales
    }
    return render(request, 'sale_report.html', context)
