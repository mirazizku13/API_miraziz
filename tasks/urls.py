from django.urls import path
from . import views

urlpatterns = [
    path('', views.salom, name='salom'),
    path('car/', views.CarList.as_view(), name='car'),
    path('car/<int:pk>', views.CarAPIView.as_view(), name='car'),
]