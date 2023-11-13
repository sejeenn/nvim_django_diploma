from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from django.http import JsonResponse
from django.core.paginator import Paginator

from rest_framework.views import APIView
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
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]

    filterset_fields = {
        'category': ['exact'],
        'price': ['gte', 'lte'],
        'freeDelivery': ['exact'],
        'count': ['gt'],
        'title': ['icontains'],
        'tags__name': ['exact'],
    }

    ordering_fields = [
        'id',
        'category__id',
        'price',
        'count',
        'date',
        'title',
        'freeDelivery',
        'rating',
    ]

    def filter_queryset(self, products):
        category_id = self.request.GET.get('category')
        min_price = float(self.request.GET.get('filter[minPrice]', 0))
        max_price = float(self.request.GET.get('filter[maxPrice]', float('inf')))
        free_delivery = self.request.GET.get('filter[freeDelivery]', '').lower() == 'true'
        available = self.request.GET.get('filter[available]', '').lower() == 'true'
        name = self.request.GET.get('filter[name]', '').strip()
        tags = self.request.GET.getlist('tags[]')

        if category_id:
            products = products.filter(category__id=category_id)

        products = products.filter(price__gte=min_price, price__lte=max_price)

        if free_delivery:
            products = products.filter(freeDelivery=True)

        if available:
            products = products.filter(count__gt=0)

        if name:
            products = products.filter(title__icontains=name)

        for tag in tags:
            products = products.filter(tags__name=tag)

        sort_field = self.request.GET.get('sort', 'id')
        sort_type = self.request.GET.get('sortType', 'inc')

        if sort_type == 'inc':
            products = products.order_by(sort_field)
        else:
            products = products.order_by('-' + sort_field)

        return products

    def get(self, request):
        products = Product.objects.all()
        filtered_products = self.filter_queryset(products)
        page_number = int(request.GET.get('currentPage', 1))
        limit = int(request.GET.get('limit', 20))
        sort_field = request.GET.get('sort', 'id')
        sort_type = request.GET.get('sortType', 'asc')

        paginator = Paginator(filtered_products, limit)
        page = paginator.get_page(page_number)

        products_list = []
        for product in page:
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
            "currentPage": page_number,
            "lastPage": paginator.num_pages
        }
        return Response(catalog_data)
