from django.contrib import admin
from dipapp.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, WishList, Address

# from
# Register your models here.


# import admin_thumbnails.

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
    extra = 1  # Number of empty forms to display for adding new images

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user','title', 'product_image', 'price', 'category', 'vendor',  'featured','product_status','pid']

#     
    
# admin.site.register(Product, ProductAdmin)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']


class VendorAdmin(admin.ModelAdmin):
    list_display = ['title', 'vendor_image']
    
    
    
class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'price', 'paid_status', 'order_date', 'product_status']
    
    
    
class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'image', 'qty', 'price', 'total']
    
    
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']
    
    
    
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']
    
    
    
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'status']




admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(WishList, WishlistAdmin)
admin.site.register(Address, AddressAdmin)