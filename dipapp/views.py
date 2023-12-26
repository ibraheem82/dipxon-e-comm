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
        return render(request, self.template_name, {'product': product})
    
    
class ProductsByCategoryView(View):
    template_name = 'dipapp/products_by_category.html'

    def get(self, request, category_id):
        category = Category.objects.get(unique_id=category_id)
        products = Product.objects.filter(category=category)
        return render(request, self.template_name, {'category': category, 'products': products})
# -------
def _cart_id(request):
    # ===> we are creating a new session
    cart = request.session.session_key
    if not cart:
    # ===> if there is no session, a new seesion will be created
        cart = request.session.create()
    # ===> this will return the cart id
    return cart


def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        
        # Retrieve or create cart based on session cart_id:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart_id = _cart_id(request)
        cart = Cart.objects.create(cart_id=cart_id)


         # Check for authenticated user and retrieve relevant cart
        if request.user.is_authenticated:
            cart.user = request.user  # Associate cart with authenticated user
            cart.save()
            cart_item, cart_item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        else:
           cart_item_data = cart.cart.get(str(product_id), {'quantity': 0})
           cart_item_data['quantity'] += 1
           cart.cart[str(product_id)] = cart_item_data
           request.session['cart'] = cart.cart
           return JsonResponse({'success': True, 'message': f"{product.product_name} added to your cart."})

        # Get desired quantity from form
        quantity = int(request.POST.get('quantity', 1))

        # Get desired quantity and validate
        error_message = validate_quantity(product, quantity)
        if error_message:
            return JsonResponse({'success': False, 'message': error_message})


       # Update cart item quantity
        cart_item.quantity += quantity
        cart_item.save()

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