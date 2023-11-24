import datetime
import json

from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from django.http import JsonResponse
from django.core.paginator import Paginator

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny

from .models import Category, Product, Review, Tag, Sale, Basket, BasketItem, DeliveryPrice, Order
from .serializers import (
    DetailsSerializer,
    TagListSerializer,
    ProductSerializer,
    BasketItemSerializer,
    OrderSerializer,
)
from myauth.models import ProfileUser


class CategoryListView(APIView):
    """
    Класс, отвечающий за обработку категорий и подкатегорий продуктов
    которые будут отображаться по нажатию на кнопку "All Departments"
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
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    filterset_fields = {
        'category': ['exact'],  # точное соответствие
        'price': ['gte', 'lte'],  # диапазон от "больше или равно" до "меньше или равно"
        'freeDelivery': ['exact'],  # точное соответствие
        'count': ['gt'],  # больше
        'title': ['icontains'],  # содержит (неточное определение)
        'tags__name': ['exact'],  # точное соответствие
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
        sort_field = self.request.GET.get('sort', 'id')
        sort_type = self.request.GET.get('sortType', 'inc')

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
                    "rating": float(product.rating),
                }
            )
        catalog_data = {
            "items": products_list,
            "currentPage": page_number,
            "lastPage": paginator.num_pages
        }
        return Response(catalog_data)


class BannerListAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Выведем на главную страницу магазина три продукта с
        самым большим рейтингом.
        """
        return Product.objects.filter(rating__gt=0).order_by('-rating')[:3]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PopularListAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Выведем на главную страницу заказы, имеющие тег "popular"
        """
        # после реализации заказов подставить - .order_by("-countOfOrders")[:8]
        return Product.objects.filter(tags__name__in=['popular'])[:8]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class LimitedListAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Выведем на главную страницу заказы, имеющие тег "limited"
        """
        return Product.objects.filter(tags__name__in=['limited'])[:16]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductDetailsAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = DetailsSerializer
    lookup_url_kwarg = "id"


class ProductReviewAPIView(ProductDetailsAPIView):
    def post(self, request, **kwargs):
        if request.user.is_authenticated:
            profile = ProfileUser.objects.get(user=request.user)
            product = Product.objects.get(pk=kwargs['id'])
            author = profile
            text = request.data['text']
            rate = request.data['rate']

            review = Review.objects.create(
                author=author,
                text=text,
                rate=rate,
                product=product,
            )
            review.save()
            return Response(status=200)
        return Response(status=403)


class TagsListAPIView(ListAPIView):
    serializer_class = TagListSerializer

    def get_queryset(self):
        return Tag.objects.all().distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SalesListAPIView(APIView):
    def get(self, request):
        page_number = int(request.GET.get('currentPage', 1))
        limit = int(request.GET.get('limit', 20))
        obj_list = []
        for obj in Sale.objects.all():
            obj_list.append(obj)
        paginator = Paginator(obj_list, limit)
        page = paginator.get_page(page_number)
        serialized_data = []

        for sale in page:
            serialized_data.append({
                "id": sale.product.id,
                "price": sale.product.price,
                "salePrice": sale.product.price - sale.discount,
                "dateFrom": sale.date_from,
                "dateTo": sale.date_to,
                "title": sale.product.title,
                "images": [
                    {
                        "src": settings.MEDIA_URL + str(image.image),
                        "alt": sale.product.title,
                    }
                    for image in
                    sale.product.images.all()],
            })
        response_data = {
            "items": serialized_data,
            "currentPage": page_number,
            "lastPage": paginator.num_pages
        }
        return Response(response_data)


class BasketAPIView(APIView):

    def get(self, request):
        """
        Вывод информации о товарах в корзине
        """

        if request.user.is_anonymous:
            anon_user = User.objects.get(username="anonymous")
            request.user = User.objects.get(id=anon_user.id)

        queryset = BasketItem.objects.filter(basket__user=request.user)
        serializer = BasketItemSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request):
        # принимаем данные, об id товара и его количестве из запроса
        id = request.data['id']
        count = request.data['count']

        # если вход не осуществлен, то назначаем пользователя по-умолчанию
        if request.user.is_anonymous:
            anon_user = User.objects.get(username="anonymous")
            basket, created = Basket.objects.update_or_create(user=anon_user)
            basket = Basket.objects.get(user=anon_user)
        else:
            try:
                basket = request.user.basket
            except Basket.DoesNotExist:
                basket = Basket.objects.create(user=request.user)

        # получаем объект продукта по его id
        product = Product.objects.get(id=id)
        # создаем объект продукта в корзине если его еще нет
        basket_item, created = BasketItem.objects.get_or_create(basket=basket, product=product)
        # добавляем в корзину количество (count) выбранного товара
        basket_item.quantity = count
        basket_item.save()

        # получаем обновленные данные корзины, передаем в сериализатор
        # где они обрабатываются и возвращаются для отображения на страничке
        basket_items = BasketItem.objects.filter(basket=basket)
        serializer = BasketItemSerializer(basket_items, many=True)

        return Response(serializer.data, status=201)

    def delete(self, request):
        id = request.data['id']
        count = request.data['count']

        try:
            if request.user.is_anonymous:
                anon_user = User.objects.get(username="anonymous")
                request.user = User.objects.get(id=anon_user.id)
            # получаем объект, который хотим удалить
            basket = request.user.basket
            # получаем продукт, который хотим удалить из корзины
            product = Product.objects.get(id=id)
            # получаем товар в корзине для удаления
            basket_item = BasketItem.objects.get(basket=basket, product=product)
            if basket_item.quantity > count:
                basket_item.quantity -= count   # будем нажимать кнопку "минус" до тех пор пока не будет 0
                basket_item.save()
            else:
                basket_item.delete()

            # получаем обновленные данные корзины, передаем в сериализатор
            # где они обрабатываются и возвращаются для отображения на страничке
            basket_items = BasketItem.objects.filter(basket=basket)
            serializer = BasketItemSerializer(basket_items, many=True)

            return Response(serializer.data)
        except Basket.DoesNotExist:
            return Response("Товары в корзине не найдены", status=404)


class CreateOrderAPIView(APIView):
    def post(self, request):
        try:
            basket = request.user.basket
            profile = ProfileUser.objects.get(user=request.user)
            basket_items = BasketItem.objects.filter(basket__user=request.user)
            total_cost = 0
            order = Order.objects.create(
                full_name=profile,
                basket=basket,
            )
            for item in basket_items:
                product = Product.objects.get(pk=item.product.pk)
                product.count_of_orders = item.quantity
                total_cost += item.product.price * item.quantity
                product.save()
            delivery_price = DeliveryPrice.objects.get(id=1)
            if total_cost > delivery_price.delivery_free_minimum_cost:
                order.totalCost = total_cost
            else:
                order.totalCost = total_cost + delivery_price.delivery_cost
            order.save()
            response_data = {"orderId": order.pk}
            return JsonResponse(response_data)
        except Basket.DoesNotExist:
            error_data = {"error": "У данного пользователя пока нет 'корзины'"}
            return JsonResponse(error_data)


class OrderDetailAPIView(APIView):
    def get(self, request, order_id):
        order = Order.objects.get(pk=order_id)
        serializer = OrderSerializer(order)
        return JsonResponse(serializer.data)

    def post(self, request, order_id):
        print(request.data)
        return Response(status=200)

