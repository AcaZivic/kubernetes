
from django.urls import path

from . import views

urlpatterns = [

    path('', views.home, name=""),

    path('register', views.register, name="register"),

    path('my-login', views.my_login, name="my-login"),

    path('user-logout', views.user_logout, name="user-logout"),

    # CRUD

    path('dashboard', views.dashboard, name="dashboard"),

    path('create-customer', views.create_customer, name="create-customer"),

    path('update-customer/<int:pk>', views.update_customer, name='update-customer'),

    path('customer/<int:pk>', views.singular_customer, name="customer"),

    path('delete-customer/<int:pk>', views.delete_customer, name="delete-customer"),

    

]






