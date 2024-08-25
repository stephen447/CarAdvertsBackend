from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AdvertSerializer, AdvertImageSerializer
from .models import Advert, AdvertisementImage

# Utility function to filter adverts based on request parameters
def filter_adverts(queryset, params):
    filter_params = {
        'make': params.get('manufacturer'),
        'model': params.get('model'),
        'price__gte': params.get('minPrice'),
        'price__lte': params.get('maxPrice'),
        'year__gte': params.get('minYear'),
        'year__lte': params.get('maxYear'),
        'color': params.get('color'),
        'transmission': params.get('transmission'),
        'condition': params.get('condition'),
        'fuel_type': params.get('fuel'),
    }
    for key, value in filter_params.items():
        if value:
            queryset = queryset.filter(**{key: value})
    return queryset

class AdvertListView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = filter_adverts(Advert.objects.all(), request.GET)
        sortby = request.GET.get('sortby')
        if sortby:
            queryset = queryset.order_by(sortby)
        serializer = AdvertSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AdvertSerializer
from .models import AdvertisementImage

class AdvertView(APIView):
    def get(self, request, idTest):
        advert = get_object_or_404(Advert, pk=idTest)
        print(advert)
        try:
            advertisement_images = AdvertisementImage.objects.filter(advertisement=advert)
            print(advertisement_images)
        except Exception as e:
            print("Error getting advertisement images:", e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        #advertisement_images = AdvertisementImage.objects.filter(advertisement=advert)
        print(advertisement_images)
        image_serializer = AdvertImageSerializer(advertisement_images, many=True)
        advert_data = AdvertSerializer(advert).data
        advert_data['images'] = image_serializer.data
        return Response(advert_data, status=status.HTTP_200_OK)
    
    def post(self, request):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)
        # Add the authenticated user to the data to be serialized
        advert_data = {key: value[0] if isinstance(value, list) else value for key, value in request.data.items()}
        advert_data['seller'] = request.user.id  # Assign the user ID to the 'seller' field

        # Serialize the data with the user included
        serializer = AdvertSerializer(data=advert_data)
        if serializer.is_valid():
            # Save the Advert instance
            try:
                advert_instance = serializer.save()
            except Exception as e:
                print("Error saving the advert instance:", e)
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            # Handle file uploads
            uploaded_files = request.FILES.getlist('images[]')
            for uploaded_file in uploaded_files:
                AdvertisementImage.objects.create(advertisement=advert_instance, image_data=uploaded_file.read())
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def patch(self, request, idTest):
        advert = get_object_or_404(Advert, pk=idTest)
        if advert.seller.username == request.user.username:
            serializer = AdvertSerializer(advert, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response("Success", status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, idTest):
        advert = get_object_or_404(Advert, pk=idTest)
        if advert.seller.username == request.user.username:
            advert.delete()
            return Response("Success", status=status.HTTP_200_OK)
        return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

class CoverPhotoView(APIView):
    def get(self, request, idTest, *args, **kwargs):
        advert = get_object_or_404(Advert, pk=idTest)
        photo = AdvertisementImage.objects.filter(advertisement=advert).first()
        if photo:
            serializer = AdvertImageSerializer(photo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("No cover photo found", status=status.HTTP_200_OK)

class ManufacturersView(APIView):
    def get(self, request, *args, **kwargs):
        manufacturers = Advert.objects.values_list('make', flat=True).distinct()
        return Response(set(manufacturers), status=status.HTTP_200_OK)

class ModelView(APIView):
    def get(self, request, *args, **kwargs):
        manufacturer = request.GET.get('manufacturer')
        if manufacturer:
            models = Advert.objects.filter(make=manufacturer).values_list('model', flat=True).distinct()
            return Response(set(models), status=status.HTTP_200_OK)
        return Response("Manufacturer not specified", status=status.HTTP_400_BAD_REQUEST)

class FeaturedAdvertsView(APIView):
    def get(self, request, *args, **kwargs):
        advertisements = Advert.objects.order_by('?')[:3]
        if advertisements.exists():
            serializer = AdvertSerializer(advertisements, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("No advertisements found", status=status.HTTP_400_BAD_REQUEST)
