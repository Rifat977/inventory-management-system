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
    path('sale/', views.AddSaleView, name="sale"),
    path('add-to-cart/', views.AddToCart, name="add-to-cart"),
    path('delete-cart-item/<int:pk>/', views.DeleteCartItem, name="delete-cart-item")

]
