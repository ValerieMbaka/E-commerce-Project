from django.db import models

# Create your models here.
class Category(models.Model):
        category_name = models.CharField(max_length=50, unique=True)
        category_image = models.ImageField(upload_to='category_images/', blank=True, null=True)
        category_description = models.TextField(blank=True, null=True)
        
        def __str__(self):
                return self.category_name


class Product(models.Model):
        product_name = models.CharField(max_length=100, blank=False, null=False)
        product_description = models.TextField()
        product_price = models.DecimalField(max_digits=10, decimal_places=2)
        product_quantity = models.PositiveIntegerField()
        product_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
        product_image = models.ImageField(upload_to='products/')
        created_at = models.DateTimeField(auto_now_add=True)
        
        def __str__(self):
                return self.product_name