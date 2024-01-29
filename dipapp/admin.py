from django.contrib import admin
from dipapp.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, WishList, Address

from
# Register your models here.


import admin_thumbnails
# Register your models here.

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of empty forms to display for adding new images

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'modified_date', 'category', 'is_available')
    prepopulated_fields  = {'slug': ('product_name',)}
    inlines = [ProductImageInline]
    
admin.site.register(Product, ProductAdmin)
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity')




admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)