from django.db import models

# Create your models here.
class FirebaseUser(models.Model):
        uid = models.CharField(max_length=255, unique=True)
        full_name = models.CharField(max_length=255)
        email = models.EmailField(unique=True)
        role = models.CharField(max_length=50,  choices=[('buyer', 'Buyer'), ('seller', 'Seller')])  # 'buyer' or 'seller'
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

        def __str__(self):
                return self.full_name
