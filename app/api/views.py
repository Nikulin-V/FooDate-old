from django.db.models import F
from rest_framework import viewsets, permissions

from app.models import Product
from book.models import ProductCard, ProductCategory, ProductSubcategory
from core.middleware import get_user
from app.api.serializers import ProductSerializer, UserSerializer, ProductCardSerializer, \
    ProductCategorySerializer, ProductSubcategorySerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user to be viewed or edited.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return [get_user()]


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows current user products to be viewed or edited.
    """
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Product.products.filter(user=get_user()).order_by(
            (F('production_date') - F('product_card__shelf_life')).desc()
        )


class ProductCardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows product cards to be viewed or edited.
    """
    queryset = ProductCard.cards.order_by('name')
    serializer_class = ProductCardSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows product categories to be viewed or edited.
    """
    queryset = ProductCategory.categories.order_by('name')
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]


class ProductSubcategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows product subcategories to be viewed or edited.
    """
    queryset = ProductSubcategory.subcategories.order_by('name')
    serializer_class = ProductSubcategorySerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
