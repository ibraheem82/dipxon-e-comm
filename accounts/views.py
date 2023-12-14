from django.shortcuts import render

# Create your views here.
# from django.shortcuts import render, redirect, get_object_or_404

# from .forms import 
# from .models import Account




import requests

# ========> Register View <========




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
