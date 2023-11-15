from django.shortcuts import render
from .models import Product, Category


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # Create a set to track displayed subcategories
    displayed_subcategories = set()

    # Iterate through categories and subcategories to populate the set
    for category in categories:
        for subcategory, _ in category.SUBCATEGORY_CHOICES:
            displayed_subcategories.add(subcategory)

    context = {
        'products': products,
        'categories': categories,
        'displayed_subcategories': displayed_subcategories,
    }

    return render(request, 'dipapp/home.html', context)