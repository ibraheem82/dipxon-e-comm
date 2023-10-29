from django.db import models
from decimal import Decimal
from PIL import Image
from decimal import Decimal
import os

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
    is_available   = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default='available',
    )
    # category      = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date   = models.DateTimeField(auto_now_add=True)
    modified_date  = models.DateTimeField(auto_now=True)
    
    
    def save(self, *args, **kwargs):
        # Calculate discounted price before saving
        if self.discount_price > 0:
            discount_percentage = Decimal(self.discount_price) / 100
            discount = self.price * discount_percentage
            self.discounted_price = self.price - discount
        else:
            # If discount is not provided, set discounted price the same as the regular price
            self.discounted_price = self.price

        # Call the original save method
        super().save(*args, **kwargs)

        # Resize and save image if it exists
        if self.images and self.images.name:
            product_name = self.product_name.replace(" ", "_").lower()

            # Ensure the original image file exists before proceeding
            if os.path.exists(self.images.path):
                # Open the original image
                img = Image.open(self.images.path)

                # Resize the image
                resized_img = img.resize((500, 666), resample=Image.LANCZOS)

                # Use the product name as part of the filename
                base_filename = f"{product_name}_image.png"

                # Save the resized image in the same directory as the original image
                output_path = os.path.join("media", "photos", "products", base_filename)
                resized_img.save(output_path, "PNG")

                # Update the images field with the new filename
                self.images.name = os.path.join("photos", "products", base_filename)

                # Call the original save method again to update the model with the new image filename
                super().save(*args, **kwargs)



    def __str__(self):
        return self.product_name