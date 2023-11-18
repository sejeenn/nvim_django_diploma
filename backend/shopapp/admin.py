from django.contrib import admin

from .models import (
    Category, SubCategory,
    Product, ProductImage,
    Tag, Review, Specification, Sale
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "pk", "title"
    list_display_links = "pk", "title"
    ordering = ("pk", )
    search_fields = ("title", )


@admin.register(SubCategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = "pk", "title"
    list_display_links = "pk", "title"
    ordering = ("pk",)
    search_fields = ("title",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = "pk", "title", "price"
    list_display_links = "pk", "title", "price"
    ordering = ("pk", )
    search_fields = ("title", )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = "pk", "name",
    list_display_links = "pk", "name",


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = "pk", "product", "image"
    list_display_links = "pk", "product", "image"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = "pk", "author", "rate", "date", "product"
    list_display_links = "pk", "author", "rate", "date", "product"


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "value"
    list_display_links = "pk", "name", "value"


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = "pk", "product", "date_from", "date_to", "discount"
    list_display_links = "pk", "product", "date_from", "date_to", "discount"

