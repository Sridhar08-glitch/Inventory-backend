from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Category, Supplier, Product,
    SaleOrder, SaleItem, StockMovement, UserProfile,
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = '__all__'

class SaleOrderSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = SaleOrder
        fields = '__all__'

class StockMovementSerializer(serializers.ModelSerializer):
    # stock_before and stock_after are always computed by the view;
    # they must never be accepted from or required of the client.
    stock_before = serializers.IntegerField(read_only=True)
    stock_after = serializers.IntegerField(read_only=True)

    class Meta:
        model = StockMovement
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'