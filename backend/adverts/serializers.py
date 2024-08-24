# serializers.py

from rest_framework import serializers
from .models import Advert, AdvertisementImage

class AdvertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advert
        fields = '__all__'

class AdvertImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementImage
        fields = '__all__'

class FeaturedAdvertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advert
        fields = ['id', 'description', 'make', 'model', 'year', 'mileage', 'price', 'fuel_type', 'transmission', 'color', 'condition', 'created_at', 'updated_at', 'images']
