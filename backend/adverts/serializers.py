from rest_framework import serializers
from .models import Advert, AdvertisementImage

class AdvertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advert
        fields = '__all__'  # Ensure all fields are included

class AdvertImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementImage
        fields = '__all__'