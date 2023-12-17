from django.db import models

# Create your models here.
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Account(models.Model):
    user                =  models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name          = models.CharField(max_length=50)
    last_name           = models.CharField(max_length=50)
    username            = models.CharField(max_length=50, unique=True)
    email               = models.EmailField(max_length = 100, unique=True)
    phone_number        = models.CharField(max_length=50)
    
    date_joined         = models.DateTimeField(auto_now_add=True)
    last_login          = models.DateTimeField(auto_now_add=True)
    id                  =  models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    
    
class UserProfile(models.Model):
    user           = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank = True, max_length = 100)
    address_line_2 = models.CharField(blank = True, max_length = 100)
    city           = models.CharField(blank=True, max_length=20)
    state          = models.CharField(blank=True, max_length=20)
    country        = models.CharField(blank=True, max_length=20)
    id             =  models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return self.user.first_name