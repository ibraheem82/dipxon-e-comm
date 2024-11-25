from dipapp.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, WishList, Address



def default(request):
    categories = Category.objects.all()
    address = None  # Initialize address with None  
    if request.user.is_authenticated:
        try:
            address = Address.objects.get(user=request.user) 
        except Address.DoesNotExist:
            pass
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            try:
                price = float(item['price']) if item['price'] else 0.0
                qty = int(item['qty']) if item['qty'] else 0 
                cart_total_amount += qty * price
            except (ValueError, TypeError) as e:
                # Log the error or handle it as needed
                print(f"Error processing item {item}: {e}")
                continue
            
    return {
        'categories': categories,
        'address': address,
        "cart_data": request.session['cart_data_obj'],
        'totalcartitems': len(request.session['cart_data_obj']),
        'cart_total_amount' : cart_total_amount
    }

     