from django.db import models
from shortuuid.django_fields import ShortUUIDField

from accounts.models import User

# was imported so as to display images in the admin panel.
from django.utils.html import mark_safe

# ###########
STATUS_CHOICE = (
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)
    category       = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    product_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    created_date   = models.DateTimeField(auto_now_add=True)
    modified_date  = models.DateTimeField(auto_now=True)


# ###########
STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)




RATING = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id)

class Category(models.Model):
    # cid is the same as (id)
    # cat is the prefix and it will be added along side the shortuuidfield
    # will be picking random alphabet and numbers to make up the id (alphabet)
    cid = ShortUUIDField(unique = True, length = 10, max_length = 30, prefix="cat", alphabet="abcbefghi12345")
    title = models.CharField(max_length = 100, default="Fashion")
    image = models.ImageField(upload_to="category", default="category.jpg")
    
    
    class Meta:
        verbose_name_plural = "Categories"
        
    def category_image(self):
        return mark_safe('<img src ="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title
    
    def get_url(self):
        return reverse('product_details', args = [str(self.product_id)])      
    
class Tags(models.Model):
    pass
        
        
class Vendor(models.Model):
    vid = ShortUUIDField(unique = True, length = 10, max_length = 30, prefix="ven", alphabet="abcbefghi12345")
    title = models.CharField(max_length = 100, default="Ibraheem")
    image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")
    description = models.TextField(null = True, blank = True, default="Good company")
    address = models.CharField(max_length = 100, default = "12 Sadiku street Ilasamaja lagos state")
    contact = models.CharField(max_length = 100, default = "+234 8102673964")
    chat_resp_time = models.CharField(max_length = 100, default = "100", null = True, blank = True)
    shipping_on_time = models.CharField(max_length = 100, default = "100", null = True, blank = True)
    authentic_rating = models.CharField(max_length = 100, default="100", null = True, blank = True)
    days_return = models.CharField(max_length = 100, default = "100", null = True, blank = True)
    warranty_period = models.CharField(max_length = 100,  default = "100", null = True, blank = True)
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    
    class Meta:
        verbose_name_plural = "Vendors"
    
    def vendor_image(self):
        return mark_safe('<img src ="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return f"Image for {self.product.product_name}"

    def save(self, *args, **kwargs):
        # Check the number of existing images for the product
        existing_images_count = self.product.product_images.count()

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

            # Delete the original image file after saving the resized image
            os.remove(self.image.path)

            # Update the image field with the resized image path
            self.image.name = os.path.join("photos", "products", base_filename)
            super().save(*args, **kwargs)



class Cart(models.Model):
    user        =  models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    cart_id     = models.CharField(max_length=250, blank=True)
    date_added  = models.DateField(auto_now_add=True)
    def __str__(self):
        return "ok"

    # grandtotal property: Calculates the total price of all items in the cart. It first retrieves all associated cart items using cartitems_set.all(). Then, it uses list comprehension to sum the subtotal of each item.
    @property
    def grandtotal(self):
        cartitems = self.cartitem_set.all()
        total = sum([item.subtotal for item in cartitems])
        return total
    
    
    # cartquantity property: Calculates the total quantity of all items in the cart. Similar to grandtotal, it retrieves all cart items and uses list comprehension to sum their quantity.
    @property
    def cartquantity(self):
        cartitems = self.cartitems_set.all()
        total = sum([item.quantity for item in cartitems])
        return total
    
    

class CartItem(models.Model):
    
    cart        = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product     = models.ForeignKey(Product, on_delete=models.CASCADE) 
    quantity    = models.PositiveIntegerField(default=0)
    is_active   = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"
    
    def __unicode__(self):
        return self.product
    
    # The subtotal property calculates the total price of a specific item in the cart based on its quantity and price
    @property
    def subtotal(self):
        total = self.quantity * self.product.price    
        return total