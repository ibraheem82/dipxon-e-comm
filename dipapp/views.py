from django.shortcuts import render
from .models import Product

# Create your views here.
def home(request):
    return render(request, 'dipapp/home.html')