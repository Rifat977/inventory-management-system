from ast import Delete
from django.urls import path
from . import views
app_name= 'store'
urlpatterns = [
    path('', views.Dashboard, name="dashboard"),

    path('login/', views.Login, name="login"),
    path('logout/', views.Logout, name="logout"),

    path('profile/', views.Profile, name="profile"),
    path('change_password/', views.ChangePassword, name="change_password"),

    path('supplier/', views.SupplierView, name="supplier"),
    path('buyer/', views.BuyerView, name="buyer"),

    path('product/', views.ProductView, name="product"),
    path('category/', views.CategoryView, name="category"),
    path('category/edit/<int:pk>/', views.CategoryEdit, name="category-edit"),
    path('category/update/<int:pk>', views.CategoryEdit, name="category-update"),
    path('category/delete/<int:pk>', views.CategoryDelete, name="category-delete"),
    
    path('sale/', views.AddSaleView, name="sale"),
    path('sale-report/', views.SaleReportView, name="sale-report"),
    path('add-to-cart/', views.AddToCart, name="add-to-cart"),
    path('delete-cart-item/<int:pk>/<int:qty>/<int:product_id>', views.DeleteCartItem, name="delete-cart-item"),
    path('add-sale/', views.AddSale, name="add-sale")

]
