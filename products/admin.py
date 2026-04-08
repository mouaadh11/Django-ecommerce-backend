from django.utils.html import format_html
from django.contrib import admin

# Register your models here.
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ['image_preview']
    fields = ['image_preview', 'image', 'is_primary']  # order matters

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="height:120px;width:120px;object-fit:cover;" /></a>',
                obj.image.url,
                obj.image.url
            )
        return "—"

    image_preview.short_description = 'Preview'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_tag', 'price',
                    'stock', 'is_active', 'created_at']
    list_filter = ['is_active', 'category']
    search_fields = ['name', 'sku']
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug': ('name',)}

    def image_tag(self, obj):
        image = obj.images.filter(is_primary=True).first()
        if image and image.image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="height:150px;width:150px;object-fit:cover;border-radius:6px;" /></a>',
                image.image.url,
                image.image.url
            )
        return "—"

    image_tag.short_description = 'Image'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['image_preview']   # 👈 important
    fields = ['name', 'slug', 'description',
              'image_preview', 'image']  # 👈 order
    list_display = ['name', 'slug', 'image_tag']

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="height:100px;width:100px;object-fit:cover;border-radius:6px;" /></a>',
                obj.image.url,
                obj.image.url
            )
        return "—"

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="height:200px;width:200px;object-fit:cover;border-radius:6px;" /></a>',
                obj.image.url,
                obj.image.url
            )
        return "No image"

    image_preview.short_description = "Preview"
