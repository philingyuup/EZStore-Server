from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.product import Product
from ..serializers import ProductSerializer, UserSerializer

# Create your views here.
class Products(generics.ListCreateAPIView):

    def get(self, request):
        """Index request"""
        products = Product.objects.all()
        # products = Product.objects.filter(owner=request.user.id)
        data = ProductSerializer(products, many=True).data
        return Response(data)

    permission_classes=(IsAuthenticatedOrReadOnly,)
    serializer_class = ProductSerializer
    def post(self, request):
        """Create request"""
        if not request.user.is_staff:
            raise PermissionDenied('Unauthorized, you do not work here!')
        # Add user to request object
        request.data['product']['owner'] = request.user.id
        # Serialize/create product
        product = ProductSerializer(data=request.data['product'])
        if product.is_valid():
            m = product.save()
            return Response(product.data, status=status.HTTP_201_CREATED)
        else:
            return Response(product.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):

    def get(self, request, pk):
        """Show request"""
        product = get_object_or_404(Product, pk=pk)
        data = ProductSerializer(product).data
        # Only want to show owned products?
        return Response(data)

    permission_classes=(IsAuthenticatedOrReadOnly,)
    def delete(self, request, pk):
        """Delete request"""
        product = get_object_or_404(Product, pk=pk)
        if not request.user.is_staff:
            raise PermissionDenied('Unauthorized, you do not work here!')
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Remove owner from request object
        if request.data['product'].get('owner', False):
            del request.data['product']['owner']

        # Locate Product
        product = get_object_or_404(Product, pk=pk)
        # Check if user is  the same
        if not request.user.is_staff:
            raise PermissionDenied('Unauthorized, you do not work here!')

        # Add owner to data object now that we know this user owns the resource
        request.data['product']['owner'] = request.user.id
        # Validate updates with serializer
        ms = ProductSerializer(product, data=request.data['product'])
        if ms.is_valid():
            ms.save()
            print(ms)
            return Response(ms.data)
        return Response(ms.errors, status=status.HTTP_400_BAD_REQUEST)
