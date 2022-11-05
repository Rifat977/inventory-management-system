from django.contrib import admin
from .models import *
# Register your models here.
class SaleAdmin(admin.ModelAdmin):
    list_display = ('date', 'invoice', 'payable', 'paid', 'customer')
    search_fields = ('date', 'invoice')
    ordering = ['date']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')

admin.site.register(Admin)
admin.site.register(Supplier)
admin.site.register(Buyer)
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Category, CategoryAdmin)