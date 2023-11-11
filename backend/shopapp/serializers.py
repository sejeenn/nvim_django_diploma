from rest_framework import serializers
from .models import Product, Tag, Review


class CatalogListSerializer(serializers.Serializer):
    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        reviews = Review.objects.filter(product_id=instance.id).values_list(
            "rate", flat=True
        )
        tags = Tag.objects.filter(tag__id=instance.id)

        if reviews.count() == 0:
            rating = "Пока нет отзывов"
        else:
            rating = sum(reviews) / reviews.count()

        representation['images'] = instance.get_image()
        representation['tags'] = [{"id": tag.pk, "name": tag.name} for tag in tags]
        representation['reviews'] = reviews.count()
        representation['rating'] = rating

        return representation

