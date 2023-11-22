from django.urls import path
from . import views 
    
    
urlpatterns = [
    path('', views.home, name="home")
    path('<int:product_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
]