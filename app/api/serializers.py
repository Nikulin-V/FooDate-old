from django.contrib.auth.models import User
from rest_framework import serializers

from app.models import Product
from book.models import ProductCard


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_joined']


class ProductCardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductCard
        fields = '__all__'


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    product_card = serializers.RelatedField(source='productcard.name', read_only=True)

    class Meta:
        model = Product
        exclude = ['user']
