from django.urls import path
from . import views 
from .views import ProductDetailView, ProductsByCategoryView
    
    
urlpatterns = [
    path('', views.home, name="home"),
    path('shop/', views.shop, name="shop"),
    path('products/<int:product_id>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('get_cart_count/', views.get_cart_count, name='get_cart_count'),
    path('category/<uuid:category_id>/', ProductsByCategoryView.as_view(), name='products_by_category'),
    path('product/<uuid:product_id>/', ProductDetailView.as_view(), name='product_details'),
]