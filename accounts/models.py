from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid
from uuid import UUID

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
            id=uuid.uuid4(),
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
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        
        # Check if UserProfile already exists for the superuser
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        
        if not created:
            # Update the existing UserProfile if it already exists
            user_profile.address_line_1 = ''  # Update with the fields you want to modify
            user_profile.address_line_2 = ''
            user_profile.profile_picture = 'default_profile_picture.png'
            user_profile.city = ''
            user_profile.state = ''
            user_profile.country = ''
            user_profile.save()

        # Set the permissions and save the user after updating the UserProfile
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)

        return user

    
    # * creating a custom user model..
class Account(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, editable=False, unique=True)
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
        return str(self.id)
    
    
    def has_perm(self, perm, obj=None):
#         # ===> if the user is the admin he has the permission to do all the changes
        return self.is_admin
    
    def has_module_perms(slef, app_label):
        return True
    


class UserProfile(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user            = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line_1  = models.CharField(blank = True, max_length = 100)
    address_line_2  = models.CharField(blank = True, max_length = 100)
    city            = models.CharField(blank=True, max_length=20)
    state           = models.CharField(blank=True, max_length=20)
    country         = models.CharField(blank=True, max_length=20)
    # ip_address = models.GenericIPAddressField(blank=True, null=True)
    # location = models.CharField(blank=True, max_length=100)



    def __str__(self):
        return self.user.first_name



    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'