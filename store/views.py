from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user

# Create your views here.
@login_required
def Dashboard(request):
    return render(request, 'dashboard.html')

@unauthenticated_user
def Login(request):
    return render(request, 'login.html')