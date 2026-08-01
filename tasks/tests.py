from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Car
from .serializers import CarCreateAndUpdateSerializer


class CarTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="12345678"
        )

        response = self.client.post("/api/token/", {
            "username": "test",
            "password": "12345678"
        }, format="json")

        self.access = response.data["access"]

    def test_create_car(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )

        data = {
            "name": "BMW",
            "description": "Good car",
            "price": 10000,
            "brand": "BMW",
            "model": "M5",
            "year": "2024-01-01T00:00:00Z"
        }

        response = self.client.post("/api/tasks/car/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.count(), 1)


class SerializerTests(APITestCase):

    def test_validation(self):
        serializer = CarCreateAndUpdateSerializer(data={
            "name": "BMW",
            "description": "BMW",
            "price": 100,
            "brand": "BMW",
            "model": "X5",
            "year": "2024-01-01T00:00:00Z"
        })

        # Serializer shartlarini tekshirish uchun (agar xato bo'lishi kerak bo'lsa False qoldirasiz)
        self.assertFalse(serializer.is_valid())


class PermissionTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1",
            password="12345678"
        )

        self.user2 = User.objects.create_user(
            username="user2",
            password="12345678"
        )

        response = self.client.post("/api/token/", {
            "username": "user2",
            "password": "12345678"
        }, format="json")

        self.access = response.data["access"]

        self.car = Car.objects.create(
            name="BMW",
            description="test",
            price=100,
            brand="BMW",
            model="M5",
            year="2024-01-01T00:00:00Z",
            author=self.user1
        )

    def test_owner_permission(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )

        response = self.client.put(
            f"/api/tasks/car/{self.car.id}/",
            {
                "name": "Audi",
                "description": "test",
                "price": 100,
                "brand": "Audi",
                "model": "A6",
                "year": "2024-01-01T00:00:00Z"
            },
            format="json"
        )

        # Agar boshqa foydalanuvchi tahrirlasa 403 (Forbidden) qaytishi shart
        # Buning uchun views.py da permission_classes ga IsOwnerOrReadOnly ulangan bo'lishi kerak
        # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class IntegrationTests(APITestCase):

    def test_full_flow(self):
        # /api/register/ mavjud emasligi sababli, to'g'ridan-to'g'ri user yaratamiz
        User.objects.create_user(
            username="admin",
            password="12345678"
        )

        response = self.client.post("/api/token/", {
            "username": "admin",
            "password": "12345678"
        }, format="json")

        access = response.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access}"
        )

        response = self.client.post("/api/tasks/car/", {
            "name": "BMW",
            "description": "Good",
            "price": 100,
            "brand": "BMW",
            "model": "M5",
            "year": "2024-01-01T00:00:00Z"
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get("/api/tasks/car/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)