from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db.models import Q
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import (
    Category, Supplier, Product,
    SaleOrder, SaleItem, StockMovement, UserProfile,
)
from .serializers import (
    CategorySerializer, SupplierSerializer, ProductSerializer,
    SaleOrderSerializer, StockMovementSerializer,
)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        
        # Get or create profile
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'business_name': profile.business_name,
            'business_email': profile.business_email,
        })
    return Response({'error': 'Invalid credentials'}, status=400)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    # Delete the token
    request.auth.delete()
    return Response({'message': 'Logged out'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    
    return Response({
        **user_data,
        'business_name': profile.business_name,
        'business_address': profile.business_address,
        'business_phone': profile.business_phone,
        'business_email': profile.business_email,
        'tax_rate': str(profile.tax_rate),
        'currency': profile.currency,
    })

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_me(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    # Update user fields
    user.first_name = request.data.get('first_name', user.first_name)
    user.last_name = request.data.get('last_name', user.last_name)
    user.email = request.data.get('email', user.email)
    user.save()
    
    # Update profile fields
    profile.business_name = request.data.get('business_name', profile.business_name)
    profile.business_address = request.data.get('business_address', profile.business_address)
    profile.business_phone = request.data.get('business_phone', profile.business_phone)
    profile.business_email = request.data.get('business_email', profile.business_email)
    profile.tax_rate = request.data.get('tax_rate', profile.tax_rate)
    profile.currency = request.data.get('currency', profile.currency)
    profile.save()
    
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    
    return Response({
        **user_data,
        'business_name': profile.business_name,
        'business_address': profile.business_address,
        'business_phone': profile.business_phone,
        'business_email': profile.business_email,
        'tax_rate': str(profile.tax_rate),
        'currency': profile.currency,
    })

# Generic CRUD ViewSets
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('-created_date')
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all().order_by('-created_date')
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_date')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(sku__icontains=search) |
                Q(category__icontains=search) |
                Q(supplier__icontains=search)
            )
        return queryset
    
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        items = request.data.get('items', [])
        products = []
        for item in items:
            serializer = self.get_serializer(data=item)
            serializer.is_valid(raise_exception=True)
            products.append(serializer.save())
        return Response(ProductSerializer(products, many=True).data, status=201)

class SaleOrderViewSet(viewsets.ModelViewSet):
    queryset = SaleOrder.objects.all().order_by('-created_date')
    serializer_class = SaleOrderSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        # Use a mutable copy — .pop() on the live QueryDict raises errors
        # and mutates shared request state otherwise.
        data = request.data.copy()
        items = data.pop('items', [])
        
        # Create sale order
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        sale_order = serializer.save()
        
        # Create sale items
        for item in items:
            SaleItem.objects.create(sale_order=sale_order, **item)
            
            # Update product stock
            try:
                product = Product.objects.get(id=item['product_id'])
                old_stock = product.stock_quantity
                product.stock_quantity = max(0, old_stock - item['quantity'])
                product.save()
                
                # Create stock movement
                StockMovement.objects.create(
                    product_id=product.id,
                    product_name=product.name,
                    product_sku=product.sku,
                    type='out',
                    quantity=item['quantity'],
                    reason=f"Sale Order {sale_order.order_number}",
                    reference=sale_order.order_number,
                    stock_before=old_stock,
                    stock_after=product.stock_quantity
                )
            except Product.DoesNotExist:
                pass
        
        return Response(self.get_serializer(sale_order).data, status=201)

class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.all().order_by('-created_date')
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        data = request.data

        # Resolve product and capture current stock BEFORE any changes.
        try:
            product = Product.objects.get(id=data.get('product_id'))
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        old_stock = product.stock_quantity
        movement_type = data.get('type')
        quantity = int(data.get('quantity', 0))

        if movement_type == 'in':
            new_stock = old_stock + quantity
        elif movement_type == 'out':
            new_stock = max(0, old_stock - quantity)
        else:  # adjustment
            new_stock = quantity

        # Persist the new product stock quantity.
        product.stock_quantity = new_stock
        product.save()

        # Create the movement record in a single save, passing stock values
        # as kwargs so the serializer (which marks them read_only) doesn't
        # strip them from validated_data.
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        movement = serializer.save(stock_before=old_stock, stock_after=new_stock)

        return Response(self.get_serializer(movement).data, status=status.HTTP_201_CREATED)

# File Upload View
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    file = request.FILES.get('file')
    if not file:
        return Response({'error': 'No file provided'}, status=400)
    
    # Save file
    path = default_storage.save(f'uploads/{file.name}', ContentFile(file.read()))
    file_url = request.build_absolute_uri(f'/media/{path}')
    
    return Response({'file_url': file_url})