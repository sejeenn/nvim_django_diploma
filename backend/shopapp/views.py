import django_filters.rest_framework
from django.conf import settings
from django.http import JsonResponse
from django.core.paginator import Paginator

from rest_framework.views import APIView
# from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter

from .models import Category, Product
from .serializers import CatalogListSerializer


class CategoryListView(APIView):
    """
    Класс, отвечающий за обработку категорий и подкатегорий продуктов
    """

    def get(self, request):
        categories = Category.objects.all()
        categories_data = []
        for category in categories:
            subcategories = category.subcategory_set.all()
            subcategories_data = []
            for subcategory in subcategories:
                data_sub = {
                    "id": subcategory.pk,
                    "title": subcategory.title,
                    "image": subcategory.get_image(),
                }
                subcategories_data.append(data_sub)
            data_cat = {
                "id": category.pk,
                "title": category.title,
                "image": category.get_image(),
                "subcategories": subcategories_data,
            }
            categories_data.append(data_cat)

        return JsonResponse(categories_data, safe=False)


class CatalogListAPIView(APIView):

    def get(self, request):
        products = Product.objects.all()
        products_list = []
        for product in products:
            products_list.append(
                {
                    "id": product.pk,
                    "category": product.category.pk,
                    "price": product.price,
                    "count": product.count,
                    "date": product.date,
                    "title": product.title,
                    "description": product.description,
                    "freeDelivery": product.freeDelivery,
                    "images": [{
                        "src": settings.MEDIA_URL + str(image.image),
                        "alt": product.title
                    }
                        for image in product.images.all()],
                    "tags": list(product.tags.values_list('name', flat=True)),
                    # "reviews": product.re,
                    "rating": float(product.rating),
                }
            )
        catalog_data = {
            "items": products_list,
        }
        return Response(catalog_data)
