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
        fields = ['image_data']  # Only include the image_data field

class AdvertSerializer(serializers.ModelSerializer):
    images = AdvertImageSerializer(many=True, write_only=True)  # Specify the related images here

    class Meta:
        model = Advert
        fields = '__all__'

    def create(self, validated_data):
        # Extract images from validated_data
        images_data = validated_data.pop('images', [])
        advert_instance = Advert.objects.create(**validated_data)  # Create the Advert instance

        # Create AdvertisementImage instances
        for image_data in images_data:
            AdvertisementImage.objects.create(advertisement=advert_instance, **image_data)
        
        return advert_instance

class FeaturedAdvertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advert
        fields = ['id', 'description', 'make', 'model', 'year', 'mileage', 'price', 'fuel_type', 'transmission', 'color', 'condition', 'created_at', 'updated_at', 'images']
