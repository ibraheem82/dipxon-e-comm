from django.shortcuts import render
from .models import Product

def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {'products': products, 'categories': categories}
    return render(request, 'dipapp/home.html', context)