from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Advert(models.Model):
    """
    Model to represent a car advertisement on the website.
    """
    id = models.AutoField(primary_key=True)
    # Basic Information
    description = models.TextField(verbose_name='Description')

    # Car Details
    make = models.CharField(max_length=50, verbose_name='Make')
    model = models.CharField(max_length=50, verbose_name='Model')
    year = models.PositiveIntegerField(verbose_name='Year')
    mileage = models.PositiveIntegerField(verbose_name='Mileage (in miles)')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')

    # Additional Details
    fuel_type = models.CharField(max_length=20, verbose_name='Fuel Type')
    transmission = models.CharField(max_length=20, verbose_name='Transmission')
    color = models.CharField(max_length=30, verbose_name='Color')
    condition = models.CharField(max_length=30, verbose_name='Condition')

    # Seller Information
    seller = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL, verbose_name='Seller')

    # Date Information
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last Updated At')

    def __str__(self):
        return f"{self.year} {self.make} {self.model} - {self.price}"

    class Meta:
        ordering = ['-created_at']

class AdvertisementImage(models.Model):
    advertisement = models.ForeignKey(Advert, on_delete=models.CASCADE, related_name='images')
    image_data = models.BinaryField()

