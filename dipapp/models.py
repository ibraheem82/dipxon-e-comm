from django.db import models
from decimal import Decimal
from PIL import Image
from decimal import Decimal
import os
from category.models import Category
from django.db import models
from accounts.models import Account
from django.utils.html import mark_safe
import uuid
# Create your models here.

class Product(models.Model):
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('out_of_stock', 'Out of Stock'),
        ('coming_soon', 'Coming Soon'),
        ('new', 'New'), 
    ]
    product_name   = models.CharField(max_length=200, unique=True)
    slug           = models.SlugField(max_length=200, unique=True)
    description    = models.TextField(max_length=500, blank=True)
    price          = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.PositiveIntegerField(blank=True, null=True, default=0)
            
    stock          = models.IntegerField()
    is_available   = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default='available',
    )
    category       = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    product_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    created_date   = models.DateTimeField(auto_now_add=True)
    modified_date  = models.DateTimeField(auto_now=True)

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


class Cart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    cart_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user}'s Cart"

    @property
    def grandtotal(self):
        total = 0
        for item in self.cartitem_set.all():
            total += item.get_total_price()
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"

    def get_total_price(self):
        if self.product.discount_price is not None and self.product.discount_price > 0:
            unit_price = self.product.discount_price
        else:
            unit_price = self.product.price

        # Ensure that unit_price is not None
        if unit_price is not None:
            return self.quantity * unit_price
        else:
            return 0  # Or any other default value you prefer
        
        
        
class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='gallery/images/products', max_length=255)
    caption = models.CharField(max_length=255, blank=True, null=True, help_text='Optional caption for the image')

    def __str__(self):
        return f"{self.product.product_name} - {self.caption or 'No Caption'}"

    def image_tag(self):
        return mark_safe('<img src="{}" style="max-height: 470px; max-width: 470px;" />'.format(self.images.url))

    image_tag.short_description = 'Image Preview'



    class Meta:
        verbose_name = 'Product Gallery'
        verbose_name_plural = 'Product Galleries'