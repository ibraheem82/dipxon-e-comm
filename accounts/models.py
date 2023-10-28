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
    
    # * creating a custom user model..
class Account(AbstractBaseUser):
    first_name          = models.CharField(max_length=50)
    last_name           = models.CharField(max_length=50)
    username            = models.CharField(max_length=50, unique=True)
    email               = models.EmailField(max_length = 100, unique=True)
    phone_number        = models.CharField(max_length=50)
    
#     # ===> these fields are madantory when creating custom user model
#     # ===> Required
    date_joined         = models.DateTimeField(auto_now_add=True)
    last_login          = models.DateTimeField(auto_now_add=True)
    is_admin            = models.BooleanField(default=False)
    is_staff            = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=False)
    is_superadmin       = models.BooleanField(default=False)
    
    
    # * You need an email to be able to login to the admin panel.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    # * it a class.
    objects = MyAccountManager()
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
#     # when we return an account object in the template we should return an email
    def __str__(self):
        return self.email
    
    
    def has_perm(self, perm, obj=None):
#         # ===> if the user is the admin he has the permission to do all the changes
        return self.is_admin
    
    def has_module_perms(slef, add_label):
        return True
    
