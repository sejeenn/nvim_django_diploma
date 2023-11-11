from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from .models import Category
from .serializers import CatalogListSerializer


class CategoriesListView(ListAPIView):
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
            }
            categories_data.append(data_cat)
        print(categories_data)
        return JsonResponse(categories_data, safe=False)


class CatalogListAPIView(ListAPIView):
    serializer_class = CatalogListSerializer
    print("serializer_class", serializer_class)

