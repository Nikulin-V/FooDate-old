from django.urls import path, include
from rest_framework import routers

from app.api import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'product-cards', views.ProductCardViewSet)
router.register(r'product-categories', views.ProductCategoryViewSet)
router.register(r'product-subcategories', views.ProductSubcategoryViewSet)
router.register(r'me', views.UserViewSet, basename='me')

urlpatterns = [
    path('', include(router.urls)),
    path('api/', include('rest_framework.urls', namespace='rest_framework'))
]
