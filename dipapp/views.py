from django.shortcuts import render
from .models import Product

def home(request):
    # Get the first four products with their images
    top_four_products = Product.objects.prefetch_related('images').all()[:4]
    return render(request, 'dipapp/home.html', {'top_four_products': top_four_products})