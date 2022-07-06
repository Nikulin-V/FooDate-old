from rest_framework import viewsets, permissions

from app.models import Product
from book.models import ProductCard
from core.middleware import get_user
from app.api.serializers import ProductSerializer, UserSerializer, ProductCardSerializer


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
    queryset = Product.products.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductCardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows product cards to be viewed or edited.
    """
    queryset = ProductCard.cards.all()
    serializer_class = ProductCardSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
