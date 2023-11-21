from django.db import models
from decimal import Decimal
from PIL import Image
from decimal import Decimal
import os
from category.models import Category

# Create your models here.

class Product(models.Model):
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('out_of_stock', 'Out of Stock'),
        ('coming_soon', 'Coming Soon'),
        ('new', 'New'), 
    ]
    PRODUCT_CATEGORY_GENDER = [
        ('men', 'Men'),
        ('woman', 'Women'),
        ('kids', 'Kids'),
    ]
    product_name   = models.CharField(max_length=200, unique=True)
    slug           = models.SlugField(max_length = 200, unique= True)
    description    = models.TextField(max_length = 500, blank=True)
    price          = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.PositiveIntegerField(blank=True, null=True, default=0)
    stock          = models.IntegerField()
    is_available   = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default='available',
    )
    category       = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    product_gender = models.CharField(
        max_length=20,
        choices=PRODUCT_CATEGORY_GENDER,
        default='men',
    )
    created_date   = models.DateTimeField(auto_now_add=True)
    modified_date  = models.DateTimeField(auto_now=True)
    
    
    def save(self, *args, **kwargs):
        # Check if discount_price is not None before comparison
        if self.discount_price is not None and self.discount_price > 0:
            discount_percentage = Decimal(self.discount_price) / 100
            discount = self.price * discount_percentage
            self.discounted_price = self.price - discount
        else:
            # If discount is not provided or is None, set discounted price the same as the regular price
            self.discounted_price = self.price

        # Call the original save method
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.product_name        
        
class ProductImage(models.Model):
    MAX_IMAGES_PER_PRODUCT = 2

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image   = models.ImageField(upload_to='photos/products')

    def __str__(self):
        return f"Image for {self.product.product_name}"

    def save(self, *args, **kwargs):
        # Check the number of existing images for the product
        existing_images_count = self.product.images.count()

        if existing_images_count >= self.MAX_IMAGES_PER_PRODUCT:
            # If the maximum number of images is reached, don't save the new image
            return

        super().save(*args, **kwargs)

        if self.image and self.image.name:
            product_name = self.product.product_name.replace(" ", "_").lower()
            base_filename = f"{product_name}_image_{self.pk}.png"

            img = Image.open(self.image.path)
            resized_img = img.resize((500, 666), resample=Image.LANCZOS)

            output_path = os.path.join("media", "photos", "products", base_filename)
            resized_img.save(output_path, "PNG")

            self.image.name = os.path.join("photos", "products", base_filename)
            super().save(*args, **kwargs)
