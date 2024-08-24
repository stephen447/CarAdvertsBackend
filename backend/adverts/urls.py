from django.urls import path
from .views import (
    AdvertListView, 
    AdvertView, 
    ManufacturersView, 
    ModelView, 
    FeaturedAdvertsView, 
    CoverPhotoView
)

urlpatterns = [
    path('search/', AdvertListView.as_view(), name='advert-list'),
    path('advert/', AdvertView.as_view(), name='advert-create'),  # For creating an advert
    path('advert/<int:idTest>/', AdvertView.as_view(), name='advert-detail'),  # For retrieving, updating, or deleting an advert
    path('manufacturers/', ManufacturersView.as_view(), name='manufacturers-list'),
    path('models/', ModelView.as_view(), name='models-list'),
    path('featuredadverts/', FeaturedAdvertsView.as_view(), name='featuredAdverts-list'),
    path('coverPicture/<int:idTest>/', CoverPhotoView.as_view(), name="coverPhoto")
]
