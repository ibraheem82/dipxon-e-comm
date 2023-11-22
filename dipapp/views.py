from django.shortcuts import render
from .models import Product, Category
from .utils import get_user_country, get_currency_symbol



from django.shortcuts import get_object_or_404, redirect, render 
from .models import Cart, CartItem, Product
from django.http import JsonResponse


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





def add_to_cart(request, product_id):
   product = get_object_or_404(Product, pk=product_id)
   cart, created = Cart.objects.get_or_create(user=request.user)
   cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

   if not created:
       cart_item.quantity += 1
       cart_item.save()
       message = f"Quantity of {product.product_name} increased in your cart."
   else:
       message = f"{product.product_name} added to your cart."

   # Create a response to send to the client
   response = {
       "success": True,
       "product_name": product.product_name,
       "message": message,
   }
   return JsonResponse(response)




def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id) 
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=cart, product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


def cart(request):
    cart = Cart.objects.get(user=request.user)
    context = {
        'cart': cart
    }
    return render(request, 'cart.html', context)