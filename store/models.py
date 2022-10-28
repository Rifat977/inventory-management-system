from email.policy import default
from pyexpat import model
from secrets import choice
from django.db import models
from django.contrib.auth.models import AbstractUser

unit = (
    ('PC', 'PC'),
    ('KG', 'KG')
)

# Create your models here.
class User(AbstractUser):
    @property
    def is_supplier(self):
        if hasattr(self, 'supplier'):
            return True
        return False

    @property
    def is_buyer(self):
        if hasattr(self, 'buyer'):
            return True
        return False
    
    @property
    def is_admin(self):
        if hasattr(self, 'admin'):
            return True
        return False

class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=220)
    phone = models.CharField(max_length=11)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=220)
    phone = models.CharField(max_length=11)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=220)
    phone = models.CharField(max_length=11)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=55, blank=False, null=False)
    price = models.FloatField(blank=False, null=False)
    qty = models.IntegerField(blank=False, null=False)
    unit = models.CharField(choices=unit, default='PC', max_length=15)
    image = models.ImageField(upload_to='images', blank=True, null=False)

    def __str__(self):
        return self.name

class Cart(models.Model):
    seller_id = models.IntegerField(blank=False, null=False)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(blank=False, null=False)

    @property
    def sub_total(self):
        return self.product.price * self.qty
