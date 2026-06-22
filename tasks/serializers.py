from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

from tasks.models import Car


class CarListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('id', 'name', 'description', 'price', 'brand', 'model', 'year')
        extra_kwargs = {'id': {'read_only': True}}

class CarCreateAndUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('id', 'name', 'description', 'price', 'brand', 'model', 'year')
        extra_kwargs = {'id': {'read_only': True}}

    def validate(self, data):
        name = data.get('name')
        description = data.get('description')

        if name == description:
            raise serializers.ValidationError('name and description cannot be same')
        return data

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwordlar mos emas")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user= authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("username or password is incorrect")

        return {"user":user}