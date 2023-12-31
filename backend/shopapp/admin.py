from django.contrib import admin

from .models import (
    Category, SubCategory,
    Product, ProductImage,
    Tag, Review, Specification, Sale,
    BasketItem, Basket, Order, DeliveryPrice, Payment
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


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = "pk", "user", "created_at"
    list_display_links = "pk", "user", "created_at"


@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = "pk", "product", "basket", "quantity"
    list_display_links = "pk", "product", "basket", "quantity"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = "pk", "created_at", "city", "delivery_address"
    list_display_links = "pk", "created_at", "city", "delivery_address"


@admin.register(DeliveryPrice)
class DeliveryPriceAdmin(admin.ModelAdmin):
    list_display = "pk", "delivery_cost", "delivery_express_cost", "delivery_free_minimum_cost"
    list_display_links = "pk", "delivery_cost", "delivery_express_cost", "delivery_free_minimum_cost"


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = "pk", "order", "card_number", "success"
    list_display_links = "pk", "order", "card_number"
