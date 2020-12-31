from rest_framework import serializers
from accounts.serializers import NurserySerializer, UserSerializer
from plants.models import Plant, Order


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['nursery'] = NurserySerializer(instance.nursery).data
        return response


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        response['plant'] = PlantSerializer(instance.plant).data
        response['total'] = int(instance.quantity)*float(instance.plant.price)
        return response
