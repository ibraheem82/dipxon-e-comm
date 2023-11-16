from django.shortcuts import render
from .models import Product, Category


from django import template

def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # Calculate the displayed subcategories
    displayed_subcategories = [item[0] for category in categories for item in category.SUBCATEGORY_CHOICES]

    # Create the context dictionary
    context = {
        'products': products,
        'categories': categories,
        'displayed_subcategories': displayed_subcategories,
    }

    # Render the template with the context data
    return render(request, 'dipapp/home.html', context)