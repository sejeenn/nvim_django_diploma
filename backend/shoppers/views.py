import json

from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Shopper
from .serializers import ShopperSerializer


class LoginView(APIView):
    """
    Класс обрабатывает вход пользователя с логином и паролем
    """
    def post(self, request):
        body = json.loads(request.body)
        user = authenticate(
            request,
            username=body['username'],
            password=body['password']
        )
        if user is not None:
            login(request, user)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=500)


class LogoutView(APIView):
    """
    Класс обрабатывает выход пользователя
    """
    def post(self, request):
        logout(request)
        return HttpResponse(status=200)


class RegisterShopperView(APIView):
    """
        Класс обрабатывает создание нового пользователя
        с логином, паролем и email
    """
    def post(self, request):
        body = json.loads(request.body)
        name = str(body['name']).split()
        username = body['username']
        password = body['password']
        email = body['username'] + '@supermail.ru'

        user = User.objects.create(
            username=username,
            password=password,
            email=email
        )
        user.save()

        if len(name) == 1:
            Shopper.objects.create(username=user, first_name=name[0], email=email)
        elif len(name) == 2:
            Shopper.objects.create(username=user, first_name=name[0], last_name=name[1], email=email)
        elif len(name) == 3:
            Shopper.objects.create(
                username=user, first_name=name[0],
                middle_name=name[1], last_name=name[2], email=email)

        if user is not None:
            login(request, user)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=500)


class UpdateShopperView(APIView):
    def get(self, request):
        """
        1.Получить данные о покупателе из БД
        2.Пропустить полученные данные через сериалайзер.
        3.Вернуть обработанные данные
        """
        shopper = Shopper.objects.get(username=request.user)
        serializer = ShopperSerializer(shopper)
        return Response(serializer.data)

    def post(self, request):
        name = request.data['fullName'].split()
        last_name, first_name, middle_name, = name[0], name[1], name[2]
        phone = request.data['phone']

        shopper = Shopper.objects.get(username=request.user)
        shopper.first_name = first_name
        shopper.middle_name = middle_name
        shopper.last_name = last_name
        shopper.phone = phone
        shopper.save()

        data = {
            "fullName": f"{shopper.last_name} {shopper.first_name} {shopper.middle_name}",
            "email": shopper.email,
            "phone": shopper.phone,
            "avatar": {
                "src": shopper.avatar.url,
                "alt": shopper.avatar.first_name,
            },

        }

        return JsonResponse(data)