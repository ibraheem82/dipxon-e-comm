from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from accounts.forms import UserRegistrationForm
from django.contrib import messages
from django.conf import settings
# # Create your views here.


# (AUTH_USER_MODEL) that was defined in the settings.py file.
User = settings.AUTH_USER_MODEL




def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        messages.warning(request, f'Hey you are already logged in.')
        return redirect('home')
        
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            # compare the email in model with the email that is been passed in from the frontend, NOTE[!] -> first email will get if is the email is in the database or not.
            user = User.objects.get(email=email)
        except:
            messages.warning(request, f'User with {email} does not exist')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'You are logged in.')
            return redirect('home')
        else:
            messages.warning(request, f'User does not Exist, create an account.')

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



# # ========> Activate View <========
# def activate(request, uidb64, token):

#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
        
#         user = Account._default_manager.get(id=uid)
        

#     except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
#         user  = None
        
    
#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
        
#         messages.success(request, 'Congratulations! your account is activated.')
#         return redirect('login')

#     else:
#         messages.error(request,'Invalid activation link OR the link has expired.')
#         return redirect('register')


# # ========> Logout <========
# def logoutUser(request):
#     logout(request)
#     messages.info(request, 'User was logged out.')
#     return redirect('login')
