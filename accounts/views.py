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
        email = request.POST['email'].lower()
        password = request.POST['password']

        try:
            # ! import the [User] model when using this.
            user = User.objects.get(email = email)
        except :
            messages.error(request, 'Email does not exist')

        user = authenticate(request, email = email, password = password)

        if user is not None:
            # ! [ login() ] is going to create a [sessions] for the user, in the database inside the [sessions] table, then it is going to get that [sessions] and add it to our browsers [cookies]
            login(request, user)
            # will send the user to the next route.
            # * the next route will be what we have passed in the url.
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Username OR Password is incorrect')

    context = {'page': page}
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
            user.save()
            messages.success(request, 'User account was created!')
            
            
            
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
