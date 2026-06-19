from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.models import Car
from tasks.serializers import CarListSerializer, CarCreateAndUpdateSerializer


# Create your views here.
def salom(request):
    return Response({'message': 'Hello World!'})

class CarList(APIView):
    def get(self, request):
        cars = Car.objects.all()
        serializer = CarListSerializer(cars, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CarCreateAndUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
class CarAPIView(APIView):
    def get(self, request, pk):
        cars = Car.objects.filter(pk=pk)
        serializer = CarListSerializer(cars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, pk=None):
        car = get_object_or_404(Car, pk=pk)
        serializer = CarCreateAndUpdateSerializer(data=request.data, instance=car)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        car = get_object_or_404(Car, pk=pk)
        car.delete()
        return Response({'message': 'Success!'})