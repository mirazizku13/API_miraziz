from django.urls import path
from rest_framework import routers

from . import views
from .views import CarViewSet, LogoutView, LoginView, RegisterView

router = routers.DefaultRouter()
router.register('car', views.CarViewSet, basename='car')
urlpatterns = [
    # path('', views.salom, name='salom'),
    # path('car/', views.CarList.as_view(), name='car'),
    # path('car/<int:pk>', views.CarAPIView.as_view(), name='car'),
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
]+ router.urls