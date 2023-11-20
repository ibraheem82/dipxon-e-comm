from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name="login"),
    # path('logout/', views.logoutUser, name="logout"),
    path('register/', views.register, name='register'),
    path("activate/<uidb64>/<token>/", views.activate, name='activate'),
]