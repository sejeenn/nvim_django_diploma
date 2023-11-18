import json
import os

from django.conf import settings
from django.contrib.auth import logout, login, authenticate, hashers
from django.contrib.auth.models import User
from django.http.response import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ProfileUser
from .serializers import ProfileSerializer
from .forms import ProfileForm


class SignOutAPIView(APIView):
    """
    Класс, реализующий выход пользователя из системы
    """
    def post(self, request):
        logout(request)
        return Response(status=200)


class SignInAPIView(APIView):
    """
    Класс, реализующий вход пользователя в систему
    """
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(status=200)
        return Response(status=500)


class SignUpAPIView(APIView):
    """
    Класс, реализующий регистрацию пользователя и вход в систему
    При создании пользователя необходимо создавать защищенный
    пароль. Делается это при помощи:
    django.contrib.auth.hashers.make_password('any_password')
    """

    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        name = data['name']
        email = username + '@django.com'
        user = User.objects.create(username=username, email=email)
        user.password = hashers.make_password(password)
        user.save()
        # Пользователь создан

        # Создадим профиль пользователя, с аватаркой по-умолчанию
        ProfileUser.objects.create(
            user=user,
            email=email,
            avatar='avatar_default.png'
        )

        if user is not None:
            login(request, user)
            return Response(status=200)
        return Response(status=500)


class ProfileUserAPIView(APIView):
    """
    Класс отвечающий за вывод и редактирование
    информации о пользователе
    """
    def get(self, request):
        """
        Метод выводит на страницу профиля пользователя
        информацию о нём.
        """
        profile = ProfileUser.objects.get(user=request.user)
        print(profile.avatar)
        serializer = ProfileSerializer(profile)
        print(serializer.data)

        return Response(serializer.data)

    def post(self, request):
        """
        Метод, обновляющий информацию о пользователе
        """
        full_name = request.data['fullName'].split()
        surname = full_name[0]
        name = full_name[1]
        patronymic = full_name[2]
        phone = request.data['phone']

        profile = ProfileUser.objects.get(user=request.user)
        profile.surname = surname
        profile.name = name
        profile.patronymic = patronymic
        profile.phone = phone
        profile.save()

        data = {
            "full_name": f"{profile.surname} {profile.name} {profile.patronymic}",
            "email": profile.email,
            "phone": profile.phone,
            "avatar": {
                "src": profile.avatar.url,
                "alt": profile.avatar.name,
            },
        }

        return JsonResponse(data)


class AvatarChangeAPIView(APIView):
    """
    Класс отвечающий за смену аватарки пользователя.
    А так же удаление старого файла аватарки
    """

    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user_profile = ProfileUser.objects.get(user=request.user)
        avatar_file = request.FILES.get('avatar')
        avatar_path = os.path.join(settings.MEDIA_ROOT, str(user_profile.avatar))

        # если получили новый файл аватара, то удалим
        # старый, если он конечно доступен и это не аватарка по-умолчанию
        if avatar_file:
            if os.path.isfile(avatar_path) and user_profile.avatar != 'avatar_default.png':
                os.remove(avatar_path)

        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return Response(status=200)
        return Response(status=500)


class ChangePasswordAPIView(APIView):
    """
    Класс, отвечающий за смену пароля пользователя
    """

    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        current_password = request.data.get('currentPassword')
        new_password = request.data.get('newPassword')

        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            return Response(status=200)
        return Response(status=500)
