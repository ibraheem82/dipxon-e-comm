from django.contrib import admin
from .models import Product, ProductImage, Cart, CartItem, ProductGallery
# Register your models here.


import admin_thumbnails
# Register your models here.


@admin_thumbnails.thumbnail('images')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    # [extra] means That when ever you want to add more fields just click on add more button add more images.
    extra = 1
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of empty forms to display for adding new images

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'modified_date', 'category', 'is_available')
    prepopulated_fields  = {'slug': ('product_name',)}
    inlines = [ProductImageInline]
    
admin.site.register(Product, ProductAdmin)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity')




admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(ProductGallery)