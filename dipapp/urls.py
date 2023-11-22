from django.urls import path
from . import views 
    
    
urlpatterns = [
    path('', views.home, name="home"),
    path('products/<int:product_id>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
]