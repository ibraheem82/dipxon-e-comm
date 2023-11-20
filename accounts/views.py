from django.shortcuts import render

# Create your views here.

from email.message import EmailMessage
from multiprocessing import context
from re import U
from unicodedata import is_normalized
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegistrationForm, UserForm, UserProfileForm 
from .models import Account, UserProfile
# from orders.models import Order, OrderProduct
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import HttpResponse




# ========> Importing for email verification   <======== 
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


from django.core.mail import send_mail
from django.conf import settings



from carts.views import _cart_id
from carts.models import Cart, CartItem



import requests

# ========> Register View <========
def register(request):
    page = 'register'
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            
            # ========> User activation <========
            current_site = get_current_site(request)
        
            mail_subject = 'Please activate your account'
            
            message = render_to_string('accounts/account_verification_email.html', {
             
                'user' : user,
                'domain' : current_site,
               
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            return redirect('/accounts/login_register/?command=verification=' + email)
    else:
        form = RegistrationForm()
    context = {
        'form' : form,
        'page': page
    }
    return render(request, 'accounts/login_register.html', context)







# ========> Login View <========
def loginUser(request):
    if request.method == 'POST':
        # ===> from the login form, the name values.
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            try:
                
                cart = Cart.objects.get(cart_id= _cart_id(request))
                
                is_cart_item_exists = CartItem.objects.filter(cart = cart).exists()
                if is_cart_item_exists:
                    
                    cart_item = CartItem.objects.filter(cart=cart)
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                     
                        product_variation.append(list(variation))
                    
                    
                    #
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id  = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                        
                        
                       
                        
                        
                        
                        
                
                    for pr in product_variation:
                        if pr in ex_var_list:
                            
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                            
                        else:
                            cart_item = CartItem.objects.filter(cart = cart)
                            for item in cart_item:
                                # ===> this is assigning the user to the cartitem
                                item.user = user
                                item.save()  
            except:
                pass  
            auth.login(request, user)
            messages.success(request, 'Your are now loggged in')
            # ===> THIS ['request.META.get('HTTP_REFERER')']  will grab the previous url from where you came,  you are coming from
            # ===> it wil store the url inside the ['url'] variable.
            url = request.META.get('HTTP_REFERER')
            try:
                # ['requests'] --> which is the request libery
                query = requests.utils.urlparse(url).query
                # ===> next=/cart/checkout/
                # ===> the ['x.split'] is spliting the ['='] sign 
                # ===> ['next'] is the key and ['cart/checkout'] as the value.
                params  = dict(x.split('=') for x in query.split('&'))
                # ===> we want to redirect the user to the value of the ['next']
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')



# ========> Activate View <========
def activate(request, uidb64, token):
    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        
        
        user = Account._default_manager.get(id=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user  = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()  # * Save the user after updating is_active
        
        messages.success(request, 'Congratulations! your account is activated.')
        return redirect('login')

    else:
        messages.error(request,'Invalid activation link.')
        return redirect('register')