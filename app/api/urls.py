from django.urls import path, include
from rest_framework import routers

from app.api import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'product-cards', views.ProductCardViewSet)
router.register(r'me', views.UserViewSet, basename='me')

urlpatterns = [
    path('', include(router.urls)),
    path('api/', include('rest_framework.urls', namespace='rest_framework'))
]
