import logging
from django.shortcuts import render
from .models import Product, Category, ProductGallery
from .utils import get_user_country, get_currency_symbol



from django.shortcuts import get_object_or_404, redirect, render 
from .models import Cart, CartItem, Product
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def home(request):
    products = Product.objects.all()[:5]
    categories = Category.objects.all()
    user_country = get_user_country(request)
    
    # Create the context dictionary
    context = {
        'products': products,
        'categories': categories,
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

logger = logging.getLogger(__name__)
@login_required  # Ensure the user is logged in to access this view
def get_cart_count(request):
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.cartitem_set.all()

            total_items = cart.get_total_items  # No parentheses
            grand_total = cart.get_grandtotal()

            cart_details = {
                'success': True,
                'total_items': total_items,
                'grand_total': grand_total,
                'cart_items': [
                    {
                        'product_name': item.product.product_name,
                        'quantity': item.quantity,
                        'total_price': item.get_total_price(),
                    }
                    for item in cart_items
                ],
            }

            return JsonResponse(cart_details)
        else:
            return JsonResponse({'success': False, 'error': 'User is not authenticated'})
    except Exception as e:
        logger.error(f"Error in get_cart_count view: {e}")
        return JsonResponse({'success': False, 'error': f'Internal server error: {str(e)}'})






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


def product_detail(request, slug):
    single_product = get_object_or_404(Product, slug=slug)
    title = f"{single_product.product_name} - Single Product Detail"
    # Fetch the product gallery for the current product
    product_gallery = ProductGallery.objects.filter(product=single_product)
    return render(request, 'dipapp/product_detail.html', {'single_product': single_product, 'title': title, 'product_gallery': product_gallery})

def shop(request):
    products = Product.objects.all()
    context = {
        'products': products
    }

    return render(request, 'dipapp/shop.html', context)