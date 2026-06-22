from django.contrib.auth import authenticate, login, logout
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.models import Car
from tasks.serializers import CarListSerializer, CarCreateAndUpdateSerializer, RegisterSerializer


# Create your views here.
def salom(request):
    return Response({'message': 'Hello World!'})
#
# class CarList(APIView):
#     def get(self, request):
#         cars = Car.objects.all()
#         serializer = CarListSerializer(cars, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = CarCreateAndUpdateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
# class CarAPIView(APIView):
#     def get(self, request, pk):
#         cars = Car.objects.filter(pk=pk)
#         serializer = CarListSerializer(cars, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
#     def put(self, request, pk=None):
#         car = get_object_or_404(Car, pk=pk)
#         serializer = CarCreateAndUpdateSerializer(data=request.data, instance=car)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def delete(self, request, pk=None):
#         car = get_object_or_404(Car, pk=pk)
#         car.delete()
#         return Response({'message': 'Success!'})


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarListSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            print(request.data)
            return JsonResponse({'status': 'success'}, status=status.HTTP_200_OK)
        return JsonResponse({'status': 'fail'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self,request):
        logout(request)
        return JsonResponse({'status': 'success'}, status=status.HTTP_200_OK)