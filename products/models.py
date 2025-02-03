from django.db import models

class Category(models.Model):
    name_en = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255)
    description_en = models.TextField()
    description_ar = models.TextField()
    image = models.ImageField(upload_to='categories/')
    sku = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name_en

class Product(models.Model):
    name_en = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255)
    description_en = models.TextField()
    description_ar = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    stock = models.IntegerField()
    material = models.CharField(max_length=100)
    diamond_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    diamond_quality = models.CharField(max_length=50, null=True, blank=True)
    sku = models.CharField(max_length=100, unique=True)
    thumbnail_image = models.ImageField(upload_to='products/thumbnails/')
    banner_images = models.ManyToManyField('ProductImage', related_name='banner_images', blank=True)
    detail_images = models.ManyToManyField('ProductImage', related_name='detail_images', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_trending = models.BooleanField(default=False)
    is_promoted = models.BooleanField(default=False)
    is_arabic_special = models.BooleanField(default=False)


    def __str__(self):
        return self.name_en

class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/images/')
    alt_text = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.alt_text or "Product Image"
