from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from api.v1.accounts.serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from api.v1.main.functions import generate_serializer_errors
from accounts.models import *
# from django.contrib.auth import logout
from rest_framework_simplejwt.exceptions import TokenError

@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    serializer = UserProfileSignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        response_data = {
            "StatusCode": 6000,
            "data": {
                "title": "Success",
                "message": "User created successfully",
            }
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "data": {
                "title": "Failed",
                "message": generate_serializer_errors(serializer._errors),
            }
        }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    
    if not email or not password:
        response_data = {
            "StatusCode": 6001,
            "data": {
                "title": "Failed",
                "message": "Email and password are required",
            }
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(request, username=email, password=password)
    
    if user is None:
        response_data = {
            "StatusCode": 6001,
            "data": {
                "title": "Failed",
                "message": "Invalid email or password",
            }
        }
        return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
    
    # Generate tokens
    refresh = RefreshToken.for_user(user)
    
    response_data = {
        "StatusCode": 6000,
        "data": {
            "title": "Success",
            "message": "Login successful",
            "tokens": {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
        }
    }
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    refresh_token = request.data.get('refresh')
    
    if not refresh_token:
        response_data = {
            "StatusCode": 6001,
            "data": {
                "title": "Failed",
                "message": "Refresh token is required",
            }
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        refresh = RefreshToken(refresh_token)
        response_data = {
            "StatusCode": 6000,
            "data": {
                "title": "Success",
                "message": "Token refresh successful",
                "tokens": {
                    "access": str(refresh.access_token)
                }
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        response_data = {
            "StatusCode": 6001,
            "data": {
                "title": "Failed",
                "message": "Invalid refresh token",
            }
        }
        return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_details(request):
    user = request.user
    if UserProfile.objects.filter(user=user).exists():
        user = UserProfile.objects.get(user=user)

        serialized_data = UserSerializer(instance=user,context = {"request": request}).data

        response_data = {
            "StatusCode": 6000,
            "data" : serialized_data   
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "data" : {
                "title" : "failed",
                "message" : "This post is not avaliable at this moment"
            }
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_details(request,pk):
    if UserProfile.objects.filter(id=pk).exists():
        user = UserProfile.objects.get(id=pk)

        serialized_data = UserSerializer(instance=user,context = {"request": request}).data

        response_data = {
            "StatusCode": 6000,
            "data" : serialized_data   
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "data" : {
                "title" : "failed",
                "message" : "This post is not avaliable at this moment"
            }
        }

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        # Get the refresh token from the request data
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response(
                {"message": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create a RefreshToken object and blacklist it
        token = RefreshToken(refresh_token)
        token.blacklist()

        # Optional: Logout the user from the session if you're using session-based auth as well
        # logout(request)

        response_data = {
            "StatusCode": 6000,
            "data": {
                "title": "Success",
                "message": "Logout successful",
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)

    except TokenError:
        # If the refresh token is invalid or expired
        return Response(
            {"message": "Invalid or expired refresh token"},
            status=status.HTTP_400_BAD_REQUEST
        )

    
