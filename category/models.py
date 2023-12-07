from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length = 255, blank=True)
    slug = models.SlugField(max_length = 100,unique=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)

        
    # ===> overiding the name [category] in the django admin panel
    # ===> the name will show under our [app table] in the admin panel
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
        
    # ===> this will bring us the url of a particular category
    # ===> 'get_url' will be use in the loop in the header templates
    def get_url(self):
        # ===> 'products_by_category' is the name of the category slug used in the url
        return reverse('products_by_category', args=[self.slug])    
    
    
    
    def __str__(self):
        return self.category_name