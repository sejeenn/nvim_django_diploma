import json

from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from rest_framework.response import Response

from rest_framework.views import APIView

from .models import Profile
from .serializers import ProfileSerializer
from .forms import ProfileForm


class SignInAPIView(APIView):
    def post(self, request):
        body = json.loads(request.body)
        username = body['username']
        password = body['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=500)


class SignOutAPIView(APIView):
    def post(self, request):
        logout(request)
        return HttpResponse(status=200)


class SignUpAPIView(APIView):
    def post(self, request):
        # Сначала создается пользователь
        body = json.loads(request.body)
        username = body['username']
        password = body['password']
        email = username + '@supermail.ru'
        user = User.objects.create(
            username=username,
            password=password,
            email=email,
        )
        user.save()

        # Затем, к созданному пользователю создаётся его профиль
        Profile.objects.create(user=user, email=email)

        if user is not None:
            login(request, user)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=500)


class ProfileAPIView(APIView):
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        full_name = request.data['fullName'].split()
        surname = full_name[0]
        name = full_name[1]
        patronymic = full_name[2]
        phone = request.data['phone']

        profile = Profile.objects.get(user=request.user)
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


class PasswordChangeAPIView(APIView):
    def post(self, request):
        user = request.user
        data = json.loads(request.body)
        print(request.data)
        if user.check_password(data['currentPassword']):
            password = data['newPassword']
            user.set_password = password
            user.save()
        else:
            return HttpResponse(status=500)
        return HttpResponse(status=200)


