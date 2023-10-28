from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# * Creation of user instance
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        # ===> raise error if not email address
        if not email:
            raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError('User must have a username')
        
        
        # * Creation of user instance  using the user model associated with the manager 
        user = self.model(
             # what the 'normalize_email' does is that if you enter a capital letter inside your email it will change it so small letter everything will be normalized
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        
        
         # ===> the 'set_password' is use for setting the password
        user.set_password(password)
        user.save(using=self._db)
        # Create a UserProfile for the superuser
        UserProfile.objects.create(user=user)
        return user
    
     # ===> creating the superUser
     # ------- Creating the SuperUser --------
    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
     # ===> giving the permisson
     # ===> set it to true
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        # * Create a UserProfile for the user
        UserProfile.objects.create(user=user)
        return user