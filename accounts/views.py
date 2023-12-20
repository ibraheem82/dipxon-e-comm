from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
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

# Create a logger instance
logger = logging.getLogger(__name__)

def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('shop')

    if request.method == 'POST':
        email = request.POST['email'].lower()
        password = request.POST['password']

        try:
            
            user = User.objects.get(email = email)
        except User.DoesNotExist:
            messages.error(request, 'Email does not exist')
            return redirect('login')

        # * Checking if the user account is active
        if user.is_active:
            # * Then authenticate the user through the email and password
            user = authenticate(request, email = email, password = password)

            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next', 'home'))
                # return redirect(request.GET['next'] if 'next' in request.GET else 'home')
            else:
                messages.error(request, 'Username OR Password is incorrect')
        else:
            messages.error(request, 'User account is not active')

    context = {'page': page}
    return render(request, 'accounts/login_register.html', context)







# ========> Register View <========
def registerUser(request):
    page = 'register'
    form  = RegistrationForm()
    
    if request.method == 'POST':
        form  = RegistrationForm(request.POST)
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
            
            current_site = get_current_site(request)
            
            mail_subject = 'Please activate your account'

            message = render_to_string('accounts/account_verification_email.html', {
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            
            to_email = email
            # ===> 
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return redirect('/accounts/login/?command=verification=' + email)

        else:
            form = RegistrationForm()

    context = {'page' : page, 'form' : form}
    return render(request, 'accounts/login_register.html', context)



# ========> Logout <========
def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out.')
    return redirect('login')
