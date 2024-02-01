# from django.contrib.sessions.models import Session
from django.shortcuts import render
from dipapp.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, WishList, Address
# from .utils import get_user_country, get_currency_symbol
from django.views import View



# from django.shortcuts import get_object_or_404, redirect, render 
from django.db.models import Count
# from django.http import JsonResponse
# from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth.decorators import login_required

# from django.core.exceptions import ObjectDoesNotExist
# from .utils import validate_quantity
# from django.http import Http404

def home(request):
    products = Product.objects.filter(product_status ="published", featured = True)
    categories = Category.objects.all()[:4]
    # count_category_products = Category.objects.annotate(product_count=Count('product'))
    # user_country = get_user_country(request)
    
    # Create the context dictionary
    context = {
        'products': products,
        'categories': categories,
        # 'count_category_products':count_category_products
        # 'user_country': user_country,
        # 'get_currency_symbol' : get_currency_symbol,
    }

    # Render the template with the context data
    return render(request, 'dipapp/home.html', context)







def shop(request):
    products = Product.objects.filter(product_status ="published")
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
    }

    return render(request, 'dipapp/shop.html', context)


def category_product_list_view(request, cid):
#     products = Product.objects.filter(product_status ="published", category = category) retrieves a collection of product objects that meet two conditions:
# product_status ="published": Filters for products marked as "published."
# category = category: Filters for products belonging to the retrieved category.
    category = Category.objects.get(cid = cid)
    products = Product.objects.filter(product_status ="published", category = category)
    
    context = {
        
        'category': category,
        'products': products,
    }

    return render(request, 'dipapp/category-product-list.html', context)

    