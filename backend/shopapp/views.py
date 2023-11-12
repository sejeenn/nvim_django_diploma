import django_filters.rest_framework
from django.http import JsonResponse
from django.core.paginator import Paginator

from rest_framework.views import APIView
# from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter

from .models import Category, Product
from .serializers import CatalogListSerializer


class CategoriesAPIView(APIView):
    """
    Класс, отвечающий за обработку категорий и подкатегорий продуктов
    """
    print("CategoriesAPIView ----------------------")

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
                "subcategory": subcategories_data,
            }
            categories_data.append(data_cat)
        print("categories_data -------------------------\n", categories_data)
        print("-----------------------------------------")
        return JsonResponse(categories_data, safe=False)


class CatalogListAPIView(APIView):
    print('CatalogListAPIView ----------------------------')
    serializer_class = CatalogListSerializer

    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_fields = {
        "category": ['exact'],
        "price": ["gte", "lte"],
        "freeDelivery": ["exact"],
        "count": ["gt"],
        "title": ["iregex"],
        "tags__name": ["exact"],
    }

    ordering_fields = [
        "id",
        "category__id",
        "price",
        "count",
        "date",
        "title",
        "freeDelivery",
        "rating",
        "tags",
    ]

    def filter_queryset(self, queryset):
        category_id = self.request.GET.get("category")
        min_price = float(self.request.GET.get("filter[minPrice]", 0))
        max_price = float(self.request.GET.get("filter[maxPrice]", float("inf")))
        free_delivery = (
            self.request.GET.get("filter[freeDelivery]", "").lower() == "true"
        )
        available = self.request.GET.get("filter[available]", "").lower() == "true"
        name = self.request.GET.get("filter[name]", "").strip()
        tags = self.request.GET.getlist("tags[]")

        if category_id:
            products = queryset.filter(category__id=category_id)

        products = queryset.filter(price__gte=min_price, price__lte=max_price)

        if free_delivery:
            products = queryset.filter(freeDelivery=True)

        if available:
            products = queryset.filter(count__gt=0)

        if name:
            products = queryset.filter(title__iregex=name)

        for tag in tags:
            products = queryset.filter(tags__name=tag)

        sort_field = self.request.GET.get("sort", "id")
        sort_type = self.request.GET.get("sortType", "inc")

        if sort_type == "inc":
            products = queryset.order_by(sort_field)
        products = queryset.order_by("-" + sort_field)

        return products

    def get_queryset(self):
        products = Product.objects.all()
        filtered_products = self.filter_queryset(products)
        return filtered_products

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page_number = int(request.GET.get("currentPage", 1))
        page_size = 3
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page_number)
        serializer = self.get_serializer(page_obj, many=True)
        response_data = {
            "items": serializer.data,
            "currentPage": page_number,
            "lastPage": paginator.num_pages,
        }
        return Response(response_data)
