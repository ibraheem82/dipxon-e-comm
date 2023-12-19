from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import RegistrationForm, CustomLoginForm
from django.core.exceptions import ValidationError
# ========> Login View <========
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('shop')

    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Authenticate without passing a username
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect(request.GET.get('next', 'shop'))
            else:
                messages.error(request, 'Email or Password is incorrect')
        else:
            # Form is not valid, display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

    else:
        form = CustomLoginForm()

    context = {'page': page, 'login_form': form}
    return render(request, 'accounts/login_register.html', context)







# ========> Register View <========
def registerUser(request):
    page = 'register'
    form  = RegistrationForm()
    
    if request.method == 'POST':
        form  = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # ! convert the [username] to lowercase.
            user.email = user.email.lower()
            messages.success(request, 'User account was created!')
            user.save()
            
            
            login(request, user)
            
            
            # return redirect('profiles')

            # * When the user create thier account they should be redirected to the shop.
            return redirect('shop')


        else:
            messages.error(request, 'An error has occured during registration')
    context = {'page' : page, 'form' : form}
    return render(request, 'accounts/login_register.html', context)



# ========> Logout <========
def logoutUser(request):
# ! [logout]it is going to take in the request and the simply delete the [sessionID]
    # ! logout(request) it is going to delete that session
    logout(request)
    messages.info(request, 'User was logged out.')
    return redirect('login')
