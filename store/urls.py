from django.urls import path
from . import views
app_name= 'store'
urlpatterns = [
    path('', views.Dashboard, name="dashboard"),
    path('login/', views.Login, name="login")
]
