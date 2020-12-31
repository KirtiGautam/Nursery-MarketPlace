from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from accounts.models import (User, Nursery)
from accounts.serializers import (UserSerializer)
from django.shortcuts import render, redirect

def index(request):
    return redirect('https://documenter.getpostman.com/view/11572058/TVt1A5no')


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    try:
        if User.objects.filter(email=request.POST['email']):
            return Response({'message': "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create(
            email=request.POST['email'], name=request.POST['name'])

        if request.POST['password'] != request.POST['password2']:
            return Response({'message': "Passwords don't match"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(request.POST['password'])
        user.save()

        return Response({'message': "Successfully registered", "user": UserSerializer(user).data, "token": Token.objects.create(user=user).key}, status=status.HTTP_200_OK)
    except Exception as e:
        if user:
            user.delete()
        return Response({'message': e.args}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def nurserySignup(request):
    try:
        if User.objects.filter(email=request.POST['email']):
            return Response({'message': "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create(
            email=request.POST['email'], name=request.POST['name'], is_staff=True)
        if request.POST['password'] != request.POST['password2']:
            return Response({'message': "Passwords don't match"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(request.POST['password'])
        user.save()
        nursery = Nursery.objects.create(
            user=user, nursery_name=request.POST['nursery_name'])
        return Response({'message': "Successfully registered", "user": UserSerializer(user).data, "token": Token.objects.create(user=user).key}, status=status.HTTP_200_OK)
    except Exception as e:
        if user:
            user.delete()
        return Response({'message': e.args}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    try:
        user = User.objects.get(email=request.POST['email'])
        if not user.check_password(request.POST['password']):
            return Response({'message': "Password Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED)
        if Token.objects.filter(user=user).exists():
            Token.objects.get(user=user).delete()
        token = Token.objects.create(user=user)
        return Response({'message': "Successfully logged in", "token": token.key, "user": UserSerializer(user).data}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'message': "No such User"}, status=status.HTTP_404_NOT_FOUND)
