import json

from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.contrib.auth.models import User

from rest_framework.views import APIView

from .models import Shopper


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
        user = User.objects.create(
            username=body['username'],
            password=body['password'],
            email=body['username'] + '@supermail.ru'
        )
        user.save()
        if user is not None:
            login(request, user)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=500)


class UpdateShopperView(APIView):
    def get(self, request):
        """
        1.Получить данные о пользователе из БД
        2.Пропустить полученные данные через сериалайзер.
        3.Вернуть обработанные данные
        """
        print(request.user)
        shopper = User.objects.all()
        print(shopper)
        return HttpResponse(status=200)