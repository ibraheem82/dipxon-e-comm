from django.db import models

# Create your models here.
from django.urls import reverse
import uuid
# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    description   = models.TextField(max_length = 255, blank=True)
    cat_image     = models.ImageField(upload_to='photos/categories', blank=True)
    unique_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

        
    # ===> overiding the name [category] in the django admin panel
    # ===> the name will show under our [app table] in the admin panel
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
        
    # ===> this will bring us the url of a particular category
    # ===> 'get_url' will be use in the loop in the header templates
    def get_url(self):
        # ===> 'products_by_category' is the name of the category slug used in the url
        return reverse('products_by_category', args=[self.unique_id])    
    
    
    
    def __str__(self):
        return f"{self.category_name}"