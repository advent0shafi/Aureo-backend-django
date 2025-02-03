from django.contrib import admin
from .models import Category, Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = Product.detail_images.through  # To allow inline image management for products
    extra = 1  # To display at least one empty form to add a ProductImage

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_ar', 'sku', 'description_en', 'description_ar', 'image',)
    search_fields = ('name_en', 'name_ar', 'sku')
    list_filter = ('sku',)
    ordering = ('name_en',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_ar', 'price', 'currency', 'stock', 'material', 'sku', 'category', 'is_trending', 'is_promoted', 'is_arabic_special',)
    search_fields = ('name_en', 'name_ar', 'sku', 'category__name_en', 'category__name_ar')
    list_filter = ('category', 'is_trending', 'is_promoted', 'is_arabic_special')
    ordering = ('-created_at',)
    prepopulated_fields = {'sku': ('name_en',)}  # Auto-fill SKU from product name
    inlines = [ProductImageInline]  # To include ProductImages inline in the product form

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'alt_text', 'created_at')
    search_fields = ('alt_text',)
    ordering = ('-created_at',)

# Register models
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
