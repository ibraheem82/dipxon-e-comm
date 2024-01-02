from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .forms import RegistrationForm
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
# ========> Login View <========
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
import logging
from .models import Account
from django.contrib.sites.shortcuts import get_current_site
from django import forms

# Create a logger instance
logger = logging.getLogger(__name__)

def loginUser(request):
    page = 'login'

    # ========> Login View <========
    if request.method == 'POST':
        # ===> from the login form, the name values.
        email = request.POST['email']
        password = request.POST['password']
        
        # * ===> will set the user so they can login
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
                # The user is valid, log them in.
                auth.login(request, user)
                messages.success(request, 'You are now logged in')
                return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    context = {'page': page}
    return render(request, 'accounts/login_register.html', context)


# def loginUser(request):
#     page = 'login'

#     if request.method == 'POST':
#         email = request.POST['email'].lower()
#         password = request.POST['password']
        
#         user = authenticate(request, email=email, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('shop')
#         else:
#             messages.info(request, 'Email OR password is incorrect')

#     return render(request, 'accounts/login_register.html', {'page': page})







# ========> Register View <========
def registerUser(request):
    page = 'register'
    form  = RegistrationForm()
    
    if request.method == 'POST':
        form  = RegistrationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password != confirm_password:
                form.add_error('confirm_password', "Passwords do not match!")
            
            try:
                user = Account.objects.create_user(
                    **form.cleaned_data, 
                    username=form.cleaned_data['email'].split("@")[0]
                    )
                user.phone_number = form.cleaned_data['phone_number']
                user.save()
                current_site = get_current_site(request)
                
                mail_subject = 'Please activate your account'

                message = render_to_string('accounts/account_verification_email.html', {
                    'user' : user,
                    'domain' : current_site,
                    'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                    'token' : default_token_generator.make_token(user),
                })
                
                to_email = user.email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                messages.info(request, 'Thank you for registering! Please check your email to activate your account.')
                send_email.send()
            

                return redirect('/accounts/login/?command=verification&email=' + user.email)
            except Exception as e:
                messages.error(request, f"An error occurred during registration: {e}")
                return redirect('register')
    print(form.errors)

    context = {'page' : page, 'form' : form}
    return render(request, 'accounts/login_register.html', context)



# ========> Activate View <========
def activate(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        
        user = Account._default_manager.get(id=uid)
        

    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user  = None
        
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        
        messages.success(request, 'Congratulations! your account is activated.')
        return redirect('login')

    else:
        messages.error(request,'Invalid activation link OR the link has expired.')
        return redirect('register')


# ========> Logout <========
def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out.')
    return redirect('login')
