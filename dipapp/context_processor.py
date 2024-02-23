from dipapp.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, WishList, Address



def default(request):
    categories = Category.objects.all()
    address = None  # Initialize address with None  
    if request.user.is_authenticated:
        try:
            address = Address.objects.get(user=request.user) 
        except Address.DoesNotExist:
            pass
    
    return  {
        'categories': categories,
        'address': address,
    }

     