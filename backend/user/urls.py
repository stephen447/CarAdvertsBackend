from django.urls import path
from .views import RegisterView, MyTokenObtainPairView, UserView, Seller
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('data/', UserView.as_view(), name='data'),
    path('getuser/<int:user_id>/', Seller.as_view(), name='getUser')
    
]
