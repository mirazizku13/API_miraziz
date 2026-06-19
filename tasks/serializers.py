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

