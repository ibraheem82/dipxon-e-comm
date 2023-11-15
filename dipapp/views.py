from django.shortcuts import render
from .models import Product, Category


from django import template

register = template.Library()

@register.filter(name='remove_from_list')
def remove_from_list(value, arg):
    return [item for item in value if item != arg]

def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    displayed_subcategories = [item[0] for category in categories for item in category.SUBCATEGORY_CHOICES]
    context = {'products': products, 'categories': categories, 'displayed_subcategories': displayed_subcategories}
    return render(request, 'dipapp/home.html', context)

