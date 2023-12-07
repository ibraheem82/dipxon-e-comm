from django.shortcuts import render

# Create your views here.
# from django.shortcuts import render, redirect, get_object_or_404

# from .forms import 
# from .models import Account




import requests

# ========> Register View <========
# def register(request):
#     page = 'register'
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
            

#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             phone_number = form.cleaned_data['phone_number']
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             username = email.split("@")[0]
            

#             user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
#             user.phone_number = phone_number
#             user.save()
            
#             # ========> User activation <========
#             current_site = get_current_site(request)
        
#             mail_subject = 'Please activate your account'
            
#             message = render_to_string('accounts/account_verification_email.html', {
             
#                 'user' : user,
#                 'domain' : current_site,
               
#                 'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token' : default_token_generator.make_token(user),
#             })
#             to_email = email
#             send_email = EmailMessage(mail_subject, message, to=[to_email])
#             send_email.send()
#             login_url = reverse('login') 
#             return redirect(f'{login_url}?command=verification={email}')
#     else:
#         # f'{login_url}?command=verification={email}'
#         form = RegistrationForm()
#     context = {
#         'form' : form,
#         'page': page
#     }
#     return render(request, 'accounts/login_register.html', context)



# ========> Activate View <========



# def login_view(request):
#     page = 'login'
#     login_form = LoginForm(request.POST or None)

#     if request.method == "POST":
#         if login_form.is_valid():
#             user = login_form.get_user()

#             # Check for "Remember Me" checkbox
#             if request.POST.get('rememberMe'):
#                 set_remember_me_cookie(request, user)

#             login(request, user)
#             return redirect('home')

#     context = {
#         'login_form': login_form,
#         'page': page
#     }

#     return render(request, 'accounts/login_register.html', context)
