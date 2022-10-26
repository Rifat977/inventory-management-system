from django.urls import path
from . import views
app_name= 'store'
urlpatterns = [
    path('', views.Dashboard, name="dashboard"),

    path('login/', views.Login, name="login"),
    path('logout/', views.Logout, name="logout"),

    path('profile/', views.Profile, name="profile"),
    path('change_password/', views.ChangePassword, name="change_password"),

    path('supplier/', views.SupplierView, name="supplier")
]
