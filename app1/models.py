from django.db import models

# Create your models here.
class Slider(models.Model):
        slider_heading = models.CharField(max_length=50)
        slider_description = models.TextField()
        slider_image = models.ImageField(upload_to='carousel/')
        
        def __str__(self):
                return self.slider_heading


class AboutSection(models.Model):
        about_heading = models.CharField(max_length=50)
        about_description1 = models.TextField()
        about_description2 = models.TextField()
        background_image = models.ImageField(upload_to='about_backgrounds/', null=True, blank=True)
        
        def __str__(self):
                return self.about_heading


class Service(models.Model):
        service_name = models.CharField(max_length=50, default='Clothes')
        service_description = models.TextField()
        service_button = models.CharField(max_length=50, default='Shop Now')
        service_image = models.ImageField(upload_to='services/', null=False, default='static/app1/images/clothes1.jpeg')
        
        def __str__(self):
                return self.service_name
