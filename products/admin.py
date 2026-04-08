from django.contrib import admin

# Register your models here.
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'is_active', 'created_at']
    list_filter = ['is_active', 'category']
    search_fields = ['name', 'sku']
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug': ('name',)}    # Auto-fill slug from name


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}