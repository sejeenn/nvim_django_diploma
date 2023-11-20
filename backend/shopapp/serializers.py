from rest_framework import serializers
from .models import (
    Product, Tag, Review, ProductImage, Specification, BasketItem
)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        reviews = Review.objects.filter(product_id=instance.id).values_list(
            "rate", flat=True
        )
        tags = Tag.objects.filter(tags__id=instance.id)
        if reviews.count() == 0:
            rating = "Пока нет отзывов"
        else:
            rating = sum(reviews) / reviews.count()
        rep['title'] = instance.title
        rep['price'] = instance.price
        rep['images'] = instance.get_image()
        rep['tags'] = [{"id": tag.pk, "name": tag.name} for tag in tags]
        rep['reviews'] = reviews.count()
        rep['rating'] = rating

        rep['id'] = instance.pk
        rep["category"] = instance.category.pk
        rep['count'] = instance.count
        rep['date'] = instance.date.strftime("%Y.%m.%d %H:%M")
        rep['description'] = instance.description
        rep['freeDelivery'] = instance.freeDelivery
        return rep


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image',)


class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ('name', 'value')


class TagListSerializer(serializers.ModelSerializer):
    """Сериализатор для представления тегов"""

    id = serializers.CharField(source="name")

    class Meta:
        model = Tag
        fields = ["id", "name"]


class DetailsSerializer(ProductSerializer):
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        specifications = Specification.objects.filter(pk=instance.id)
        reviews = Review.objects.filter(product_id=instance.id)

        rep['specifications'] = [{'name': spec.name, 'value': spec.value} for spec in specifications]
        rep['reviews'] = [
            {
                'author': f'{review.author.name} {review.author.surname}',
                'email': review.author.email,
                'text': review.text,
                'rate': review.rate,
                'date': review.date.strftime("%Y.%m.%d %H:%M"),
            }
            for review in reviews
        ]
        return rep


class BasketItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления корзины и продуктов в ней
    """
    class Meta:
        model = BasketItem
        fields = (
            "product", "count",
        )

    def to_representation(self, instance):
        data = ProductSerializer(instance.product).data
        data['count'] = instance.quantity
        return data
