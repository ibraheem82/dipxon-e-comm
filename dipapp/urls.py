from django.urls import path
from . import views 
from .views import ProductDetailView, ProductsByCategoryView, add_to_cart
    
    
urlpatterns = [
    path('', views.home, name="home"),
    path('shop/', views.shop, name="shop"),
    path('products_by_category/<uuid:category_id>/', ProductsByCategoryView.as_view(), name='products_by_category'),
    path('product/<uuid:product_id>/', ProductDetailView.as_view(), name='product_details'),
    path('products/<uuid:product_id>/add-to-cart/', add_to_cart, name='add_to_cart'),
]