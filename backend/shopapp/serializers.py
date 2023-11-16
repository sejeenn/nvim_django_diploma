from rest_framework import serializers
from .models import (
    Product, Tag, Review, ProductImage, Specification
)


class CatalogListSerializer(serializers.Serializer):
    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        reviews = Review.objects.filter(product_id=instance.id).values_list(
            "rate", flat=True
        )
        tags = Tag.objects.filter(tags__id=instance.id)

        if reviews.count() == 0:
            rating = "Пока нет отзывов"
        else:
            rating = sum(reviews) / reviews.count()

        representation['title'] = instance.title
        representation['price'] = instance.price
        representation['images'] = instance.get_image()
        representation['tags'] = [{"id": tag.pk, "name": tag.name} for tag in tags]
        representation['reviews'] = reviews.count()
        representation['rating'] = rating
        return representation


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image',)


class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ('name', 'value')


class BannerListSerializer(CatalogListSerializer):
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        tags = Tag.objects.filter(tags__id=instance.id)
        rep["tags"] = [tag.name for tag in tags]

        return rep


class DetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        tags = Tag.objects.filter(tags__id=instance.id)
        images = ProductImage.objects.filter(product__id=instance.id)
        for img in images:
            print(img.image)
        rep["tags"] = [tag.name for tag in tags]
        rep['images'] = instance.get_image()

        return rep
