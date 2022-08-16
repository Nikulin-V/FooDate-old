from rest_framework import serializers

from app.models import Product
from book.models import ProductCard, ProductSubcategory, ProductCategory
from users.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_joined']


class ProductCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductSubcategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductSubcategory
        fields = '__all__'


class ProductCardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductCard
        exclude = ['gallery']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        exclude = ['user']
