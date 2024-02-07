from django.urls import path
from . import views 


urlpatterns = [
    path('', views.home, name="home"),
    path('shop/products', views.shop, name="shop"),
    path('category/', views.category_list_view, name="category-list"),
    path('category/<cid>/', views.category_product_list_view, name="category-product-list"),
]