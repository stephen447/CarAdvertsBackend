from django.shortcuts import render
from .serializers import userLoginSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import logout
from .models import CustomUser
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import requests

# Create your views here.
# Login View

class LoginView(APIView):
    def post(self, request, format=None, *args, **kwargs):
        # If user alreadfy authenticated, return response with 200 OK
        print("request header: ", request.user)
        if request.user.is_authenticated:
            print("Authenticated")
            return Response("Already logged in!", status=status.HTTP_200_OK)
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response("Logged In!", status=status.HTTP_200_OK)
        else:
            # Authentication failed
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        # If user authenticated, logout the user, otherwise return response with 401 unauthorised
        if request.user.is_authenticated:
            logout(request)
            return Response("Logged Out!", status=status.HTTP_200_OK)
        else:
            return Response("You are not logged in!", status=status.HTTP_401_UNAUTHORIZED)
    
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if request.user.is_authenticated:
            return Response({"error": "User already logged in, please log out"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            # Check if the username is unique
            if CustomUser.objects.filter(username=serializer.validated_data['username']).exists():
                return Response({"error": "Username already exists haha"}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the email is unique
            if CustomUser.objects.filter(email=serializer.validated_data['email']).exists():
                return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

            # Create a new user
            username = serializer.validated_data['username']
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            phone_number = serializer.validated_data['phone_number']
            date_of_birth = serializer.validated_data['date_of_birth']
            user = CustomUser.objects.create(username=username, first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, date_of_birth=date_of_birth)
            user.set_password(password) # Need to set the users password using the set password function - for hashing
            user.save()
            return Response("User registered successfully", status=status.HTTP_201_CREATED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response("User updated successfully", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = get_object_or_404(CustomUser, pk=request.user.id)
            user.delete()
            return Response("User deleted successfully", status=status.HTTP_200_OK)
        return Response("You are not logged in!", status=status.HTTP_401_UNAUTHORIZED)

class DeleteUserView(APIView):
    def post(self, request, *args, **kwargs):
        # If user authenticated, delete the user, otherwise return response with 401 unauthorised
        user = get_object_or_404(CustomUser, pk=request.user.id)
        return Response("User deleted successfully", status=status.HTTP_200_OK)
        
# Profile View
class ProfileView(APIView):
    # get details - email, adverts, name, username etc....
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = get_object_or_404(CustomUser, pk=request.user.id)
            return Response({"username": user.username, "email": user.email, "first_name": user.first_name, "last_name": user.last_name, "phone_number": user.phone_number, "date_of_birth": user.date_of_birth}, status=status.HTTP_200_OK)
        return Response("Not logged in!", status=status.HTTP_200_OK)

class UserView(APIView):
    # get username
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = get_object_or_404(CustomUser, pk=request.user.id)
            return Response({"username": user.username}, status=status.HTTP_200_OK)
        return Response("Not logged in!", status=status.HTTP_200_OK)


# View for getting the user with a passed ID
class UserDetailView(APIView):
    def get(self, request, pk, format=None):
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    



    