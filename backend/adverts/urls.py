from django.contrib import admin
from django.urls import path, include 
from .views import AdvertListView, AdvertView, ManufacturersView, ModelView, FeaturedAdvertsView, CoverPhoto
urlpatterns = [
    path('search/', AdvertListView.as_view(), name='advert-list'),
    path('advert/', AdvertView.as_view(), name='advert-list'),
    path('advert/<int:idTest>/', AdvertView.as_view(), name='advert-list'),
    path('manufacturers/', ManufacturersView.as_view(), name='manufacturers-list'),
    path('models/', ModelView.as_view(), name='models-list'),
    path('featuredadverts/', FeaturedAdvertsView.as_view(), name='featuredAdverts-list'),
    path('coverPicture/<int:idTest>/', CoverPhoto.as_view(), name="coverPhoto" )

]