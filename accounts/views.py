from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from accounts.forms import UserRegistrationForm
from django.contrib import messages
from django.conf import settings
from accounts.models import User
# # Create your views here.





def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        messages.warning(request, 'Hey, you are already logged in.')
        return redirect('home')
     
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
     
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Welcome 🤝.')
                return redirect('home')
            else:
                messages.warning(request, 'User does not exist, create an account.')
        except User.DoesNotExist:
            messages.warning(request, f'User with {email} does not exist')
     
    return render(request, 'accounts/login_register.html', {'page': page})







# # ========> Register View <========
def registerUser(request):
    page = 'register'
    form  = UserRegistrationForm()
    
    if request.method == 'POST':
        form  = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hi {username}, your account was created successfully.")
            new_user = authenticate(
                username = form.cleaned_data["email"],
                password = form.cleaned_data["password1"])

            # Log in the new user that just registered
            login(request, new_user)
            print(new_user)
            return redirect('home')
    else:
        form = UserRegistrationForm()

    context = {'page' : page,
               'form' : form}
    return render(request, 'accounts/login_register.html', context)


# # ========> Logout <========
def logoutUser(request):
    logout(request)
    messages.success(request, 'User was logged out.')
    return redirect('login')
