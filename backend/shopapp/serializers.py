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


class CustomDecimalField(serializers.DecimalField):
    def to_representation(self, value):
        return value


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()
    # specifications = ProductSpecificationSerializer(many=True)
    price = CustomDecimalField(max_digits=10, decimal_places=2)
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_category(self, obj):
        return str(obj.category.id)

    def get_reviews(self, obj):
        reviews = Review.objects.filter(product=obj)
        return [
            {
                "author": review.author,
                "text": review.text,
                "date": review.date.strftime('%Y-%m-%d %H:%M'),
                "rate": review.rate,
            }
            for review in reviews
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        images = []
        for image in rep['images']:
            images.append(
                {
                    "src": image.get("image", ""),
                    "alt": image.get("alt", ""),
                }

            )
        rep['images'] = images
        rep['id'] = str(rep['id'])
        return rep


