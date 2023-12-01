from django.urls import path
from . import views 
    
    
urlpatterns = [
    path('', views.home, name="home"),
    path('shop/', views.shop, name="shop"),
    path('products/<int:product_id>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('get_cart_count/', views.get_cart_count, name='get_cart_count'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]