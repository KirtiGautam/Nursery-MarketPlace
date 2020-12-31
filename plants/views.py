from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from plants.models import (Plant, Order)
from accounts.models import (User, Nursery)
from plants.serializers import (PlantSerializer, OrderSerializer)


@api_view(['GET', "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def plants(request):
    if request.method == 'POST':
        if not request.user.is_staff:
            return Response({"message": "Not Allowed"}, status=status.HTTP_403_FORBIDDEN)

        plant = Plant.objects.create(
            nursery=request.user.Nursery, name=request.POST['name'], image=request.FILES['image'], price=request.POST['price'])
        return Response({'message': "Plant successfully added", "details": PlantSerializer(plant).data}, status=status.HTTP_200_OK)
    plans = request.user.Nursery.Plants.all(
    ) if request.user.is_staff else Plant.objects.all()
    return Response({'plants': PlantSerializer(plans, many=True).data}, status=status.HTTP_200_OK)


@api_view(['GET', "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def plantDetails(request, id):
    try:
        plant = Plant.objects.get(id=id)
        if request.method == "POST":
            if request.user.is_staff:
                return Response({"message": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
            order = Order.objects.create(
                user=request.user, plant=plant, quantity=request.POST['quantity'])
            return Response({'message': "Order Successfully placed", "details": OrderSerializer(order).data}, status=status.HTTP_200_OK)
        return Response(PlantSerializer(plant).data, status=status.HTTP_200_OK)
    except Plant.DoesNotExist:
        return Response({"message": "No such plant exists"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def orders(request):
    if request.user.is_staff:
        ords = Order.objects.filter(plant__nursery=request.user.Nursery)
        return Response({'orders': OrderSerializer(ords, many=True).data}, status=status.HTTP_200_OK)
    return Response({'message': "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
