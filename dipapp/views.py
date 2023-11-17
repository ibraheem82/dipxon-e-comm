from django.shortcuts import render
from .models import Product, Category
from .utils import get_user_country, get_currency_symbol

def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    gender_choices = Product.PRODUCT_CATEGORY_GENDER
    user_country = get_user_country(request)
    
    # Create the context dictionary
    context = {
        'products': products,
        'categories': categories,
        'gender_choices' : gender_choices,
        'user_country': user_country,
        'get_currency_symbol' : get_currency_symbol,
    }

    # Render the template with the context data
    return render(request, 'dipapp/home.html', context)