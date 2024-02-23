from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from dipapp.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, WishList, Address
from .utils import get_user_country, get_currency_symbol
from django.views import View
from django.db.models import Count, Avg
from dipapp.forms import ProductReviewForm
# from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth.decorators import login_required
from taggit.models import Tag

def home(request):
    products = Product.objects.filter(product_status ="published", featured = True)
    categories = Category.objects.all()[:4]
    # count_category_products = Category.objects.annotate(product_count=Count('product'))
    user_country = get_user_country(request)
    currency_symbol = get_currency_symbol(user_country)
    print(user_country)
    
    # Create the context dictionary
    context = {
        'products': products,
        'categories': categories,
        # 'count_category_products':count_category_products
        'user_country': user_country,
        'currency_symbol' : currency_symbol
    }

    # Render the template with the context data
    return render(request, 'dipapp/home.html', context)


def category_list_view(request):
    categories = Category.objects.all()

    context = {
        'categories': categories,
    }

    return render(request, 'dipapp/category-list.html', context)




def shop(request):
    products = Product.objects.filter(product_status ="published")
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
    }

    return render(request, 'dipapp/shop.html', context)


def category_product_list_view(request, cid):
#     products = Product.objects.filter(product_status ="published", category = category) retrieves a collection of product objects that meet two conditions:
# product_status ="published": Filters for products marked as "published."
# category = category: Filters for products belonging to the retrieved category.
    category = Category.objects.get(cid = cid)
    products = Product.objects.filter(product_status ="published", category = category)
    
    context = {
        
        'category': category,
        'products': products,
    }

    return render(request, 'dipapp/category-product-list.html', context)






def product_detail_view(request, pid):
    product = Product.objects.get(pid = pid)
    # product = get_object_or_404(Product, id = pid)
    products = Product.objects.filter(category = product.category).exclude(pid = pid) # filtering by the category in the Product model, if the category = the product that we are currently viewing, meaning that filtering by the category of that product. that is show all the products that have the same categories, and also exclude what so ever product that you are currently viewing or that you are on.
    
    # getting all reviews that is related to the product that we are currently viewing.
    reviews  = ProductReview.objects.filter(product = product).order_by("-date")
    
    # filter all the images that is related to the product that you are getting it details, it will get all it corresponding images.
    p_image = product.p_images.all()
    
    # Getting average review of the product, checking average on the rating field.
    average_rating = ProductReview.objects.filter(product = product).aggregate(rating = Avg('rating'))

    review_form = ProductReviewForm()
    context = {
        'p': product,
        'p_image': p_image,
        'review_form': review_form,
        'average_rating': average_rating,
        'reviews' : reviews,
        'products': products
    }

    return render(request, 'dipapp/product_detail.html', context)


def tag_list(request, tag_slug = None):
    products = Product.objects.filter(product_status ="published").order_by("-id")
    tag = None # initially is should have nothing in it.
    if tag_slug:
        tag = get_object_or_404(Tag, slug =  tag_slug) # the second argument (slug) is in the Tag model that we installed from pip, and we are saying slug = whatsoever slug that we will be passing in.
        # when ever the is a slug we want to get all the products that is related to that slug.
        products = products.filter(tags__in=[tag]) # [tags__in] , take note that the product model has a field called tag, checking if we have this (tags__in) in what so ever product that we are filtering. 
    context = {
        "products":products,
        'tag': tag
    }
    return render(request, 'dipapp/tag.html', context)



def ajax_add_review(request, pid):
    product = Product.objects.get(pk  = pid)
    user = request.user
    # we want to create new review with whatsoever the user pass in the review form.
    # [user] field in the [ProductReview] model
    review   = ProductReview.objects.create(
        user = user,
        product = product,
        # getting the review that the user is passing in.
        review = request.POST['review'],
        rating = request.POST['rating']
    )
    
    context = {
        'user':user.username,
        'review': request.POST['review'],
        'rating' : request.POST['rating']
    }
    # getting the average reviews
    average_reviews = ProductReview.objects.filter(product = product).aggregate(rating = Avg("rating"))
    
    return JsonResponse(
        {
            'bool':True,
            'context': context,
            'average_reviews': average_reviews
        }
    )
