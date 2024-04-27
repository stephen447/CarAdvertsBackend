from django.shortcuts import render
from .serializers import AdvertSerializer, AdvertImageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Advert, AdvertisementImage

class AdvertListView(APIView):
    def get(self, request, *args, **kwargs):
        # Parse the request (example: extract parameters from query string)
        make = request.GET.get('manufacturer')
        model = request.GET.get('model')
        min_price = request.GET.get('minPrice')
        max_price = request.GET.get('maxPrice')
        min_year = request.GET.get('minYear')
        max_year = request.GET.get('maxYear')
        color = request.GET.get('color')
        transmission = request.GET.get('transmission')
        condition = request.GET.get('condition')
        fuel = request.GET.get('fuel')
        sortby = request.GET.get('sortby')
        print(min_price, max_price, )
        # Query the database
        # Get all adverts from the database
        queryset = Advert.objects.all()
        # Filter the adverts based on the parameters
        if make:
            queryset = queryset.filter(make=make)
        if model:
            queryset = queryset.filter(model=model)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if min_year:
            queryset = queryset.filter(year__gte=min_year)
        if max_year:
            queryset = queryset.filter(year__lte=max_year)
        if color:
            queryset = queryset.filter(color=color)
        if transmission:
            queryset = queryset.filter(transmission=transmission)
        if condition:
            queryset = queryset.filter(condition=condition)
        if fuel:
            queryset = queryset.filter(fuel_type=fuel)
        if sortby:
            queryset = queryset.order_by(sortby)
        # Serialize the data to JSON
        serializer = AdvertSerializer(queryset, many=True)
        # Return a HTTP Response with a list of adverts
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AdvertView(APIView):
    def get(self, request, idTest):
        if idTest:
            advert = get_object_or_404(Advert, pk=idTest)
            if(advert):
                # Get the images for the corresponding advert
                advertisement_images = AdvertisementImage.objects.filter(advertisement=advert)
                # Serialize the advertisement images
                image_serializer = AdvertImageSerializer(advertisement_images, many=True)
                advert_data = AdvertSerializer(advert).data
                # Add the serialized images to the advertisement data
                advert_data['images'] = image_serializer.data
                return Response(advert_data, status=status.HTTP_200_OK)
            else:
                return Response("Advertisement not found", status=status.HTTP_404_NOT_FOUND)
        
        else:
            return Response("Error", status=status.HTTP_400_BAD_REQUEST)
              
    def post(self, request, format=None):
        if request.user.is_authenticated:
            # Store the seller id in the request data
            request.data['seller'] = request.user.id
            # Create a serializer with the request data
            serializer = AdvertSerializer(data=request.data)
            # Check if the data is valid
            if serializer.is_valid():
                # Save the data to the database
                advert_instance = serializer.save()
                # Loop through the images and save them to the database
                if 'images[]' in request.FILES:
                    # Access the files as a list
                    uploaded_files = request.FILES.getlist('images[]')
                    
                    for uploaded_file in uploaded_files:
                        # Process each uploaded file
                        file_contents = uploaded_file.read()
                        file_name = uploaded_file.name
                        file_size = uploaded_file.size
                        AdvertisementImage.objects.create(advertisement=advert_instance, image_data=file_contents)


                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Not authenticated", status=status.HTTP_401_UNAUTHORIZED)
        
    
    def patch(self, request, idTest):
        if request.user.is_authenticated:
            if idTest:
                advert = Advert.objects.get(id=idTest)
                if(advert.seller.username==request.user.username):
                    #Update the advert
                    serializer = AdvertSerializer(instance=advert, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response("Success", status=status.HTTP_201_CREATED)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response("Error", status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response("Error", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Error", status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, idTest, request, format=None):
        if request.user.is_authenticated:
            if idTest:
                advert = get_object_or_404(Advert, pk=id)
                if(advert.seller.username==request.user.username):
                    advert.delete()
                    return Response("Sucess", status=status.HTTP_201_CREATED)
                else:
                    return Response("Error", status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response("Error", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Error", status=status.HTTP_401_UNAUTHORIZED)
class CoverPhoto(APIView):
    def get(self,request,idTest, *args, **kwargs):
        # Get the advert
        advert = Advert.objects.get(id=idTest)
        # Get the photos for the advert
        photos = AdvertisementImage.objects.filter(advertisement=advert)
        # Return the 1st photo
        image_serializer = AdvertImageSerializer(photos)
        if(photos.exists()):
            return Response(image_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("No cover photo found", status=status.HTTP_200_OK)
class ManufacturersView(APIView):
    def get(self, request, *args, **kwargs):
        manufacturers = Advert.objects.values_list('make', flat=True).distinct()
        manufacturers = list(set(manufacturers))
        # Return a HTTP Response with a list of adverts
        return Response(manufacturers, status=status.HTTP_200_OK)

class ModelView(APIView):
    def get(self, request, *args, **kwargs):
        # Get the manufacturer from the request
        manufacturer = request.GET.get('manufacturer')
        
        # Check if manufacturer is provided
        if manufacturer:
            # Filter adverts by the manufacturer
            queryset = Advert.objects.filter(make=manufacturer)
            # Get distinct models for the filtered adverts
            model = queryset.values_list('model', flat=True).distinct()
            model = list(set(model))
            # Return the list of models
            return Response(model, status=status.HTTP_200_OK)
        else:
            # Handle the case where manufacturer is not provided
            return Response("Manufacturer not specified", status=status.HTTP_400_BAD_REQUEST)

class FeaturedAdvertsView(APIView):
    def get(self, request, *args, **kwargs):
        # Get three random Advertisements from the database
        advertisements = Advert.objects.order_by('?')[:3]
        if advertisements:
            return Response(AdvertSerializer(advertisements, many=True).data, status=status.HTTP_200_OK)
        else:
            return Response("Error", status=status.HTTP_400_BAD_REQUEST)


