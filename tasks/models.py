from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Car(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.DateTimeField()