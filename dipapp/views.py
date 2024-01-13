from django.contrib.sessions.models import Session
from django.shortcuts import render
from .models import Product, Category
from .utils import get_user_country, get_currency_symbol
from django.views import View



from django.shortcuts import get_object_or_404, redirect, render 
from .models import Cart, CartItem, Product
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist
from .utils import validate_quantity
from django.http import Http404

def home(request):
    products = Product.objects.all()[:5]
    categories = Category.objects.all()[:4]
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


class ProductDetailView(View):
    template_name = 'dipapp/product_detail.html'

    def get(self, request, product_id):
        product = get_object_or_404(Product, product_id=product_id)

        # Check if product is in cart
        cart, cart_created = Cart.objects.get_or_create(cart_id=request.session.session_key)
        cart_items = cart.cartitem_set.all()
        isInCart = cart_items.filter(product=product).exists()

        return render(request, self.template_name, {
            'product': product,
            'isInCart': isInCart,
        })

    
    
class ProductsByCategoryView(View):
    template_name = 'dipapp/products_by_category.html'

    def get(self, request, category_id):
        category = Category.objects.get(unique_id=category_id)
        products = Product.objects.filter(category=category)
        return render(request, self.template_name, {'category': category, 'products': products})

def add_to_cart(request, product_id):
    try:
        product = get_object_or_404(Product, pk=product_id)
        cart, cart_created = Cart.objects.get_or_create(cart_id=request.session.session_key)

        # Retrieve existing cart item or create a new one
        cart_item, cart_item_created = cart.cartitem_set.get_or_create(product=product, defaults={'quantity': 0})  # Set default quantity to 0

        quantity = int(request.POST.get('quantity', 1))
        error_message = validate_quantity(product, quantity)
        if error_message:
            return JsonResponse({'success': False, 'message': error_message})

        # Update quantity of existing item instead of creating a new one
        cart_item.quantity += quantity
        cart_item.save()

        # Save cart to recalculate grandtotal
        cart.save()

        data = {
            'success': True,
            'message': f"{product.product_name} added to your cart.",
            'cart_quantity': cart_item.quantity,
            'cart_items': [{
                'product_name': item.product.product_name,
                'quantity': item.quantity,
                'price': item.product.price,
                'image_url': item.product.product_images.first().image.url,
                'product_url': item.product.get_url(),
            } for item in cart.cartitem_set.all()],
            'cart_subtotal': cart.grandtotal,
        }
        return JsonResponse(data, safe=True)

    except Http404:
        return JsonResponse({'success': False, 'message': "Product not found."})

    except ValueError as ve:
        return JsonResponse({'success': False, 'message': f"Invalid quantity entered: {ve}"})





def shop(request):
    products = Product.objects.all()
    context = {
        'products': products
    }

    return render(request, 'dipapp/shop.html', context)