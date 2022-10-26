import email
from turtle import update
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib import messages
from .models import Supplier, Buyer, Admin, User
from django.contrib.auth.forms import PasswordChangeForm
import random

# Create your views here.
@login_required
def Dashboard(request):
    return render(request, 'dashboard.html')

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
        
    return render(request, 'supplier.html')