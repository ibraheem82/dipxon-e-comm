from django.shortcuts import render
from .models import Product

def home(request):
    # Get the first four products with their images
    top_three_products = Product.objects.prefetch_related('images').all()[:4]
    return render(request, 'dipapp/home.html', {'top_three_products': top_three_products})