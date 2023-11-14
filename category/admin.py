from django.contrib import admin

# Register your models here.
from .models import Category
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('slug',) 
    # list_display = ('category', 'slug') 
    
    
admin.site.register(Category, CategoryAdmin)
