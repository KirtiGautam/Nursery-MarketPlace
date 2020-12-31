from rest_framework import serializers
from accounts.models import (User, Nursery)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if instance.is_staff:
            response['nursery_name'] = instance.Nursery.name
        return response


class NurserySerializer(serializers.ModelSerializer):
    class Meta:
        model = Nursery
        fields = '__all__'
