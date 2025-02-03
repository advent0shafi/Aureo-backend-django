from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .models import Product,Category,ProductImage
from rest_framework import viewsets
from .serializers import CategorySerializer,ProductDetailSerializer,ProductImageSerializer,ProductSerializer
# Create your views here.
from rest_framework.parsers import MultiPartParser, FormParser

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['patch'])
    def soft_delete(self, request, pk=None):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response({"status": "category soft deleted"}, status=status.HTTP_200_OK)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser]
    def _get_data_with_file_lists(self, request):
        """
        Build a new dictionary containing the normal request.data fields and add
        file fields as lists without doing a deep copy on file objects.
        """
        # Create a shallow dictionary from request.data
        data = {key: request.data.get(key) for key in request.data}

        # Add file lists explicitly
        data["banner_images"] = request.FILES.getlist("banner_images")
        data["detail_images"] = request.FILES.getlist("detail_images")
        return data

    def create(self, request, *args, **kwargs):
        data = self._get_data_with_file_lists(request)
        serializer = self.get_serializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        detail_serializer = ProductDetailSerializer(product, context={"request": request})
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProductDetailSerializer(instance, context={'request': request})
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        data = self._get_data_with_file_lists(request)
        serializer = self.get_serializer(instance, data=data, partial=partial, context={"request": request})
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        detail_serializer = ProductDetailSerializer(product, context={"request": request})
        return Response(detail_serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"status": "product deleted"}, status=status.HTTP_204_NO_CONTENT)