from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('home/', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('add-to-cart-by-gram/<int:food_id>/', views.add_to_cart, name='add_to_cart_by_gram'),
]
