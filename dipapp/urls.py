from django.urls import path
from . import views 


urlpatterns = [
    path('', views.home, name="home"),
    path('shop/products', views.shop, name="shop"),
    path('product/<pid>', views.product_detail_view, name="product_detail"),
    path('category/', views.category_list_view, name="category-list"),
    path('category/<cid>/', views.category_product_list_view, name="category-product-list"),
    
    # Tags
    path('products/tag/<slug:tag_slug/>', views.tag_list, name="tags"),
]