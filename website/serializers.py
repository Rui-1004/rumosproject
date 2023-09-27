from rest_framework import serializers
from .models import User, Address, Product, Category, Cart, CartItem, Order


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
