from django.db import models

# Create your models here.

class Product(models.Model):
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('out_of_stock', 'Out of Stock'),
        ('coming_soon', 'Coming Soon'),
        ('new', 'New'), 
    ]
    product_name   = models.CharField(max_length=200, unique=True)
    slug           = models.SlugField(max_length = 200, unique= True)
    description    = models.TextField(max_length = 500, blank=True)
    price          = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.PositiveIntegerField()
    images         = models.ImageField(upload_to = 'photos/products')
    stock          = models.IntegerField()
    is_available   = models.BooleanField(default=True)
    # category      = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date   = models.DateTimeField(auto_now_add=True)
    modified_date  = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Calculate discounted price before saving
        if self.discount_price > 0:
            discount = self.price * (self.discount_price / 100)
            self.discounted_price = self.price - discount
        else:
            # If discount is not provided, set discounted price same as regular price
            self.discounted_price = self.price

        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name