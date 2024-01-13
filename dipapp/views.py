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
# -------
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        
        # Retrieve or create cart based on session cart_id:
        cart, cart_created = Cart.objects.get_or_create(cart_id=_cart_id(request))
        
        # Get or create cart item
        cart_item, cart_item_created = CartItem.objects.get_or_create(cart=cart, product=product)

        # Get desired quantity from form
        quantity = int(request.POST.get('quantity', 1))

        # Get desired quantity and validate
        error_message = validate_quantity(product, quantity)
        if error_message:
            return JsonResponse({'success': False, 'message': error_message})


       # Update cart item quantity
        cart_item.quantity += quantity
        cart_item.save()
        
        # If the user is not authenticated, update the session-based cart
        if not request.user.is_authenticated:
            cart.cart[str(product_id)] = {'quantity': cart_item.quantity}
            request.session['cart'] = cart.cart

        # Prepare successful response data
        data = {
            'success': True,
            'message': f"{quantity} {product.product_name}(s) added to your cart.",
            'cart_quantity': cart_item.quantity,  # Include updated cart quantity for the product
        }

        return JsonResponse(data, safe=True)

    except ObjectDoesNotExist:
        return JsonResponse({
            'success': False,
            'message': "Product not found."
        })

    except ValueError as ve:
        return JsonResponse({
            'success': False,
            'message': f"Invalid quantity entered: {ve}"
        })




def shop(request):
    products = Product.objects.all()
    context = {
        'products': products
    }

    return render(request, 'dipapp/shop.html', context)