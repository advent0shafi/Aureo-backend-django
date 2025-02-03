
from rest_framework import serializers, viewsets
from .models import Category,ProductImage,Product
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    # For writing: accept a list of image files directly.
    banner_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    detail_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    # For reading: show the related image objects.
    banner_images_details = ProductImageSerializer(source="banner_images", many=True, read_only=True)
    detail_images_details = ProductImageSerializer(source="detail_images", many=True, read_only=True)
    
    class Meta:
        model = Product
        # List out all your fields plus the read-only nested representations.
        fields = [
            "id",
            "name_en",
            "name_ar",
            "description_en",
            "description_ar",
            "category",
            "price",
            "currency",
            "stock",
            "material",
            "diamond_weight",
            "diamond_quality",
            "sku",
            "thumbnail_image",
            # write-only fields (used for input):
            "banner_images",
            "detail_images",
            # read-only representations:
            "banner_images_details",
            "detail_images_details",
            "is_trending",
            "is_promoted",
            "is_arabic_special",
            "created_at",
            "updated_at",
        ]
    
    def create(self, validated_data):
        banner_files = validated_data.pop("banner_images", [])
        detail_files = validated_data.pop("detail_images", [])
        product = Product.objects.create(**validated_data)
        
        # Save banner images.
        for file in banner_files:
            image_obj = ProductImage.objects.create(image=file)
            product.banner_images.add(image_obj)
        
        # Save detail images.
        for file in detail_files:
            image_obj = ProductImage.objects.create(image=file)
            product.detail_images.add(image_obj)
        
        return product

    def update(self, instance, validated_data):
    # Pop out the file fields.
    # Note: if no file data is provided, these will be None.
        banner_data = validated_data.pop("banner_images", None)
        detail_data = validated_data.pop("detail_images", None)

        # Update all other simple fields.
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Only update banner images if a non-empty list is provided.
        if banner_data is not None and len(banner_data) > 0:
            instance.banner_images.clear()
            for file in banner_data:
                image_obj = ProductImage.objects.create(image=file)
                instance.banner_images.add(image_obj)

        # Only update detail images if a non-empty list is provided.
        if detail_data is not None and len(detail_data) > 0:
            instance.detail_images.clear()
            for file in detail_data:
                image_obj = ProductImage.objects.create(image=file)
                instance.detail_images.add(image_obj)

        return instance



class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    banner_images = ProductImageSerializer(many=True, read_only=True)
    detail_images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'