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



# from carts.views import _cart_id
# from carts.models import Cart, CartItem



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
            return redirect('/accounts/login/?command=verification=' + email)
    else:
        form = RegistrationForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/login_register.html', context)