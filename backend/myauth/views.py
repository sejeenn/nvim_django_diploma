import json

from django.contrib.auth import logout, login, authenticate, hashers
from django.contrib.auth.models import User
from django.http.response import HttpResponse, JsonResponse
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
        # Пользователь создан, необходимо создать профиль пользователя
        ProfileUser.objects.create(user=user, email=email)

        if user is not None:
            login(request, user)
            return Response(status=200)
        return Response(status=500)


class ProfileUserAPIView(APIView):
    def get(self, request):
        profile = ProfileUser.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
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
    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return HttpResponse(status=200)
